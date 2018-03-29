from rest_framework import status, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from api.master.serializers import ParametrizacionSerializer
from app.master.models import Parametrizacion
from app.seguridad.models import Menu


class ParametrizacionViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Parametrizacion.objects.all()
        serializer = ParametrizacionSerializer(queryset, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None})


