"""Errores del dominio."""


class ErrorDeNegocio(Exception):
    """Se viola una regla del negocio (dato invalido, entidad inexistente, transicion no permitida).

    El mensaje es el que se le muestra al usuario, sin el prefijo 'ERROR:'.
    """
