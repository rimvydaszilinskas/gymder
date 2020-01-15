from django.contrib.auth import authenticate

from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from apps.users.models import User
from apps.users.serializers import UserSerializer, MobileUserSerializer


class AuthPingView(views.APIView):
    serializer_class = UserSerializer
    
    def get(self, request, *args, **kwargs):
        return Response(self.serializer_class(request.user).data)


class PingView(views.APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        return Response()


class AuthenticateUserView(views.APIView):
    """
    View for authorizing mobile users

    Returns token as well as the user
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = MobileUserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if not email or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if not user:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={'detail': 'Wrong credentials'})

        token, created = Token.objects.get_or_create(user=user)

        serializer = self.serializer_class(user)

        return Response(status=status.HTTP_200_OK, data=serializer.data)
