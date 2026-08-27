# Versiones alternativas — listas, en espera

**Regla que no se salta:** solo una revista a la vez. Estas dos versiones existen para que el
día que llegue un rechazo de BRM el reenvío salga en horas, no en semanas. No se envían en
paralelo: eso es envío duplicado, y cambiar el título no lo cambia.

**Orden de disparo**

```
1. Behavior Research Methods      ← enviado / en curso
2. Information Processing & Mgmt  ← si BRM rechaza
3. Natural Language Processing    ← si IP&M rechaza
```

Antes de reenviar, dos cosas: retirar formalmente en el portal anterior (o tener el rechazo por
escrito), y actualizar en la carta la frase de "not under consideration elsewhere".

---

## Versión 2 — Information Processing & Management

Encaje: su público construye y evalúa sistemas, no instrumentos psicométricos. El paper se
vende como fiabilidad de una tubería de evaluación, no como validez de una medida.

**Título**
```
When the Instrument Produces the Score: Item Sampling, Instruction Framing and
Threshold Placement in LLM-Based Evaluation
```

**Qué cambia respecto de la versión BRM**

- El marco de la introducción pasa de psicometría a *evaluation pipelines*: quien despliega un
  juez LLM en producción hereda estas tres decisiones sin saberlo.
- El párrafo *What is not new* deja de apoyarse en Cronbach y se apoya en la literatura de
  evaluación de LLM, que es la que su revisor conoce.
- La regla de los ítems se presenta como dimensionamiento de un banco de pruebas, no como
  precisión de un instrumento.
- El apartado de validez de constructo se acorta: allí no es la objeción principal.

**Abstract** — en `abstract_IPM.txt`. Sin límite de 250 estricto; IP&M admite más holgura.

---

## Versión 3 — Natural Language Processing (Cambridge)

Encaje: comunidad de PLN. Aquí lo que vende es LLM-as-a-judge y la sensibilidad al prompt.

**Título**
```
How Much of an Elicited Evaluation Is the Protocol? Three Measured Artifacts and the
Design Rules They Imply
```

**Qué cambia**

- **El abstract** lidera con el umbral y la instrucción, que son los que esa comunidad reconoce
  como suyos, y deja el muestreo de ítems en tercer lugar. **El cuerpo NO está reordenado**: sus
  secciones siguen en el orden de la versión BRM. Reordenarlas exige reescribir las transiciones
  y las referencias cruzadas, y es una decisión que conviene tomar viendo si el revisor lo pide,
  no antes.
- Se cita explícitamente el trabajo de sensibilidad al protocolo y el de fiabilidad de jueces
  como el hilo que este paper continúa.
- El vocabulario psicométrico (*between-item variance*, *construct validity*) se traduce a
  *benchmark design* y *prompt sensitivity* donde no pierda precisión.

**Ojo con el APC:** es open access completo desde 2024. Pregunta el importe antes de enviar.

---

## Lo que NO cambia en ninguna versión

Los datos, los números, las figuras, las reglas de diseño y las declaraciones. Cambia el
encuadre y el orden de presentación, no el contenido. Si cambiara el contenido serían papers
distintos y habría que preguntarse si eso es honesto; no lo son, y por eso van en serie.

## Si lo que quieres es más papers, no más envíos del mismo

La vía legítima es una contribución distinta, no un reempaquetado. El candidato real es la
**familia II sola**: 1.800 elicitaciones sobre confianza factual, con la calibración por
constructo y el hallazgo de que binarizar en 0,9 destruye la única señal del banco. Eso es un
paper de calibración con su propia pregunta y su propio público, y no repite las conclusiones
de este. Habría que decidirlo antes de enviar este, para poder declarar la relación en las dos
cartas.
