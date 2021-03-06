from rest_framework import serializers
from . import models


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = (
            'id', 'name', 'email'
        )


class CountersignSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=models.MyUser.objects.all(),
        help_text='user id',
    )
    contract = serializers.PrimaryKeyRelatedField(
        queryset=models.Contract.objects.all(),
        help_text='contract id',
    )

    class Meta:
        model = models.Countersign
        fields = (
            'id', 'user', 'contract', 'message', 'is_confirmed',
        )


class ReivewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=models.MyUser.objects.all(),
        help_text='user id',
    )
    contract = serializers.PrimaryKeyRelatedField(
        queryset=models.Contract.objects.all(),
        help_text='contract id',
    )

    class Meta:
        model = models.Review
        fields = (
            'id', 'user', 'contract', 'message', 'is_confirmed',
        )


class SignSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=models.MyUser.objects.all(),
        help_text='user id',
    )
    contract = serializers.PrimaryKeyRelatedField(
        queryset=models.Contract.objects.all(),
        help_text='contract id',
    )

    class Meta:
        model = models.Sign
        fields = (
            'id', 'user', 'contract', 'message', 'is_confirmed',
        )


class ContractSerializer(serializers.ModelSerializer):
    # author = serializers.SlugRelatedField(
    #     slug_field='username',
    #     queryset=models.MyUser.objects.all()
    # )
    author = serializers.PrimaryKeyRelatedField(
        queryset=models.MyUser.objects.all(),
        help_text='user id of the author',
    )
    countersigns = CountersignSerializer(many=True, read_only=True)
    reviews = ReivewSerializer(many=True, read_only=True)
    signs = SignSerializer(many=True, read_only=True)
    # clients = serializers.SlugRelatedField(
    #     many=True,
    #     slug_field='name',
    #     queryset=models.Client.objects.all()
    # )
    clients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Client.objects.all(),
        help_text='id of each client',
    )

    class Meta:
        model = models.Contract
        fields = (
            'id', 'title', 'date_begin', 'date_end', 'content',
            'clients', 'status', 'author',
            'countersigns', 'reviews', 'signs'
        )


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, min_length=1)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=50, min_length=6, write_only=True)

    def validate(self, data):
        if models.MyUser.objects.filter(username=data['username']).count() > 0:
            raise serializers.ValidationError('username already taken.')
        if models.MyUser.objects.filter(email=data['email']).count() > 0:
            raise serializers.ValidationError('email already taken.')
        return data

    def create(self, validated_data):
        user = models.MyUser.objects.create_user(
            validated_data['email'], validated_data['username'], validated_data['password'])
        return user


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MyUser
        fields = (
            'email', 'username', 'role', 'id',
            'contracts_created', 'countersigns', 'reviews', 'signs',
        )
    # role = serializers.SlugRelatedField(
    #     slug_field='name', queryset=models.Role.objects.all())
    role = serializers.PrimaryKeyRelatedField(queryset=models.Role.objects.all(), help_text='role id')
    contracts_created = ContractSerializer(many=True, read_only=True)
    countersigns = CountersignSerializer(many=True, read_only=True)
    reviews = ReivewSerializer(many=True, read_only=True)
    signs = SignSerializer(many=True, read_only=True)


class PwdSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=50, write_only=True)
