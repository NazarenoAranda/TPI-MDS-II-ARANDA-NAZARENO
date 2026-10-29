# Gestión de Solicitudes Académicas — VERSIÓN INICIAL (`estado-inicial`)

Trabajo Práctico Integrador — **Metodología de Sistemas II** · Tecnicatura Universitaria en Programación a Distancia (UTN)
Autor: Nazareno Aranda · Comisión 6

> ⚠️ Esta es la **versión base**. Funciona correctamente desde el punto de vista del usuario, pero contiene **problemas de diseño e implementación intencionales** (code smells y deuda técnica) que se diagnostican y corrigen en la versión `estado-refactorizado`.

## Descripción
Módulo de línea de comandos para registrar solicitudes de estudiantes (certificados, equivalencias, reincorporaciones, consultas), clasificarlas por tipo, prioridad y estado, asignar un responsable, buscar/filtrar y generar un reporte básico. Los datos son **sintéticos**.

## Instalación y uso
Requisitos: Python 3.10 o superior (no requiere instalar paquetes).
```bash
python main.py init-demo
python main.py registrar --legajo 1001 --tipo CERTIFICADO --prioridad MEDIA --descripcion "Certificado de alumno regular"
python main.py asignar --id 1 --responsable 1
python main.py cambiar-estado --id 1 --estado RESUELTA
python main.py buscar --estado RESUELTA
python main.py reporte
```
(En algunos sistemas el comando es `python3`.) Ayuda: `python main.py --help`.

## Funcionalidades
`init-demo`, `registrar`, `cambiar-estado`, `asignar`, `buscar` (por estado, tipo, prioridad, legajo, texto, sin responsable, responsable) y `reporte`.

## Pruebas
```bash
python -m unittest discover -s tests -v
```
Son pruebas de **caracterización** (*golden master*): `tests/golden/` guarda la salida exacta de esta versión y sirve de referencia para comprobar que el refactoring no altera el comportamiento externo.

## Tecnologías
Python 3 · SQLite · argparse · unittest.

## Estructura
```
gestor.py   Toda la lógica del sistema en una sola clase (Gestor)
main.py     Interfaz de línea de comandos
tests/      Escenarios y archivos golden
```
