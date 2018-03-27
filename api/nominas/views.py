from rest_framework import status, viewsets
from rest_framework.response import Response

from api.nominas.serializers import EmpleadoSerializer, RolPagoSerializer
from app.nominas.models import Empleado, RolPago


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
