from enum import Enum


class AuthEnum(Enum):
    AUTH_TOKEN = 'Token'
    HTTP_AUTHORIZATION = 'HTTP_AUTHORIZATION'


class OptionHttpEnum(Enum):
    BODY = 'body'
    DATA = 'data'


class MessageEnum(Enum):
    """
    Clase que lista los mensajes de acceso al API
    """
    USER_NOT_AUTHORIZED = 'Usuario no Autorizado'
    USER_NOT_PERMISSION = 'Usuario no tiene permiso para ejecutar la ' \
                          'funcionalidad'
