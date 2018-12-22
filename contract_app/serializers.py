from rest_framework import serializers
from . import models


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = (
            'id', 'name',
        )


class CountersignSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=models.MyUser.objects.all()
    )
    contract = serializers.PrimaryKeyRelatedField(
        queryset=models.Contract.objects.all()
    )

    class Meta:
        model = models.Countersign
        fields = (
            'user', 'contract', 'message', 'is_confirmed',
        )


class ReivewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=models.MyUser.objects.all()
    )
    contract = serializers.PrimaryKeyRelatedField(
        queryset=models.Contract.objects.all()
    )

    class Meta:
        model = models.Review
        fields = (
            'user', 'contract', 'message', 'is_confirmed',
        )


class SignSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=models.MyUser.objects.all()
    )
    contract = serializers.PrimaryKeyRelatedField(
        queryset=models.Contract.objects.all()
    )

    class Meta:
        model = models.Sign
        fields = (
            'user', 'contract', 'message', 'is_confirmed',
        )


class ContractSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=models.MyUser.objects.all()
    )
    countersign_set = CountersignSerializer(many=True, read_only=True)
    review_set = ReivewSerializer(many=True, read_only=True)
    sign_set = SignSerializer(many=True, read_only=True)
    clients = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=models.Client.objects.all()
    )

    class Meta:
        model = models.Contract
        fields = (
            'id', 'title', 'date_begin', 'date_end', 'content',
            'clients', 'status', 'author',
            'countersign_set', 'review_set', 'sign_set'
        )

    def validate(self, data):
        if data['date_begin'] > data['date_end']:
            raise serializers.ValidationError("contract finish must occur after start")
        return data
