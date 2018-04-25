from django.utils.decorators import method_decorator
from rest_framework import status, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from api.master.serializers import ParametrizacionSerializer, EmpresaSerializer, \
    CatalogoSerializer, DireccionSerializer, ItemSerializer
from api.seguridad.permissions import IsAuthenticated
from app.master.models import Parametrizacion, Empresa, Catalogo, Direccion, \
    Item


class ParametrizacionViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Parametrizacion.objects.all()
        serializer = ParametrizacionSerializer(queryset, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None})


class CatalogoViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Catalogo.objects.all()
        serializer = CatalogoSerializer(queryset, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None})

    @list_route()
    def list_by_codigo(self, request):
        queryset = Catalogo.objects.all().order_by('nombre')
        codigo = None
        if 'CODIGO' in request.GET:
            codigo = request.GET['CODIGO']
            queryset = queryset.filter(codigo=codigo)
        serializer = CatalogoSerializer(queryset, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None})


class ItemViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        try:
            objeto = Item.objects.get(id=pk)
            item = ItemSerializer(objeto).data
            return Response({'data': item, 'status': status.HTTP_200_OK,
                             'message': None})
        except Item.DoesNotExist:
            return Response({'data': None, 'status': status.HTTP_404_NOT_FOUND,
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


class DireccionViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            objeto = Direccion.objects.get(id=pk)
            direccion = DireccionSerializer(objeto).data
            return Response({'data': direccion, 'status': status.HTTP_200_OK,
                             'message': None})
        except Direccion.DoesNotExist:
            return Response({'data': None, 'status': status.HTTP_404_NOT_FOUND,
                             'message': None})

    def list(self, request):
        queryset = Direccion.objects.all()
        persona = None
        if 'PERSONA' in request.GET:
            persona = request.GET['PERSONA']
            queryset = queryset.filter(persona_id=persona)
        count = queryset.count();
        serializer = DireccionSerializer(queryset, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None,'count':count})

    def create(self, request):
        try:
            direccion = Direccion()
            serializer = DireccionSerializer(direccion, data=request.data)
            if serializer.is_valid():
                serializer.save()
                direccion_message = 'Dirección creada satisfactoriamente'
                direccion_status = status.HTTP_200_OK
            else:
                direccion_message = serializer.errors
                direccion_status = status.HTTP_400_BAD_REQUEST

            return Response({'data': serializer.data,
                             'status': direccion_status,
                             'message': direccion_message})

        except Exception as e:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': e})

    def update(self, request, pk=None):
        try:
            direccion = Direccion.objects.get(id=pk)
            print(direccion, 'paso 1')
            serializer = DireccionSerializer(direccion, data=request.data)
            print(direccion, 'paso 2')
            if serializer.is_valid():
                serializer.save()
                direccion_message = 'Dirección actualizada satisfactoriamente'
                direccion_status = status.HTTP_200_OK
            else:
                direccion_message = serializer.errors
                direccion_status = status.HTTP_400_BAD_REQUEST

            return Response({'data': serializer.data,
                             'status': direccion_status,
                             'message': direccion_message})

        except Exception as e:
            return Response({'data': None,
                             'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': e})

    def destroy(self, request, pk=None):
        direccion = Direccion.objects.get(id=pk)
        try:
            direccion.delete()
            return Response({'data': pk,
                             'status': status.HTTP_200_OK,
                             'message': "La Dirección {0} fue eliminado".format(
                                 direccion.calle_principal.upper())
                             })
        except ProtectedError:
            msg = "La Dirección {0} , no puede eliminarse".format(direccion.id)
            return HttpResponse(json.dumps({'data': pk,
                                            'status': status.HTTP_400_BAD_REQUEST,
                                            'message': msg}),
                                content_type='application/json')
