# Las tres versiones — listas, y ninguna cuesta dinero

**Regla que no se salta:** una revista a la vez. Estas versiones existen para que el día que
llegue un rechazo el reenvío salga en horas, no en semanas. Enviar en paralelo es envío
duplicado, y cambiar el título no lo cambia.

## Coste: verificado, cero en las tres

| Orden | Revista | Modelo | Qué cuesta |
|---|---|---|---|
| **1** | Behavior Research Methods (Springer) | híbrida | **0 €** por la vía de suscripción. El APC de £2.690 / $4.090 / €3.090 es **opcional** y solo si quieres acceso abierto; se elige *después* de la aceptación |
| **2** | Information Processing & Management (Elsevier) | híbrida | **0 $** por la vía de suscripción. APC de $3.720 solo si eliges OA |
| **3** | Journal of AI Research (JAIR) | **diamante** | **0**. No cobra nada, nunca. Sin APC y sin cuota de envío |

**Cuidado con el paso de la aceptación.** En BRM y en IP&M el formulario te ofrece el acceso
abierto *después* de que te acepten, y está diseñado para que digas que sí. Si no quieres pagar,
ahí hay que elegir explícitamente la vía de suscripción. El artículo se publica igual; lo único
que cambia es que queda tras el muro de pago, y el preprint en el repositorio sigue siendo libre.

## Descartada por cobrar

**Natural Language Processing** (Cambridge, la antigua *Natural Language Engineering*) era la
tercera opción hasta que verifiqué la tarifa: desde 2024 es **oro completo**, con APC obligatorio
de **£2.610 / $3.655**. No hay vía de suscripción. Cambridge tiene exenciones y descuentos por
equidad, pero hay que solicitarlos y no están garantizados. Queda como suplente de pago si algún
día hay financiación; mientras tanto, JAIR ocupa su lugar y no cuesta nada.

---

## Orden de disparo

```
1. Behavior Research Methods   ← el envío actual
2. Information Processing & Mgmt  ← si BRM rechaza
3. JAIR                           ← si IP&M rechaza
```

Antes de cada reenvío: retirada formal en el portal anterior o rechazo por escrito, y actualizar
en la carta la frase de *"not under consideration elsewhere"*.

---

## Versión 1 — Behavior Research Methods

Carpeta `brm_submission/`. Manuscrito, carta al editor, abstract de 249 palabras para el
formulario y la hoja con todos los campos. Encaje: psicometría aplicada a un tipo nuevo de
respondente.

## Versión 2 — Information Processing & Management

`alternates/main_ipm.pdf`, abstract en `abstract_IPM.txt`.

**Título:** *When the Instrument Produces the Score: Item Sampling, Instruction Framing and
Threshold Placement in LLM-Based Evaluation*

El encuadre pasa de psicometría a tuberías de evaluación: su lector despliega un juez LLM y
hereda estas tres decisiones sin saberlo. El muestreo de ítems se presenta como dimensionar un
banco de pruebas. El párrafo *What is not new* se apoya en la literatura de evaluación de LLM en
vez de en Cronbach.

## Versión 3 — JAIR

`alternates/main_nlp.pdf`, abstract en `abstract_NLP_Cambridge.txt` (el nombre del fichero
conserva el destino original; el contenido sirve igual para JAIR, que es la misma comunidad).

**Título:** *How Much of an Elicited Evaluation Is the Protocol? Three Measured Artifacts and the
Design Rules They Imply*

Lidera con el umbral y la instrucción, que es lo que esa comunidad reconoce como suyo, y se
posiciona como continuación de la línea de sensibilidad al prompt y fiabilidad de jueces.
**El cuerpo NO está reordenado**: las secciones siguen el orden de la versión BRM. Reordenarlas
exige reescribir transiciones y referencias cruzadas, y es una decisión que conviene tomar si un
revisor lo pide, no antes.

JAIR no tiene límite estricto de longitud y valora el material reproducible, así que el
repositorio juega a favor igual que en BRM.

---

## Lo que NO cambia entre versiones

Datos, números, figuras, reglas de diseño y declaraciones. Cambian el título, el resumen y un
párrafo de encuadre. Las tres se generan de `paper/main.tex` con `build_variants.py`, así que
cualquier corrección se propaga con un comando y no pueden divergir.

## Si lo que quieres es más papers, no más envíos del mismo

La vía legítima es una contribución distinta. El candidato real es la **familia II sola**: 1.800
elicitaciones sobre confianza factual, la calibración por constructo, y el hallazgo de que
binarizar en 0,9 destruye la única señal del banco. Tiene su propia pregunta y su propio público.
Habría que decidirlo antes de enviar este, para declarar la relación en las dos cartas.
