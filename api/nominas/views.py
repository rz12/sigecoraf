from django.db.models import Q
from django.utils.decorators import method_decorator
from rest_framework import status, viewsets
from rest_framework.response import Response

from api.nominas.serializers import EmpleadoSerializer, RolPagoSerializer, \
    CargoSerializer, ContratoSerializer
from api.seguridad.permissions import IsAuthenticated
from app.master.views import *
from app.nominas.models import Empleado, RolPago, Cargo, Contrato


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

            serializer = EmpleadoSerializer(empleado, data=request.data)

            if serializer.is_valid():
                serializer.save()
                empleado_message = 'Empleado Creado Satisfactoriamente.'
                empleado_status = status.HTTP_200_OK
            else:
                empleado_message = serializer.errors
                empleado_status = status.HTTP_400_BAD_REQUEST

            return Response({'data': serializer.data,
                             'status': empleado_status,
                             'message': empleado_message})

        except Exception as e:
            print(e)
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

            if request.data['tipo_documento_identificacion_object'][
                'codigo'] == 'CEDULA' or \
                    request.data['tipo_documento_identificacion_object'][
                        'codigo'] == 'RUC':

                if verificar(request.data['numero_identificacion']) is False:
                    return Response({'data': None,
                                     'status': status.HTTP_400_BAD_REQUEST,
                                     'message': 'Número de Identificación Incorrecto'})

            serializer = EmpleadoSerializer(empleado, data=request.data)
            if serializer.is_valid():
                serializer.save()
                empleado_message = 'Empleado Actualizado Satisfactoriamente.'
                empleado_status = status.HTTP_200_OK
            else:
                empleado_message = serializer.errors
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

    ##@method_decorator(IsAuthenticated('ROLPAGO', None))
    def list(self, request):
        #queryset.all()
        serializer = RolPagoSerializer(None, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None})

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

        queryset = Contrato.objects.filter(estado=True).all()
        serializer = ContratoSerializer(queryset, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'count': queryset.count(), 'message': None})

    def create(self, request):
        try:
            contrato = Contrato()
            serializer = ContratoSerializer(contrato, data=request.data)
            if serializer.is_valid():
                serializer.save()
                contrato_message = 'Contrato creado'
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
            serializer = ContratoSerializer(contrato, data=request.data)
            if serializer.is_valid():
                serializer.save()
                contrato_message = 'Contrato actualizado'

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
        print(serializer.data, 'aqui')
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'count': count, 'message': None})

    def create(self, request):
        try:
            cargo = Cargo()
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
            print(request.data)
            contratos_empleado_vigentes = Contrato.objects.filter(
                empleado__id=request.data['empleado'], estado=True).all()
            print('paso1')
            if contratos_empleado_vigentes.count() > 0:
                return Response({'data': None,
                                 'status': status.HTTP_400_BAD_REQUEST,
                                 'message': "El empleado ya tiene un contrato"})
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
