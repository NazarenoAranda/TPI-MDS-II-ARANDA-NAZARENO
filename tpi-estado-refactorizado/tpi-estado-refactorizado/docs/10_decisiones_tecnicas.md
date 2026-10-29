## Decisiones técnicas

| ID | Decisión | Alternativas | Justificación |
|---|---|---|---|
| D1 | Python + SQLite + biblioteca estándar | Java/Spring, ORM | Cero dependencias de ejecución; el foco es la calidad del diseño, no el framework |
| D2 | Dos versiones en dos tags (`estado-inicial`, `estado-refactorizado`) | Ramas | Los tags son lo que pide la consigna y fijan el estado exacto para comparar |
| D3 | Pruebas de caracterización con *golden master* por línea de comandos | Solo pruebas unitarias | Congelan el comportamiento externo *antes* de refactorizar; detectan regresiones de texto y de códigos de salida |
| D4 | Mantener comportamientos "raros" de la versión inicial | Corregirlos de paso | Refactoring = cambiar estructura **sin** cambiar comportamiento; las correcciones funcionales irían en otro commit |
| D5 | Patrón repositorio (interfaz + implementación SQLite) | SQL dentro del servicio | Aplica DIP y permite probar sin base de datos |
| D6 | `dataclass(frozen=True)` para entidades y objetos de parámetros | Diccionarios/tuplas | Campos con nombre, inmutabilidad y mejor legibilidad |
| D7 | Reglas de prioridad como datos (`REGLAS_DE_PRIORIDAD`) | `if/elif` | Aplica OCP: nueva regla = nueva entrada |
| D8 | Un único tipo de excepción de negocio (`ErrorDeNegocio`) | Jerarquía de excepciones | Suficiente para el alcance; se captura en un solo punto (CLI) |
| D9 | Datos de demostración sintéticos | Datos reales | La consigna prohíbe datos personales sin consentimiento |
