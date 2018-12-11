from rest_framework import serializers
from .models import Contract, Client


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = (
            'id', 'title', 'date_begin', 'date_end', 'content',
            'clients', 'status',
        )


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            'id', 'name',
        )
