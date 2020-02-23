# pylint: disable=no-member,arguments-differ

from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt
from .serializers import UserSerializer
User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration Successful'})
        return Response(serializer.errors, status=422)


class LoginView(APIView):
    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise PermissionDenied({'message': 'Invalid Credentials'})

    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        user = self.get_user(email)

        dt = datetime.now() + timedelta(days=1)
        token = jwt.encode({
            'sub': user.id,
            'exp': int(dt.strftime('%s'))
        },
                           settings.SECRET_KEY,
                           algorithm='HS256')

        if not user.check_password(password):
            raise PermissionDenied({'message': 'Invalid Credentials'})

        token = jwt.encode({
            'sub': user.id,
            'exp': int(dt.strftime('%s'))
        },
                           settings.SECRET_KEY,
                           algorithm='HS256')
        return Response({
            'token': token,
            'message': f'Hello again {user.username}'
        })