from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('no email provided')
        if not password:
            raise ValueError('no password provided')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    # todo: set user permissions


class Client(models.Model):
    name = models.CharField(max_length=30)


class Contract(models.Model):
    CREATED = 'created'
    COUNTERSIGNED = 'countersigned'
    REWRITED = 'rewrited'
    REVIEWED = 'reviewed'
    SIGNED = 'signed'
    STATUS_CHOICES = (
        (CREATED, 'Created'),
        (COUNTERSIGNED, 'Countersigned'),
        (REWRITED, 'Rewrited'),
        (REVIEWED, 'Reviewed'),
        (SIGNED, 'Signed'),
    )
    title = models.CharField(max_length=50)
    date_begin = models.DateField()
    date_end = models.DateField()
    content = models.CharField(max_length=5000)
    clients = models.ManyToManyField(Client)
    status = models.CharField(choices=STATUS_CHOICES, default=CREATED)
    # attachment with 10 MB max size
    # attachment = models.BinaryField(null=True, editable=True, max_length=10 * 1024 * 1024)
    # todo: add models data validation in clean and save,
    # such as procudure control, and date comparison


class Countersign(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    is_confirmed = models.BooleanField(default=False)


class Review(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    is_confirmed = models.BooleanField(default=False)


class Sign(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    is_confirmed = models.BooleanField(default=False)
