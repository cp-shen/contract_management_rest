from rest_framework import generics
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers
from django.shortcuts import redirect


def index(request):
    return redirect('docs/')


class ContractList(generics.ListCreateAPIView):
    queryset = models.Contract.objects.all()
    serializer_class = serializers.ContractSerializer


class ContractDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Contract.objects.all()
    serializer_class = serializers.ContractSerializer


class ClientList(generics.ListCreateAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer


class CountersignList(generics.ListCreateAPIView):
    queryset = models.Countersign.objects.all()
    serializer_class = serializers.CountersignSerializer


class CountersignDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Countersign.objects.all()
    serializer_class = serializers.CountersignSerializer


class ReviewList(generics.ListCreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReivewSerializer


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReivewSerializer


class SignList(generics.ListCreateAPIView):
    queryset = models.Sign.objects.all()
    serializer_class = serializers.SignSerializer


class SignDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Sign.objects.all()
    serializer_class = serializers.SignSerializer


class RoleList(generics.ListCreateAPIView):
    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleSerializer


class RoleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleSerializer


class Register(generics.GenericAPIView):
    serializer_class = serializers.RegisterSerializer

    def post(self, request, format=None):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class MyDetail(generics.GenericAPIView):
    # def patch(self, request, format=None):
    # def get(self, request, format=None):
