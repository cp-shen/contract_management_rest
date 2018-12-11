from rest_framework import generics
# from rest_framework.views import APIView
# from rest_framework.response import Response
from .models import Client, Contract
from .serializers import ContractSerializer, ClientSerializer
from django.shortcuts import redirect


def index(request):
    return redirect('docs/')


class ContractList(generics.ListCreateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class ContractDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
