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


def format_timezone_to_date(fecha):
    if fecha is not None:
        index = fecha.find("T")
        return fecha[:index] if index > -1 else fecha


def verificar(nro):
    l = len(nro)

    if l == 10 or l == 13:  # verificar la longitud correcta
        cp = int(nro[0:2])
        if cp >= 1 and cp <= 22:  # verificar codigo de provincia
            tercer_dig = int(nro[2])
            if tercer_dig >= 0 and tercer_dig < 6:  # numeros enter 0 y 6
                if l == 10:
                    return __validar_ced_ruc(nro, 0)
                elif l == 13:
                    return __validar_ced_ruc(nro, 0) and nro[
                                                         10:13] != '000'  # se verifica q los ultimos numeros no sean 000
            elif tercer_dig == 6:
                return __validar_ced_ruc(nro, 1)  # sociedades publicas
            elif tercer_dig == 9:  # si es ruc
                return __validar_ced_ruc(nro, 2)  # sociedades privadas
            else:
                return False
                #raise Exception(u'Tercer digito invalido')
        else:
            return False
            #raise Exception(u'Codigo de provincia incorrecto')
    else:
        return False
        #raise Exception(u'Longitud incorrecta del numero ingresado')


def __validar_ced_ruc(nro, tipo):
    total = 0
    if tipo == 0:  # cedula y r.u.c persona natural
        base = 10
        d_ver = int(nro[9])  # digito verificador
        multip = (2, 1, 2, 1, 2, 1, 2, 1, 2)
    elif tipo == 1:  # r.u.c. publicos
        base = 11
        d_ver = int(nro[8])
        multip = (3, 2, 7, 6, 5, 4, 3, 2)
    elif tipo == 2:  # r.u.c. juridicos y extranjeros sin cedula
        base = 11
        d_ver = int(nro[9])
        multip = (4, 3, 2, 7, 6, 5, 4, 3, 2)
    for i in range(0, len(multip)):
        p = int(nro[i]) * multip[i]
        if tipo == 0:
            total += p if p < 10 else int(str(p)[0]) + int(str(p)[1])
        else:
            total += p
    mod = total % base
    val = base - mod if mod != 0 else 0
    return val == d_ver
