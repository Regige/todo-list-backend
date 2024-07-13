from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import TodoItem
from .serializers import TodoItemSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class TodoItemView(APIView):
    # zum Nutzen des Tokens den man beim Login erhält, und hier immer mit gesendet wird!
    authentication_classes = [TokenAuthentication] 
    # man muss eingeloggt sein!
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        todos = TodoItem.objects.all()
        serializer = TodoItemSerializer(todos, many=True)
        return Response(serializer.data)


class LoginView(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })