## 5. Diagnóstico de deuda técnica y code smells

Se identificaron **12 code smells / debilidades técnicas** en la versión inicial (la consigna pide al menos 8). Las ubicaciones son del tag `estado-inicial`. Prioridad: **Alta** = riesgo de errores/seguridad o bloquea la evolución; **Media** = encarece el mantenimiento; **Baja** = limpieza.

| # | Code smell | Ubicación | Prioridad | Refactoring que lo corrige |
|---|---|---|---|---|
| S1 | God Class (clase Dios) | `gestor.py:12-214` | Alta | Extract Class / Move Method (R2, R3) |
| S2 | Long Method + condicionales complejos | `gestor.py:124-165` (`buscar`, CC = 33) | Alta | Extract Method + Move Method (R1, R3) |
| S3 | Código duplicado (validaciones) | `gestor.py:59/131`, `61/135`, `91/127` | Alta | Extract Method / enumeraciones (R1) |
| S4 | SQL armado por concatenación | `gestor.py:67, 84, 139` | Alta | Consultas parametrizadas (R5) |
| S5 | Excepciones tragadas (`except:` desnudo) | `gestor.py:29-30` | Alta | Dejar propagar + `ErrorDeNegocio` (R6) |
| S6 | Lógica mezclada con presentación | `gestor.py` (todos los `return "ERROR..."`) y `main.py:57` | Alta | Separar servicio / presentación (R2) |
| S7 | Números y textos mágicos | `gestor.py:191-197` (plazos 5/15/10/3), `"NUEVA"…` en todo el archivo, `200` | Media | Enum + constantes (R1) |
| S8 | Nombres poco expresivos | `Gestor.q/reg/asig/rep`, función `e`, variables `r, rr, f, c, s, nom` | Media | Rename Method/Variable (R7) |
| S9 | Estado global mutable | `gestor.py:5, 14` (`global DB`) | Media | Inyección de dependencias (R5) |
| S10 | Lista larga de parámetros / obsesión por primitivos | `reg` (7 params), `buscar` (7 params) | Media | Introduce Parameter Object (R4) |
| S11 | Cadena `if/elif` sobre el tipo (viola OCP) | `gestor.py:70-81` (con ramas vacías `pass`), `190-197` | Media | Reglas como datos (R3) |
| S12 | Código muerto | `gestor.py:50-51` (método comentado), `17-18` (`cnt`, `ult` sin usar) | Baja | Remove Dead Code (R8) |

### Detalle de cada smell (evidencia, impacto y riesgo)

**S1 – God Class.** *Evidencia:* una sola clase `Gestor` concentra validación, reglas, SQL, formateo de salida y cálculo del reporte; complejidad de clase C (13). *Impacto:* cualquier cambio toca el mismo archivo; es imposible probar una parte sin las demás. *Riesgo:* alto; cada modificación puede romper funciones no relacionadas.

**S2 – Long Method.** *Evidencia:* `buscar` tiene 42 líneas y complejidad ciclomática **33 (rango E, la peor de todas)**; contiene 3 validaciones, un `for` con 7 filtros y el armado del texto. *Impacto:* difícil de leer y casi imposible de cubrir con pruebas unitarias. *Riesgo:* alto; agregar un filtro nuevo añade más ramas.

**S3 – Código duplicado.** *Evidencia:* la misma condición `tipo != "CERTIFICADO" and tipo != … ` aparece en `reg` (línea 59) y en `buscar` (línea 131); la de prioridad en 61 y 135; la de estado en 91 y 127. *Impacto:* si cambia un valor válido hay que corregirlo en varios lugares. *Riesgo:* alto; olvidar uno produce comportamiento inconsistente entre comandos.

**S4 – SQL por concatenación.** *Evidencia:* `"... WHERE legajo = '" + e(legajo) + "'"`. Se usa una función de escape manual (`e`) y algunos campos (`fecha`, `tipo`, `prioridad`) se concatenan **sin** escapar, confiando en validaciones previas. *Impacto:* vulnerabilidad de inyección SQL latente y consultas frágiles. *Riesgo:* alto (seguridad); basta un campo nuevo sin escapar.

**S5 – Excepciones tragadas.** *Evidencia:* `except:` sin tipo devuelve `None` (línea 29). Comprobado: `g.q('SELECT * FROM tabla_inexistente', True)` devuelve `None` **sin ningún error visible**. *Impacto:* los fallos de base de datos se disfrazan de "no se encontró" o "no se pudo registrar". *Riesgo:* alto; errores silenciosos y difíciles de depurar.

**S6 – Lógica mezclada con presentación.** *Evidencia:* los métodos devuelven textos listos para imprimir y los errores se distinguen con `res.startswith("ERROR")` (`main.py:57`). *Impacto:* no se puede reutilizar la lógica en otra interfaz ni probar reglas sin comparar textos. *Riesgo:* alto para la evolución (web, API).

**S7 – Valores mágicos.** *Evidencia:* plazos `5, 15, 10, 3` dentro de `rep`; estados y tipos como cadenas repetidas; límite `200` incrustado. *Impacto:* errores de tipeo no detectables por el intérprete. *Riesgo:* medio.

**S8 – Nombres poco expresivos.** *Evidencia:* `q`, `reg`, `asig`, `rep`, `e`, `r`, `rr`, `f`, `nom`. *Impacto:* hay que leer el cuerpo para saber qué hace cada cosa. *Riesgo:* medio (legibilidad, incorporación de nuevos integrantes).

**S9 – Estado global mutable.** *Evidencia:* `global DB` reasigna una variable de módulo desde el constructor. *Impacto:* dos instancias con bases distintas se pisan entre sí; pruebas con efectos cruzados. *Riesgo:* medio.

**S10 – Lista larga de parámetros.** *Evidencia:* `reg(legajo, tipo, prioridad, descripcion, canal, creado_por, fecha)` y `buscar` con 7 parámetros. *Impacto:* llamadas propensas a errores de orden; cada dato nuevo cambia la firma. *Riesgo:* medio.

**S11 – Cadena `if/elif` sobre el tipo.** *Evidencia:* ramas para CERTIFICADO y EQUIVALENCIA que solo contienen `pass`, y otra cadena para los plazos. *Impacto:* viola el principio abierto/cerrado: cada tipo nuevo exige editar código existente. *Riesgo:* medio.

**S12 – Código muerto.** *Evidencia:* método `listar_todo` comentado, atributos `cnt` y `ult` que nunca se usan. *Impacto:* confunde al lector. *Riesgo:* bajo.

### Orden de corrección sugerido
1.º **S5 y S4** (errores silenciosos y seguridad) → 2.º **S1, S2, S3, S6** (estructura) → 3.º **S7, S9, S10, S11** (diseño) → 4.º **S8, S12** (limpieza). Se aplicó en este orden de impacto, no de comodidad.
