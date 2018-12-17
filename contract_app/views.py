from rest_framework import generics
# from rest_framework.views import APIView
# from rest_framework.response import Response
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
