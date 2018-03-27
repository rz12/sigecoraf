from rest_framework import status, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from api.seguridad.serializers import UsuarioSerializer
from app.master.utils.enums import AuthEnum
from app.seguridad.models import Usuario
from rest_framework.authtoken.models import Token


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
                usuario = Usuario(token.user.username, token.user.first_name,
                                  token.user.last_name, token.user.email)
            else:
                usuario = usuarios[-1]

            if usuario is None:
                return Response({'status': status.HTTP_400_BAD_REQUEST,
                                 'message': 'Error de Autenticacion'},
                                status=status.HTTP_400_BAD_REQUEST)
            
            serialized = UsuarioSerializer(usuario)
            return Response(serialized.data)

        except Exception as e:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': e
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
