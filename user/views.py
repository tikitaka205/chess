from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .serializers import JoinSerializer

class UserView(APIView):

    def post(self, request):
        serializer = JoinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료"},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)