"""La escalera de tres peldanos medida sobre 110 items en vez de sobre 8.

El estudio previo (corpus v3 + escalera) tenia UN enunciado por fenomeno, asi que
ninguna afirmacion a nivel de fenomeno era estimable y la varianza entre items era
inaccesible por construccion. Este analisis la estima.

Preguntas, en orden de cuanto deciden sobre el formalismo:

  Q1  ocupacion   : se pueblan los tres peldanos sobre un banco real?
  Q2  N vs I      : son distinguibles, y con cuanta varianza ENTRE items?
  Q3  glosa       : la dependencia de la glosa sobrevive con 110 items?
  Q4  entre items : cuanto varia la asignacion de peldano de un item a otro
                    DENTRO del mismo fenomeno? (inestimable con n=1)
  Q5  contenido   : el peldano depende del contenido o de la marca sintactica,
      vs marca      ahora para los TRES peldanos y no solo para el fuerte

Uso:  python analyze_quad_bank.py [--raw results/raw_quad_bank.jsonl]
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent / "results"
CONTESTED = ["ethical", "ignorance", "vagueness", "contingency", "paradox"]
RUNGS = ["strong", "weak", "very_weak", "classical"]


def load(raw: Path) -> pd.DataFrame:
    rows = [json.loads(l) for l in raw.read_text(encoding="utf-8").splitlines() if l.strip()]
    df = pd.DataFrame(rows)
    n0 = len(df)
    df = df[df["parsed"] & ~df["error"]].copy()
    for c in "TINF":
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=list("TINF"))
    df["TF"] = df["T"] + df["F"]
    print(f"[datos] registros={n0}  usables={len(df)}  "
          f"fallo de parseo={(n0-len(df))/max(n0,1):.1%}")
    return df


def fleiss(piv):
    piv = piv.dropna()
    if len(piv) < 4 or piv.shape[1] < 2:
        return np.nan, len(piv)
    cats = sorted(set(piv.values.ravel()))
    n = piv.shape[1]
    cnt = np.array([[list(r).count(c) for c in cats] for r in piv.values])
    P = ((cnt ** 2).sum(1) - n) / (n * (n - 1))
    pj = cnt.sum(0) / (len(piv) * n)
    pe = (pj ** 2).sum()
    return (float((P.mean() - pe) / (1 - pe)) if pe < 1 else np.nan), len(piv)


def pct(df, index):
    t = df.groupby(index)["rung"].value_counts(normalize=True).unstack(fill_value=0)
    return t.reindex(columns=RUNGS, fill_value=0).round(3)


def main(raw: Path):
    OUT.mkdir(exist_ok=True)
    df = load(raw)
    core = df[df["phenomenon"].isin(CONTESTED)]
    anchors = df[df["form"] == "anchor"]

    # ---- Q1 ocupacion --------------------------------------------------------
    print("\n=== Q1  ocupacion de los peldanos sobre 110 items ===")
    occ = pct(df.assign(grp=np.where(df["form"] == "anchor", "anchors", "contested")), "grp")
    print(occ.to_string())
    vw = pct(core, "phenomenon").reindex(CONTESTED)["very_weak"]
    print(f"\n  peldano MUY DEBIL, global contested = "
          f"{(core['rung']=='very_weak').mean():.3f}")
    print("  por fenomeno:", vw.to_dict())
    print("  (el estudio con 8 items reporto 0.120; si aqui difiere mucho,")
    print("   aquella cifra era una propiedad de esas ocho oraciones)")
    occ.to_csv(OUT / "quad_q1_occupancy.csv")

    # ---- Q2 N vs I -----------------------------------------------------------
    print("\n=== Q2  N frente a I, con varianza entre items ===")
    r = core["N"].corr(core["I"])
    mad = float((core["N"] - core["I"]).abs().mean())
    print(f"  correlacion global(N, I) = {r:.3f}   |N-I| medio = {mad:.3f}")
    per = core.groupby("item_id")[["N", "I"]].mean()
    print(f"  correlacion ENTRE items (medias por item) = {per['N'].corr(per['I']):.3f}")
    print(f"  medias: I={core['I'].mean():.3f}  N={core['N'].mean():.3f}")
    print("\n  N medio por fenomeno:")
    print(core.groupby("phenomenon")[["I", "N"]].mean().round(3)
              .reindex(CONTESTED).to_string())
    pd.DataFrame([{"corr_global": r, "mad": mad,
                   "corr_between_items": per["N"].corr(per["I"])}]
                 ).to_csv(OUT / "quad_q2_N_vs_I.csv", index=False)

    # ---- Q3 glosa ------------------------------------------------------------
    print("\n=== Q3  dependencia de la glosa sobre el banco ===")
    g = pct(core, "gloss")
    print(g.to_string())
    print(f"  rango de la tasa FUERTE entre glosas = "
          f"{g['strong'].max()-g['strong'].min():.3f}")
    print(f"  rango de MUY DEBIL entre glosas      = "
          f"{g['very_weak'].max()-g['very_weak'].min():.3f}")
    g.to_csv(OUT / "quad_q3_gloss.csv")

    # ---- Q4 varianza ENTRE items --------------------------------------------
    print("\n=== Q4  varianza entre items dentro de fenomeno (lo que n=1 no permitia) ===")
    rows = []
    for ph, gg in core[core["form"] == "bare"].groupby("phenomenon"):
        for rg in ["strong", "weak", "very_weak"]:
            per_item = gg.assign(x=(gg["rung"] == rg).astype(int)) \
                         .groupby("item_id")["x"].mean()
            rows.append({"phenomenon": ph, "rung": rg, "n_items": len(per_item),
                         "mean": round(per_item.mean(), 3),
                         "sd_between_items": round(per_item.std(ddof=1), 3),
                         "min": round(per_item.min(), 3), "max": round(per_item.max(), 3)})
    q4 = pd.DataFrame(rows)
    print(q4.pivot(index="phenomenon", columns="rung",
                   values=["mean", "sd_between_items"]).reindex(CONTESTED).to_string())
    q4.to_csv(OUT / "quad_q4_between_items.csv", index=False)

    # ---- Q5 contenido vs marca, por peldano ---------------------------------
    print("\n=== Q5  contenido vs marca, para los TRES peldanos ===")
    for rg in ["strong", "weak", "very_weak"]:
        t = core.assign(x=(core["rung"] == rg).astype(int)) \
                .pivot_table(index="phenomenon", columns="form", values="x", aggfunc="mean")
        t["delta"] = t["marked"] - t["bare"]
        print(f"\n  --- {rg} ---")
        print(t.reindex(CONTESTED).round(3).to_string())

    # ---- acuerdo -------------------------------------------------------------
    piv = core.pivot_table(index=["item_id", "gloss"], columns="model",
                           values="rung", aggfunc="first")
    k, n = fleiss(piv)
    agr = [float((piv[a] == piv[b]).mean()) for a, b in combinations(piv.columns, 2)]
    print(f"\n=== acuerdo entre adjudicadores sobre el peldano ===")
    print(f"  Fleiss kappa = {k:.3f}  (n = {n} unidades)   acuerdo bruto = {np.mean(agr):.3f}")
    print("  (con 8 items el estudio previo reporto kappa = 0.358 agregado)")

    print(f"\nescritos CSV en {OUT}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=str(OUT / "raw_quad_bank.jsonl"))
    main(Path(ap.parse_args().raw))
