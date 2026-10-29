## 10. Conclusiones y mejoras futuras

### 10.1 Conclusiones grupales / generales

- **Funcionar no es lo mismo que estar bien construido.** La versión inicial pasa todas las pruebas funcionales y, sin embargo, tiene complejidad ciclomática 33 en una función, SQL concatenado y errores silenciosos. La calidad interna es invisible desde la interfaz pero condiciona el costo de cada cambio.
- **Primero las pruebas, después el refactoring.** Las pruebas de caracterización (*golden master*) permitieron refactorizar con confianza y detectaron una regresión real (concordancia de género en un mensaje) que se habría escapado a simple vista.
- **SOLID se justifica con ejemplos concretos, no con dogma.** OCP, DIP y SRP mostraron valor medible: agregar un tipo de solicitud pasó de editar 5 lugares a editar 1, y las reglas de negocio ahora se prueban sin base de datos.
- **Las métricas ayudan a priorizar, pero no reemplazan el criterio.** radon y flake8 señalaron dónde mirar (complejidad 11,18 → 2,33; avisos 9 → 0); la decisión de qué refactorizar primero (seguridad y errores silenciosos) fue de diseño.

### 10.2 Dificultades y límites del trabajo

- Preservar **exactamente** los mensajes y el orden de las validaciones obligó a leer con detalle el comportamiento de la versión inicial.
- Es un módulo pequeño: algunas decisiones (patrón repositorio, objetos de parámetros) serían excesivas en un script descartable, pero se justifican por el objetivo académico y por la evolución esperada.
- Las pruebas de caracterización fijan también los comportamientos "raros" de la versión inicial (p. ej. se puede volver a `NUEVA` desde `EN_PROCESO`); se respetaron para no alterar el comportamiento externo.

### 10.3 Mejoras pendientes
Filtrar en SQL en lugar de en memoria (O5); reemplazar la cadena de guardas de `coincide` por una lista de predicados (O4); despachar comandos con un diccionario (O7); agregar una interfaz web o API reutilizando `ServicioSolicitudes`; incorporar integración continua (GitHub Actions) que ejecute pruebas y flake8; modelar explícitamente la máquina de estados.

### 10.4 Relación con los contenidos de la asignatura
Calidad externa vs. interna (§4), deuda técnica y code smells (§5), SOLID y Clean Code (§6), refactoring seguro (§7), pruebas de caracterización (§8) y code review con checklist (§9).

### 10.5 Conclusión individual
**Nazareno Aranda:** `Lo que más me costó entender fue el manejo y la sincronización inicial de las pruebas de caracterización (golden master) para asegurar que ningún comportamiento legado se alterara al modificar la estructura del código. El refactoring más valioso me pareció la separación entre la lógica de negocio y la presentación, ya que rompió con el acoplamiento original y permitió aislar las reglas para testearlas sin depender de la base de datos. Si tuviera que hacer algo distinto, habría establecido las abstracciones del repositorio y los objetos de parámetros desde las primeras iteraciones del diseño para evitar refactorizar sobre código fuertemente acoplado a SQLite.`
