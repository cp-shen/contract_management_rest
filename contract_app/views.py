from rest_framework import generics
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from . import models
from . import serializers
from django.shortcuts import redirect
from django.core.exceptions import ValidationError


def index(request):
    return redirect('docs/')


class ContractList(generics.ListCreateAPIView):
    queryset = models.Contract.objects.all()
    serializer_class = serializers.ContractSerializer
    filterset_fields = ('author', 'status')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as err:
            return Response(err.error_dict, status=status.HTTP_400_BAD_REQUEST)


class ContractDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Contract.objects.all()
    serializer_class = serializers.ContractSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        except ValidationError as err:
            return Response(err.error_dict, status=status.HTTP_400_BAD_REQUEST)


class ClientList(generics.ListCreateAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    filterset_fields = ('name', )


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer


class CountersignList(generics.ListCreateAPIView):
    queryset = models.Countersign.objects.all()
    serializer_class = serializers.CountersignSerializer
    filterset_fields = ('user', 'contract', 'is_confirmed')


class CountersignDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Countersign.objects.all()
    serializer_class = serializers.CountersignSerializer


class ReviewList(generics.ListCreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReivewSerializer
    filterset_fields = ('user', 'contract', 'is_confirmed')


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReivewSerializer


class SignList(generics.ListCreateAPIView):
    queryset = models.Sign.objects.all()
    serializer_class = serializers.SignSerializer
    filterset_fields = ('user', 'contract', 'is_confirmed')


class SignDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Sign.objects.all()
    serializer_class = serializers.SignSerializer


class RoleList(generics.ListCreateAPIView):
    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleSerializer
    filterset_fields = ('__all__')


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


class MyDetail(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        return Response(serializers.MyUserSerializer(request.user).data)


class ChangePwd(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.PwdSerializer

    def post(self, request, format=None):
        serializer = serializers.PwdSerializer(data=request.data)
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['password'])
            request.user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    queryset = models.MyUser.objects.all()
    serializer_class = serializers.MyUserSerializer
    filterset_fields = ('role',)


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = models.MyUser.objects.all()
    serializer_class = serializers.MyUserSerializer
