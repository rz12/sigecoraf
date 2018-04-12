from django.utils.decorators import method_decorator
from rest_framework import status, viewsets
from rest_framework.response import Response

from api.master.serializers import ParametrizacionSerializer, EmpresaSerializer
from api.seguridad.permissions import IsAuthenticated
from app.master.models import Parametrizacion, Empresa


class ParametrizacionViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Parametrizacion.objects.all()
        serializer = ParametrizacionSerializer(queryset, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None})


class EmpresaViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            objeto = Empresa.objects.get(id=pk)
            empresa = EmpresaSerializer(objeto).data
            return Response({'data': empresa, 'status': status.HTTP_200_OK,
                             'message': None})
        except Empresa.DoesNotExist:
            return Response({'data': None, 'status': status.HTTP_404_NOT_FOUND,
                             'message': None})

    @method_decorator(IsAuthenticated())
    def list(self, request):
        queryset = Empresa.objects.filter(estado=True).all()
        serializer = EmpresaSerializer(queryset, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None})

    def create(self, request):
        try:
            empresa = Empresa()
            serializer = EmpresaSerializer(empresa, data=request.data)
            if serializer.is_valid():
                serializer.save()
                empresa_message = 'Empresa creada satisfactoriamente'
                empresa_status = status.HTTP_200_OK
            else:
                empresa_message = serializer.errors
                empresa_status = status.HTTP_400_BAD_REQUEST

            return Response({'data': serializer.data,
                             'status': empresa_status,
                             'message': empresa_message})

        except Exception as e:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': e})

    def update(self, request, pk=None):
        try:
            empresa = Empresa.objects.get(id=pk)
            serializer = EmpresaSerializer(empresa, data=request.data)
            if serializer.is_valid():
                serializer.save()
                empresa_message = 'Empresa actualizada satisfactoriamente'
                empresa_status = status.HTTP_200_OK
            else:
                empresa_message = serializer.errors
                empresa_status = status.HTTP_400_BAD_REQUEST

            return Response({'data': serializer.data,
                             'status': empresa_status,
                             'message': empresa_message})

        except Exception as e:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': e})
