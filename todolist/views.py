from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import TodoItem
from .serializers import TodoItemSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import date


class TodoItemView(APIView):
    # zum Nutzen des Tokens den man beim Login erhält, und hier immer mit gesendet wird!
    authentication_classes = [TokenAuthentication] 
    # man muss eingeloggt sein!
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        todos = TodoItem.objects.filter(author=request.user)
        serializer = TodoItemSerializer(todos, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        request.data['author'] = request.user.id
        serializer = TodoItemSerializer(data=request.data)
        if serializer.is_valid():
            # Set the author to the current logged-in user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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