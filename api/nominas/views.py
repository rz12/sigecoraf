import datetime
import json

from django.db.models import Q
from django.utils.decorators import method_decorator
from rest_framework import status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from api.nominas.serializers import RolPagoSerializer, \
    CargoSerializer, ContratoSerializer, ConsolidadRolPagoSerializer, \
    EmpleadoSerializer, DetalleRolPagoSerializer
from api.seguridad.permissions import IsAuthenticated
from app.master.models import Parametrizacion
from app.master.views import *
from app.nominas.models import Empleado, RolPago, Cargo, Contrato, \
    ConsolidadoRolPago, DetalleRolPago, EstructuraDetalleRolPago


class EmpleadoViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            objeto = Empleado.objects.get(id=pk)
            empleado = EmpleadoSerializer(objeto).data
            return Response({'data': empleado, 'status': status.HTTP_200_OK,
                             'message': None})
        except Empleado.DoesNotExist:
            return Response({'data': None, 'status': status.HTTP_404_NOT_FOUND,
                             'message': None})

    @method_decorator(IsAuthenticated())
    def list(self, request):
        page = request.GET.get('PAGE')
        items_per_page = request.GET.get('PAGE_SIZE')
        filter = request.GET.get('FILTER')
        queryset = Empleado.objects.all()
        count = queryset.count();
        if filter is not None:
            queryset = queryset.filter(
                Q(primer_nombre__icontains=filter) | Q(
                    primer_apellido__icontains=filter) | Q(
                    numero_identificacion__icontains=filter))
        queryset_pagination = api_paginacion(queryset, int(page),
                                             items_per_page)

        serializer = EmpleadoSerializer(queryset_pagination, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None, 'count': count})

    def create(self, request):
        try:
            empleado = Empleado()
            request.data['fecha_inicio'] = format_timezone_to_date(
                request.data['fecha_inicio'])
            request.data['fecha_nacimiento'] = format_timezone_to_date(
                request.data['fecha_nacimiento'])
            if "fecha_fin" in request.data:
                request.data['fecha_fin'] = format_timezone_to_date(
                    request.data['fecha_fin'])

            if "fecha_ingreso_iess" in request.data:
                request.data['fecha_ingreso_iess'] = format_timezone_to_date(
                    request.data['fecha_ingreso_iess'])

            if request.data['tipo_documento_identificacion'][
                'codigo'] == 'CEDULA' or \
                    request.data['tipo_documento_identificacion'][
                        'codigo'] == 'RUC':

                if verificar(request.data['numero_identificacion']) is False:
                    return Response({'data': None,
                                     'status': status.HTTP_400_BAD_REQUEST,
                                     'message': 'Número de Identificación Incorrecto'})

            empleado.tipo_documento_identificacion_id = \
                request.data['tipo_documento_identificacion']['id']
            empleado.genero_id = request.data['genero']['id']
            empleado.estado_civil_id = request.data['estado_civil']['id']
            empleado.empresa_id = request.data['empresa']['id']
            serializer = EmpleadoSerializer(empleado, data=request.data)
            if serializer.is_valid():
                serializer.save()
                empleado_message = 'Empleado Creado Satisfactoriamente.'
                empleado_status = status.HTTP_200_OK
            else:
                empleado_message = json.dumps(serializer.errors)
                empleado_status = status.HTTP_400_BAD_REQUEST

            return Response({'data': serializer.data,
                             'status': empleado_status,
                             'message': empleado_message})

        except Exception as e:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': e})

    def update(self, request, pk=None):
        try:
            empleado = Empleado.objects.get(id=pk)
            request.data['fecha_inicio'] = format_timezone_to_date(
                request.data['fecha_inicio'])

            request.data['fecha_nacimiento'] = format_timezone_to_date(
                request.data['fecha_nacimiento'])
            if "fecha_fin" in request.data:
                request.data['fecha_fin'] = format_timezone_to_date(
                    request.data['fecha_fin'])

            if "fecha_ingreso_iess" in request.data:
                request.data['fecha_ingreso_iess'] = format_timezone_to_date(
                    request.data['fecha_ingreso_iess'])

            if request.data['tipo_documento_identificacion'][
                'codigo'] == 'CEDULA' or \
                    request.data['tipo_documento_identificacion'][
                        'codigo'] == 'RUC':

                if verificar(request.data['numero_identificacion']) is False:
                    return Response({'data': None,
                                     'status': status.HTTP_400_BAD_REQUEST,
                                     'message': 'Número de Identificación Incorrecto'})

            empleado.tipo_documento_identificacion_id = \
                request.data['tipo_documento_identificacion']['id']
            empleado.genero_id = request.data['genero']['id']
            empleado.estado_civil_id = request.data['estado_civil']['id']
            empleado.empresa_id = request.data['empresa']['id']
            serializer = EmpleadoSerializer(empleado, data=request.data)
            if serializer.is_valid():
                serializer.save()
                empleado_message = 'Empleado Actualizado Satisfactoriamente.'
                empleado_status = status.HTTP_200_OK
            else:
                empleado_message = json.dumps(serializer.errors)
                empleado_status = status.HTTP_400_BAD_REQUEST

            return Response({'data': serializer.data,
                             'status': empleado_status,
                             'message': empleado_message})

        except Exception as e:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': e})


class RolPagoViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            objeto = RolPago.objects.get(id=pk)
            rolPago = RolPagoSerializer(objeto).data
            return Response({'data': rolPago, 'status': status.HTTP_200_OK,
                             'message': None})
        except RolPago.DoesNotExist:
            return Response({'data': None, 'status': status.HTTP_404_NOT_FOUND,
                             'message': None})

    def list(self, request):
        queryset = RolPago.objects.all()
        count = queryset.count();
        serializer = RolPagoSerializer(queryset, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None, 'count': count})

    @list_route()
    def list_by_consolidado(self, request):
        consolidado = None
        if 'CONSOLIDADO_ROLPAGO' in request.GET:
            consolidado = request.GET['CONSOLIDADO_ROLPAGO']

        queryset = RolPago.objects.filter(consolidado_rolpago=consolidado).all()
        count = queryset.count();
        serializer = RolPagoSerializer(queryset, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None, 'count': count})

    def create(self, request):
        try:
            rolPago = RolPago()
            serializer = RolPagoSerializer(rolPago, data=request.data)
            if serializer.is_valid():
                serializer.save()
                rolPago_message = 'Cargo creado'
                rolPago_status = status.HTTP_200_OK
            else:
                rolPago_message = serializer.errors
                rolPago_status = status.HTTP_400_BAD_REQUEST

            return Response({'data': serializer.data,
                             'status': rolPago_status,
                             'message': rolPago_message})

        except Exception as e:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': e})

    def update(self, request, pk=None):
        try:
            rolPago = RolPago.objects.get(id=pk)
            serializer = RolPagoSerializer(rolPago, data=request.data)
            if serializer.is_valid():
                serializer.save()
                rolPago_message = 'RolPago actualizado'
                rolPago_status = status.HTTP_200_OK
            else:
                rolPago_message = serializer.errors
                rolPago_status = status.HTTP_400_BAD_REQUEST

            return Response({'data': serializer.data,
                             'status': rolPago_status,
                             'message': rolPago_message})

        except Exception as e:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': e})

    @detail_route(methods=['put'])
    def update_with_detalles(self, request, pk=None):
        try:

            rol_pago = RolPago.objects.get(id=pk)
            detalles = request.data['detalles']
            serializer = RolPagoSerializer(rol_pago, data=request.data)
            for detalle in detalles:
                detalle_rolpago = DetalleRolPago.objects.get(id=detalle['id'])
                serializer_detalle=DetalleRolPagoSerializer(detalle_rolpago,data=detalle)
                if serializer_detalle.is_valid():
                    serializer_detalle.save()

            if serializer.is_valid():
                serializer.save()

                rolpago_message = 'Rol de Pago actualizado Satisfactoriamente.'
                rolpago_status = status.HTTP_200_OK
            else:
                rolpago_message = json.dumps(serializer.errors)
                rolpago_status = status.HTTP_400_BAD_REQUEST
            return Response({'data': serializer.data,
                             'status': rolpago_message,
                             'message': rolpago_status})

        except Exception as e:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': e})

    @detail_route(methods=['post'])
    def create_by_consolidado_rolpago(self, request, pk=None):
        empresa = request.GET.get("EMPRESA")

        consolidado_rolpago = request.GET.get("CONSOLIDADO_ROLPAGO")
        queryset = Contrato.objects.filter(empleado__empresa=empresa,
                                           estado=True).all()

        contratos_by_consolidados = Contrato.objects.filter(
            roles_pago__consolidado_rolpago=consolidado_rolpago).all()
        queryset_difference = list(
            set(queryset).difference(contratos_by_consolidados))
        roles_pago = []

        for contrato in queryset_difference:
            rol_pago = RolPago()
            rol_pago.contrato = contrato
            rol_pago.fecha_inicio = datetime.date.today
            rol_pago.total = 0.0
            rol_pago.consolidado_rolpago_id = consolidado_rolpago
            rol_pago.save()
            roles_pago.append(rol_pago)
        serializer = RolPagoSerializer(roles_pago, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None, "count": len(roles_pago) + len(
                contratos_by_consolidados)})


class CargoViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            objeto = Cargo.objects.get(id=pk)
            cargo = CargoSerializer(objeto).data
            return Response({'data': cargo, 'status': status.HTTP_200_OK,
                             'message': None})
        except Cargo.DoesNotExist:
            return Response({'data': None, 'status': status.HTTP_404_NOT_FOUND,
                             'message': None})

    @method_decorator(IsAuthenticated())
    def list(self, request):
        page = request.GET.get('PAGE')
        items_per_page = request.GET.get('PAGE_SIZE')
        filter = request.GET.get('FILTER')
        queryset = Cargo.objects.all().order_by('nombre')
        count = queryset.count();
        if filter is not None:
            queryset = queryset.filter(
                Q(nombre__icontains=filter) | Q(descripcion__icontains=filter))
        queryset_pagination = api_paginacion(queryset, int(page),
                                             items_per_page)

        serializer = CargoSerializer(queryset_pagination, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'count': count, 'message': None})

    def create(self, request):
        try:
            cargo = Cargo()
            cargo.empresa_id = request.data['empresa']['id']
            serializer = CargoSerializer(cargo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                cargo_message = 'Cargo creado satisfactoriamente.'
                cargo_status = status.HTTP_200_OK
            else:
                cargo_message = serializer.errors
                cargo_status = status.HTTP_400_BAD_REQUEST

            return Response({'data': serializer.data,
                             'status': cargo_status,
                             'message': cargo_message})

        except Exception as e:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': e})

    def update(self, request, pk=None):
        try:
            cargo = Cargo.objects.get(id=pk)
            cargo.empresa_id = request.data['empresa']['id']
            serializer = CargoSerializer(cargo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                cargo_message = 'Cargo actualizado Satisfactoriamente.'
                cargo_status = status.HTTP_200_OK
            else:
                cargo_message = serializer.errors
                cargo_status = status.HTTP_400_BAD_REQUEST

            return Response({'data': serializer.data,
                             'status': cargo_status,
                             'message': cargo_message})

        except Exception as e:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': e})


class ContratoViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            objeto = Contrato.objects.get(id=pk)
            contrato = ContratoSerializer(objeto).data
            return Response({'data': contrato, 'status': status.HTTP_200_OK,
                             'message': None})
        except Contrato.DoesNotExist:
            return Response({'data': None, 'status': status.HTTP_404_NOT_FOUND,
                             'message': None})

    @method_decorator(IsAuthenticated())
    def list(self, request):

        page = request.GET.get('PAGE')
        items_per_page = request.GET.get('PAGE_SIZE')
        filter = request.GET.get('FILTER')
        queryset = Contrato.objects.all().order_by('fecha_inicio',
                                                   'empleado__primer_apellido')
        count = queryset.count();
        if filter is not None:
            queryset = queryset.filter(
                Q(empleado__primer_nombre__icontains=filter) | Q(
                    empleado__primer_apellido__icontains=filter) | Q(
                    empleado__numero_identificacion__icontains=filter))
        queryset_pagination = api_paginacion(queryset, int(page),
                                             items_per_page)
        serializer = ContratoSerializer(queryset_pagination, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None, 'count': count})

    def create(self, request):
        try:
            contrato = Contrato()
            request.data['fecha_inicio'] = format_timezone_to_date(
                request.data['fecha_inicio'])
            if "fecha_fin" in request.data:
                request.data['fecha_fin'] = format_timezone_to_date(
                    request.data['fecha_fin'])
            contratos_empleado_vigentes = Contrato.objects.filter(
                empleado__id=request.data['empleado']['id'], estado=True).all()
            if contratos_empleado_vigentes.count() > 0:
                return Response({'data': None,
                                 'status': status.HTTP_400_BAD_REQUEST,
                                 'message': "El empleado ya tiene un contrato"})
            contrato.empleado_id = request.data['empleado']['id']
            contrato.cargo_id = request.data['cargo']['id']
            serializer = ContratoSerializer(contrato, data=request.data)
            if serializer.is_valid():
                serializer.save()
                contrato_message = 'Contrato creado satisfactoriamente'
                contrato_status = status.HTTP_200_OK
            else:
                contrato_message = serializer.errors
                contrato_status = status.HTTP_400_BAD_REQUEST
            return Response({'data': serializer.data,
                             'status': contrato_status,
                             'message': contrato_message})
        except Exception as e:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': e})

    def update(self, request, pk=None):
        try:
            contrato = Contrato.objects.get(id=pk)
            request.data['fecha_inicio'] = format_timezone_to_date(
                request.data['fecha_inicio'])

            if "fecha_fin" in request.data:
                request.data['fecha_fin'] = format_timezone_to_date(
                    request.data['fecha_fin'])
            contrato.empleado_id = request.data['empleado']['id']
            contrato.cargo_id = request.data['cargo']['id']
            serializer = ContratoSerializer(contrato, data=request.data)
            if serializer.is_valid():
                serializer.save()
                contrato_message = 'Contrato Actualizado Satisfactoriamente.'
                contrato_status = status.HTTP_200_OK
            else:
                contrato_message = serializer.errors
                contrato_status = status.HTTP_400_BAD_REQUEST

            return Response({'data': serializer.data,
                             'status': contrato_status,
                             'message': contrato_message})

        except Exception as e:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': e})

    def destroy(self, request, pk=None):
        contrato = Contrato.objects.get(id=pk)
        try:
            contrato.delete()
            return Response({'data': pk,
                             'status': status.HTTP_200_OK,
                             'message': "El contrato {0} fue eliminado".format(
                                 contrato.empleado.numero_identificacion)
                             })
        except ProtectedError:
            msg = "El Contrato {0} , no puede eliminarse".format(contrato.id)
            return HttpResponse(json.dumps({'data': pk,
                                            'status': status.HTTP_400_BAD_REQUEST,
                                            'message': msg}),
                                content_type='application/json')


class ConsolidadoRolPagoViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            objeto = ConsolidadoRolPago.objects.get(id=pk)
            consolidado_rol_pago = ConsolidadRolPagoSerializer(objeto).data
            return Response(
                {'data': consolidado_rol_pago, 'status': status.HTTP_200_OK,
                 'message': None})
        except ConsolidadoRolPago.DoesNotExist:
            return Response({'data': None, 'status': status.HTTP_404_NOT_FOUND,
                             'message': None})

    @method_decorator(IsAuthenticated())
    def list(self, request):
        page = request.GET.get('PAGE')
        items_per_page = request.GET.get('PAGE_SIZE')
        filter = request.GET.get('FILTER')
        queryset = ConsolidadoRolPago.objects.all()
        count = queryset.count();
        if filter is not None:
            queryset = queryset.filter(Q(observacion__icontains=filter))
        queryset_pagination = api_paginacion(queryset, int(page),
                                             items_per_page)
        serializer = ConsolidadRolPagoSerializer(queryset_pagination, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None, 'count': count})

    def create(self, request):
        try:
            consolidado_rol_pago = ConsolidadoRolPago()
            consolidado_rol_pago.fecha_desde = format_timezone_to_date(
                request.data['fecha_desde'])
            consolidado_rol_pago.fecha_hasta = format_timezone_to_date(
                request.data['fecha_hasta'])
            serializer = ConsolidadRolPagoSerializer(consolidado_rol_pago,
                                                     data=request.data)

            if serializer.is_valid():
                serializer.save()
                consolidado_rol_pago_message = 'Consolidado de Rol de Pago Creado Satisfactoriamente.'
                consolidado_rol_pago_status = status.HTTP_200_OK
            else:
                consolidado_rol_pago_message = serializer.errors
                consolidado_rol_pago_status = status.HTTP_400_BAD_REQUEST

            return Response({'data': serializer.data,
                             'status': consolidado_rol_pago_status,
                             'message': consolidado_rol_pago_message})

        except Exception as e:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': e})

    def update(self, request, pk=None):
        try:
            consolidado_rol_pago = ConsolidadoRolPago.objects.get(id=pk)
            consolidado_rol_pago.fecha_desde = format_timezone_to_date(
                request.data['fecha_desde'])
            consolidado_rol_pago.fecha_hasta = format_timezone_to_date(
                request.data['fecha_hasta'])

            serializer = ConsolidadRolPagoSerializer(consolidado_rol_pago,
                                                     data=request.data)
            if serializer.is_valid():
                serializer.save()
                consolidado_rol_pago_message = 'Consonsolidado de Rol de Pago Actualizado Satisfactoriamente.'
                consolidado_rol_pago_status = status.HTTP_200_OK
            else:
                consolidado_rol_pago_message = serializer.errors
                consolidado_rol_pago_status = status.HTTP_400_BAD_REQUEST

            return Response({'data': serializer.data,
                             'status': consolidado_rol_pago_status,
                             'message': consolidado_rol_pago_message})

        except Exception as e:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': e})

    def destroy(self, request, pk=None):
        consolidado_rol_pago = ConsolidadoRolPago.objects.get(id=pk)
        try:
            consolidado_rol_pago.delete()
            return Response({'data': pk,
                             'status': status.HTTP_200_OK,
                             'message': "El consolidado de roles de pago {0} fue eliminado".format(
                                 consolidado_rol_pago.observacion)
                             })
        except ProtectedError:
            msg = "El Consolidado de Roles de Pago {0} , no puede eliminarse".format(
                consolidado_rol_pago.id)
            return HttpResponse(json.dumps({'data': pk,
                                            'status': status.HTTP_400_BAD_REQUEST,
                                            'message': msg}),
                                content_type='application/json')


class DetalleRolPagoViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            objeto = DetalleRolPago.objects.get(id=pk)
            detalle_rolpago = DetalleRolPagoSerializer(objeto).data
            return Response(
                {'data': detalle_rolpago, 'status': status.HTTP_200_OK,
                 'message': None})
        except DetalleRolPago.DoesNotExist:
            return Response({'data': None, 'status': status.HTTP_404_NOT_FOUND,
                             'message': None})

    @method_decorator(IsAuthenticated())
    def list(self, request):
        page = request.GET.get('PAGE')
        items_per_page = request.GET.get('PAGE_SIZE')
        filter = request.GET.get('FILTER')
        queryset = DetalleRolPago.objects.all()
        count = queryset.count();
        if filter is not None:
            queryset = queryset.filter(Q(observacion__icontains=filter))
        queryset_pagination = api_paginacion(queryset, int(page),
                                             items_per_page)
        serializer = DetalleRolPagoSerializer(queryset_pagination, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None, 'count': count})

    @list_route()
    def list_by_rolpago(self, request):
        page = request.GET.get('PAGE')
        items_per_page = request.GET.get('PAGE_SIZE')
        filter = request.GET.get('FILTER')
        rol_pago = request.GET.get('ROL_PAGO')
        queryset = DetalleRolPago.objects.filter(rol_pago=rol_pago)
        count = queryset.all().count();
        param = Parametrizacion.objects.get(codigo="REGLAS_NEGOCIO")
        if filter is not None:
            queryset = queryset.filter(Q(observacion__icontains=filter))
        queryset_pagination = api_paginacion(queryset.all(), int(page),
                                             items_per_page)

        for detalle in queryset_pagination:

            if detalle.estructura_detalle_rolpago.editable is False:
                var = {}
                exec(detalle.estructura_detalle_rolpago.regla, var)
                method = (var['calcular'])

                detalle = (method(detalle, detalle.rol_pago.contrato.empleado,
                                  param))

        serializer = DetalleRolPagoSerializer(queryset_pagination, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None, 'count': count})

    def create(self, request):
        try:
            detalle_rol_pago = DetalleRolPago()
            serializer = DetalleRolPagoSerializer(detalle_rol_pago,
                                                  data=request.data)

            if serializer.is_valid():
                serializer.save()
                detalle_rol_pago_message = 'DetalleRolPago Creado Satisfactoriamente.'
                detalle_rol_pago_status = status.HTTP_200_OK
            else:
                detalle_rol_pago_message = serializer.errors
                detalle_rol_pago_status = status.HTTP_400_BAD_REQUEST

            return Response({'data': serializer.data,
                             'status': detalle_rol_pago_status,
                             'message': detalle_rol_pago_message})

        except Exception as e:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': e})

    def update(self, request, pk=None):
        try:
            detalle_rol_pago = DetalleRolPago.objects.get(id=pk)
            serializer = DetalleRolPagoSerializer(consolidado_rol_pago,
                                                  data=request.data)
            if serializer.is_valid():
                serializer.save()
                consolidado_rol_pago_message = 'Consonsolidado de Rol de Pago Actualizado Satisfactoriamente.'
                consolidado_rol_pago_status = status.HTTP_200_OK
            else:
                consolidado_rol_pago_message = serializer.errors
                consolidado_rol_pago_status = status.HTTP_400_BAD_REQUEST

            return Response({'data': serializer.data,
                             'status': consolidado_rol_pago_status,
                             'message': consolidado_rol_pago_message})

        except Exception as e:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': e})

    def destroy(self, request, pk=None):
        consolidado_rol_pago = ConsolidadoRolPago.objects.get(id=pk)
        try:
            consolidado_rol_pago.delete()
            return Response({'data': pk,
                             'status': status.HTTP_200_OK,
                             'message': "El consolidado de roles de pago {0} fue eliminado".format(
                                 consolidado_rol_pago.observacion)
                             })
        except ProtectedError:
            msg = "El Consolidado de Roles de Pago {0} , no puede eliminarse".format(
                consolidado_rol_pago.id)
            return HttpResponse(json.dumps({'data': pk,
                                            'status': status.HTTP_400_BAD_REQUEST,
                                            'message': msg}),
                                content_type='application/json')

    @detail_route(methods=['post'])
    def create_detalles_by_rolpago(self, request, pk=None):
        try:
            empresa = request.GET.get("EMPRESA")
            rol_pago_id = request.GET.get("ROL_PAGO")
            estructuras_detalle_rolpago = EstructuraDetalleRolPago.objects.filter(
                estado=True, empresa=empresa).all()
            estructuras_detalle_rolpago_by_rolpago = EstructuraDetalleRolPago.objects.filter(
                detalles__rol_pago=rol_pago_id).all()
            estructuras_detalles_diff = list(
                set(estructuras_detalle_rolpago).difference(
                    estructuras_detalle_rolpago_by_rolpago))
            detalles_rolpago = []
            for estructura in estructuras_detalles_diff:
                detalle_rolpago = DetalleRolPago()
                detalle_rolpago.nombre = estructura.nombre
                detalle_rolpago.descripcion = ""
                detalle_rolpago.estructura_detalle_rolpago = estructura
                detalle_rolpago.rol_pago_id = rol_pago_id
                detalle_rolpago.save()
                detalles_rolpago.append(detalle_rolpago)
            serializer = DetalleRolPagoSerializer(detalles_rolpago, many=True)
            return Response(
                {'data': serializer.data, 'status': status.HTTP_200_OK,
                 'message': None, "count": len(detalles_rolpago) + len(
                    estructuras_detalle_rolpago)})
        except Exception as e:
            return Response(
                {'data': None, 'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                 'message': json.dumps(e)})

    @list_route()
    def get_valor_by_rule(self, request):
        """

        :param request:
        :return:
        """
        try:

            detalle_rol_pago = json.loads(request.GET.get("DETALLE_ROL_PAGO"))
            detalle_object = DetalleRolPago()
            detalle_object.cantidad = detalle_rol_pago['cantidad']
            detalle_object.valor = detalle_rol_pago['valor']
            param = Parametrizacion.objects.get(codigo="REGLAS_NEGOCIO")
            regla = EstructuraDetalleRolPago.objects.get(
                id=detalle_rol_pago['estructura_detalle_rolpago']['id'])

            empleado = Empleado.objects.get(
                id=detalle_rol_pago["rol_pago"]['contrato']["empleado"]["id"])
            var = {}
            exec(regla.regla, var)
            method = (var['calcular'])
            detalle_object = (method(detalle_object,
                                     empleado, param))
            detalle_rol_pago['valor'] = detalle_object.valor
            return Response(
                {'data': detalle_rol_pago, 'status': status.HTTP_200_OK,
                 'message': None, })
        except Exception as e:
            return Response(
                {'data': None, 'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                 'message': json.dumps(e)})
