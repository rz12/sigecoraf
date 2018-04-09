from django.utils.decorators import method_decorator
from rest_framework import status, viewsets
from rest_framework.response import Response

from api.nominas.serializers import EmpleadoSerializer, RolPagoSerializer, \
    CargoSerializer, ContratoSerializer
from api.seguridad.permissions import IsAuthenticated
from app.master.utils.enums import AuthEnum
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

    def list(self, request):
        queryset = Empleado.objects.all()
        serializer = EmpleadoSerializer(queryset, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None})

    def create(self, request):
        try:
            empleado = Empleado()
            serializer = EmpleadoSerializer(empleado, data=request.data)
            if serializer.is_valid():
                serializer.save()
                empleado_message = 'Empleado creado'
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
    '''

    '''

    def retrieve(self, request, pk=None):
        '''

        :param request:
        :param pk:
        :return:
        '''
        try:
            objeto = RolPago.objects.get(id=pk)
            empleado = RolPagoSerializer(objeto).data
            return Response({'data': rolpago, 'status': status.HTTP_200_OK,
                             'message': None})
        except RolPago.DoesNotExist:
            return Response({'data': None, 'status': status.HTTP_404_NOT_FOUND,
                             'message': None})

    def list(self, request):
        '''

        :param request:
        :return:
        '''
        queryset = RolPago.objects.all()
        serializer = RolPagoSerializer(queryset, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None})

    # @method_decorator(IsAuthenticated(None, 'add_rolpago'))
    def create(self, request):
        '''

        :param request:
        :return:
        '''
        try:
            rolpago = RolPago()
            serializer = RolPagoSerializer(rolpago, data=request.data)
            if serializer.is_valid():
                serializer.save()
                rolpago_message = 'Rol de Pago creado'
                rolpago_status = status.HTTP_200_OK
            else:
                rolpago_message = serializer.errors
                rolpago_status = status.HTTP_400_BAD_REQUEST

            return Response({'data': serializer.data,
                             'status': rolpago_status,
                             'message': rolpago_message})

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

    @method_decorator(IsAuthenticated('CARGOS', None))
    def list(self, request):
        queryset = Cargo.objects.filter(estado=True).all()
        serializer = CargoSerializer(queryset, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None})

    def create(self, request):
        try:
            cargo = Cargo()
            serializer = CargoSerializer(cargo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                cargo_message = 'Cargo creado'
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
                cargo_message = 'Cargo actualizado'
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
            contrato = CargoSerializer(objeto).data
            return Response({'data': contrato, 'status': status.HTTP_200_OK,
                             'message': None})
        except Contrato.DoesNotExist:
            return Response({'data': None, 'status': status.HTTP_404_NOT_FOUND,
                             'message': None})

    def list(self, request):
        queryset = Contrato.objects.all()
        serializer = CargoSerializer(queryset, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None})

    def create(self, request):
        try:
            contratos = Contrato()
            serializer = ContratoSerializer(contratos, data=request.data)
            if serializer.is_valid():
                serializer.save()
                contratos_message = 'Empleado creado'
                contratos_status = status.HTTP_200_OK
            else:
                contratos_message = serializer.errors
                contratos_status = status.HTTP_400_BAD_REQUEST

            return Response({'data': serializer.data,
                             'status': contratos_status,
                             'message': contratos_message})

        except Exception as e:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': e})
