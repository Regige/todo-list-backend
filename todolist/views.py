from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import TodoItem
from .serializers import TodoItemSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from datetime import date
from django.http import Http404
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import generics



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
    
    
    def get_object(self, pk):
        try:
            return TodoItem.objects.get(pk=pk)
        except TodoItem.DoesNotExist:
            raise Http404
        
        
    def put(self, request, pk, format=None):
        todo = self.get_object(pk)
        serializer = TodoItemSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self, request, pk, format=None):
        todo = self.get_object(pk)
        todo.delete()
        return Response({'message': 'Todo Item successfully deleted', 'id': pk}, status=status.HTTP_200_OK)



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
        
        
        
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer