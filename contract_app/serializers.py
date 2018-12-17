from rest_framework import serializers
from .models import Contract, Client


class ContractSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Contract
        fields = (
            'id', 'title', 'date_begin', 'date_end', 'content',
            'clients', 'status', 'author',
        )

    def validate(self, data):
        if data['date_begin'] > data['date_end']:
            raise serializers.ValidationError("contract finish must occur after start")
        return data


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            'id', 'name',
        )
