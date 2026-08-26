"""Separa CONTENIDO de MARCA SINTACTICA en la firma paraconsistente fuerte.

La pregunta que decide todo es la INTERACCION fenomeno x forma:

  H1  contenido   : los items eticos BARE producen T+F>1 mas que los no-eticos BARE.
                    Si falla, el resultado del corpus v3 era el fraseo.
  H2  marca sola  : los items NO eticos MARKED no producen T+F>1.
                    Si falla, la conjuncion de opuestos dispara la firma por si sola.
  H3  interaccion : el salto bare->marked es mayor en no-eticos que en eticos
                    (porque los eticos ya estaban altos). Cuantifica cuanto de la
                    firma es contenido y cuanto es marca.
  H4  anclas      : tautologias y consensos en cero.
  H5  fiabilidad  : varianza entre items DENTRO de fenomeno, que con n=1 era
                    inestimable y es la razon de ser de este banco.

Uso:  python analyze_bank.py [--raw results/raw_bank.jsonl]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent / "results"
CONTESTED = ["ethical", "ignorance", "vagueness", "contingency", "paradox"]


def load(raw: Path) -> pd.DataFrame:
    rows = [json.loads(l) for l in raw.read_text(encoding="utf-8").splitlines() if l.strip()]
    df = pd.DataFrame(rows)
    n0 = len(df)
    df = df[df["parsed"] & ~df["error"]].copy()
    for c in "TIF":
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=list("TIF"))
    df["TF"] = df["T"] + df["F"]
    df["strong"] = (df["TF"] > 1.0).astype(int)
    print(f"[datos] registros={n0}  usables={len(df)}  "
          f"fallo de parseo={(n0-len(df))/max(n0,1):.1%}")
    return df


def boot_ci(x, n=5000, seed=11):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype=float)
    if len(x) < 3:
        return (np.nan, np.nan)
    b = [rng.choice(x, len(x), replace=True).mean() for _ in range(n)]
    return tuple(np.percentile(b, [2.5, 97.5]).round(3))


def main(raw: Path):
    OUT.mkdir(exist_ok=True)
    df = load(raw)
    core = df[df["phenomenon"].isin(CONTESTED)]

    # --- tabla principal: fenomeno x forma -----------------------------------
    tab = core.pivot_table(index="phenomenon", columns="form", values="strong",
                           aggfunc="mean").reindex(CONTESTED).round(3)
    tab["delta"] = (tab["marked"] - tab["bare"]).round(3)
    n = core.pivot_table(index="phenomenon", columns="form", values="strong",
                         aggfunc="size").reindex(CONTESTED)
    print("\n=== TASA FUERTE (T+F>1) por fenomeno x forma ===")
    print(tab.to_string())
    print("\n  n por celda:")
    print(n.to_string())
    tab.to_csv(OUT / "main_phenomenon_x_form.csv")

    # --- H1: contenido -------------------------------------------------------
    eb = core[(core.phenomenon == "ethical") & (core.form == "bare")]["strong"]
    ob = core[(core.phenomenon != "ethical") & (core.form == "bare")]["strong"]
    print("\n=== H1  contenido: etico BARE vs no-etico BARE ===")
    print(f"  etico bare    = {eb.mean():.3f}  IC95 {boot_ci(eb)}  n={len(eb)}")
    print(f"  no-etico bare = {ob.mean():.3f}  IC95 {boot_ci(ob)}  n={len(ob)}")
    print(f"  -> {'SOSTENIDO' if eb.mean() > ob.mean() else 'NO SOSTENIDO'}: "
          "el contenido etico eleva la firma sin marca sintactica"
          if eb.mean() > ob.mean() else
          "  -> NO SOSTENIDO: el resultado del corpus v3 era el fraseo")

    # --- H2: la marca por si sola --------------------------------------------
    om = core[(core.phenomenon != "ethical") & (core.form == "marked")]["strong"]
    print("\n=== H2  marca sola: no-etico MARKED ===")
    print(f"  no-etico marked = {om.mean():.3f}  IC95 {boot_ci(om)}  n={len(om)}")
    print("  -> si es alto, la conjuncion de opuestos dispara la firma por si sola,")
    print("     y la firma NO es diagnostica de conflicto de valores.")

    # --- H3: descomposicion --------------------------------------------------
    em = core[(core.phenomenon == "ethical") & (core.form == "marked")]["strong"]
    print("\n=== H3  cuanto es contenido y cuanto es marca ===")
    print(f"  efecto CONTENIDO (etico bare - no-etico bare) = {eb.mean()-ob.mean():+.3f}")
    print(f"  efecto MARCA     (no-etico marked - no-etico bare) = {om.mean()-ob.mean():+.3f}")
    print(f"  INTERACCION      = {(em.mean()-eb.mean()) - (om.mean()-ob.mean()):+.3f}")

    # --- H4: anclas ----------------------------------------------------------
    anch = df[df["form"] == "anchor"]
    print("\n=== H4  anclas ===")
    print(anch.groupby("phenomenon")[["strong", "TF"]].mean().round(3).to_string())

    # --- H5: variabilidad ENTRE items dentro de fenomeno ---------------------
    print("\n=== H5  variabilidad entre items dentro de cada fenomeno (forma bare) ===")
    rows = []
    for ph, g in core[core.form == "bare"].groupby("phenomenon"):
        per = g.groupby("item_id")["strong"].mean()
        rows.append({"phenomenon": ph, "n_items": len(per), "mean": per.mean().round(3),
                     "sd_between_items": per.std(ddof=1).round(3),
                     "min": per.min().round(3), "max": per.max().round(3)})
    h5 = pd.DataFrame(rows).set_index("phenomenon").reindex(CONTESTED)
    print(h5.to_string())
    print("  Con un item por fenomeno esta columna era inestimable. Si sd es grande,")
    print("  cualquier tasa publicada a partir de un solo enunciado era ruido.")
    h5.to_csv(OUT / "h5_between_item_variance.csv")

    # --- por modelo ----------------------------------------------------------
    print("\n=== robustez por modelo: etico bare vs no-etico bare ===")
    for m, g in core[core.form == "bare"].groupby("model"):
        e = g[g.phenomenon == "ethical"]["strong"].mean()
        o = g[g.phenomenon != "ethical"]["strong"].mean()
        print(f"  {m:20s} etico={e:.3f}  no-etico={o:.3f}  -> {'SI' if e > o else 'NO'}")

    print(f"\nescritos CSV en {OUT}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=str(OUT / "raw_bank.jsonl"))
    main(Path(ap.parse_args().raw))
