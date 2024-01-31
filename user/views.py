from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .serializers import JoinSerializer, CustomTokenObtainPairSerializer
from .models import User

class UserView(APIView):

    def post(self, request):
        serializer = JoinSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료"},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            username = request.query_params['username']
        except KeyError:
            return Response({'result':'Bad Request'},status=status.HTTP_400_BAD_REQUEST)
        else:
            flag = User.objects.filter(username = username).exists()
            return Response({'result': flag}, status=status.HTTP_200_OK)

from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer