from django.shortcuts import render
from django.core.paginator import Paginator

def api_paginacion(queryset, page=None, numero_items_por_pagina=None):
    '''
    Retorna lista de objetos segun la paginación requerida
    :param queryset: sql del ORM a ejecutar
    :param page: número de página
    :param numero_items_por_pagina: número de objetos a retornar
    :return: lista de objetos
    '''
    try:
        paginator = Paginator(queryset, numero_items_por_pagina)
        queryset = paginator.page(page)
    except Exception as e:
        print(e)
    return queryset
