from django.utils.decorators import method_decorator
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import list_route
from rest_framework.response import Response

from api.seguridad.permissions import IsAuthenticated
from api.seguridad.serializers import UsuarioSerializer, MenuSerializer
from app.master.utils.enums import AuthEnum
from app.seguridad.models import Usuario, Menu


class UsuarioViewSet(viewsets.ViewSet):

    @list_route()
    def get_usuario_by_token(self, request):
        """
        Éste método permite devolver un usuario a través de un token de
        seguridad.
        :param request:
        :return:
        """
        try:

            token = Token.objects.get(
                key=request.META[AuthEnum.HTTP_AUTHORIZATION.value])
            if token is None:
                return Response({'status': status.HTTP_400_BAD_REQUEST,
                                 'message': 'Error de Autenticacion'},
                                status=status.HTTP_400_BAD_REQUEST)
            usuarios = Usuario.objects.filter(id=token.user.id).all()
            usuario = None
            if usuarios.count() == 0:
                usuario = Usuario()
                usuario.username = token.user.username
                usuario.first_name = token.user.first_name
                usuario.last_name = token.user.last_name
                usuario.email = token.user.email
            else:
                usuario = usuarios[0]

            if usuario is None:
                return Response({'status': status.HTTP_400_BAD_REQUEST,
                                 'message': 'Error de Autenticacion'},
                                status=status.HTTP_400_BAD_REQUEST)

            serialized = UsuarioSerializer(usuario)
            return Response({'data':serialized.data})

        except Exception as e:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': e
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MenusViewSet(viewsets.ViewSet):

    def list(self, request):

        queryset = Menu.objects.filter(estado=True,
                                       padre=None).all().order_by('orden')
        serializer = MenuSerializer(queryset, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK,
                         'message': None})

    @list_route()
    @method_decorator(IsAuthenticated())
    def has_permission(self,request):
        return Response({'data': True, 'status': status.HTTP_200_OK,
                         'message': None})
