# Behavior Research Methods — hoja de envío

**Revista:** Behavior Research Methods (Springer, Psychonomic Society)
**IF 5,0 · Q1 · ISSN 1554-3528 · portal Editorial Manager**
**Tipo:** Article

---

## Ficheros de esta carpeta

| Fichero | Para qué |
|---|---|
| `Leyva-Vazquez_ThreeWays_BRM_manuscript.pdf` | el manuscrito, 14 pp |
| `abstract_plain.txt` | 249 palabras, para pegar en el formulario |
| `COVER_LETTER.md` | carta al editor |

---

## Campos del formulario

**Título**
```
Three Ways an Elicited Evaluation Measures Its Own Design
```
Subtítulo, si el formulario lo admite: *Item sampling, instruction effects, and threshold
artifacts, with a worked case and 7,920 elicitations*

**Autor único y de correspondencia**

Maikel Y. Leyva-Vázquez · `myleyvav@ube.edu.ec` · ORCID `0000-0001-7911-5879` (verificado)
Universidad Bernardo O'Higgins, Santiago, Chile
Universidad Bolivariana del Ecuador, Guayaquil, Ecuador
Universidad de Guayaquil, Guayaquil, Ecuador

**Palabras clave**
```
elicited evaluation; measurement validity; large language models; item sampling;
verbalized confidence; LLM-as-a-judge; threshold artifacts; reproducibility
```

**Declaraciones** — ya están escritas en el manuscrito, sección *Declarations*: ética y sujetos
humanos (ninguno), uso de modelos de lenguaje, conflictos de interés, financiación (ninguna).

**Disponibilidad de datos**
```
Both item banks, all 7,920 raw generations including response text, the elicitation and
analysis scripts, and the code producing every figure and table are available at
https://github.com/mleyvaz/elicited-evaluation-design — code under MIT, banks and
generations under CC BY 4.0.
```

---

## Lo que BRM exige y ya se cumple

- **Abstract ≤ 250 palabras.** Estaba en 399 y se reescribió a **249**. No es un recorte: es otro
  abstract, con las mismas cifras titulares y sin el detalle numérico secundario.
- **Sin sujetos humanos.** Cero encuestas, entrevistas, anotadores o datos personales. Declarado
  explícitamente en el manuscrito.
- **Secciones apropiadas al contenido** (APA admite estructura temática cuando no hay un
  experimento único). Las siete secciones van de problema → corpus → tres resultados → acuerdo →
  réplica → límites.
- **Material abierto.** BRM valora esto mucho: los dos bancos, las 7.920 generaciones con el
  texto de respuesta, y el código de cada figura.

## Lo que NO hace falta ahora

**No hay que pasar el paper a plantilla Springer ni convertir las referencias a APA.** Springer
Nature acepta **formato libre en la primera vuelta**; el estilo exacto solo se exige si piden
revisión. El paper usa `plainnat`, que ya da citas autor-año. Si lo aceptan, entonces se
convierte — y ahí hará falta instalar `apacite`, que hoy no está en el TinyTeX de esta máquina y
requiere actualizar `tlmgr` primero.

---

## Antes de enviar

1. ~~Subir el repo.~~ **Hecho**: `github.com/mleyvaz/elicited-evaluation-design` está público
   con los dos bancos, las 7.920 generaciones, los scripts y el código de cada figura.
2. **Revisores sugeridos.** El formulario los pide. Los candidatos naturales salen de la propia
   bibliografía —los autores del trabajo sobre sensibilidad al protocolo y del de fiabilidad de
   jueces LLM—, pero elígelos tú: no conviene proponer a nadie con quien haya relación.
3. **Decidir tipo de artículo.** Va como *Article*. BRM tiene además una convocatoria de
   *Tutorial papers* para «best practices for reproducible experimental design» y prácticas de
   ciencia abierta, y el paper encaja ahí porque cada sección cierra con una regla. Pero es
   empírico antes que didáctico —7.920 elicitaciones— así que *Article* es lo correcto. Si
   rechazan por alcance, reencuadrarlo como Tutorial es la segunda bala.

## Coste

**Publicar aquí no cuesta nada** si eliges la vía de suscripción. BRM es híbrida: tras la
aceptación el formulario ofrece acceso abierto por £2.690 / $4.090 / €3.090, y está diseñado
para que digas que sí. Es opcional. Elegir suscripción deja el artículo tras muro de pago, pero
el preprint del repositorio sigue abierto para todos.

## Si BRM rechaza

El plan completo, con las tarifas verificadas de las tres, está en `../alternates/READY_TO_FIRE.md`.

- **Information Processing & Management** (Elsevier, IF 6,9, Q1) — híbrida, gratis por
  suscripción. Más impacto, peor encaje.
- **JAIR** (IF 4,0) — diamante, no cobra nada nunca.

*Natural Language Processing* (Cambridge) se descartó: pasó a oro completo en 2024 con APC
obligatorio de £2.610 y sin vía de suscripción.
