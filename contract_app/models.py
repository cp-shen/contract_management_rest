from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('no username provided')
        if not password:
            raise ValueError('no password provided')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.EmailField(max_length=255, unique=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    # todo: set user permissions


class Client(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return ':'.join([str(self.id), self.name])


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
    status = models.CharField(choices=STATUS_CHOICES, default=CREATED, max_length=50)
    # attachment with 10 MB max size
    # attachment = models.BinaryField(null=True, editable=True, max_length=10 * 1024 * 1024)

    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, editable=False)
    users_countersign = models.ManyToManyField(MyUser, through='Countersign', related_name='contracts_countersign')
    users_review = models.ManyToManyField(MyUser, through='Review', related_name='contracts_review')
    users_sign = models.ManyToManyField(MyUser, through='Sign', related_name='contracts_sign')

    def __str__(self):
        return ':'.join([str(self.id), self.title])

    def check_countersign(self):
        count = self.countersign_set.filter(is_confirmed=False).count()
        if count > 0:
            raise ValidationError('%s people have not countersigned' % count)

    def check_review(self):
        count = self.review_set.filter(is_confirmed=False).count()
        if count > 0:
            raise ValidationError('%s people have not reviewed' % count)

    def check_sign(self):
        count = self.sign_set.filter(is_confirmed=False).count()
        if count > 0:
            raise ValidationError('%s people have not signed' % count)

    def clean(self):
        if self.status == self.CREATED:
            pass
        elif self.status == self.COUNTERSIGNED:
            self.check_countersign()
        elif self.status == self.REWRITED:
            self.check_countersign()
        elif self.status == self.REVIEWED:
            self.check_countersign()
            self.check_review()
        elif self.status == self.SIGNED:
            self.check_countersign()
            self.check_review()
            self.check_sign()


class Countersign(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, editable=False)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, editable=False)
    message = models.CharField(max_length=1000)
    is_confirmed = models.BooleanField(default=False)


class Review(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, editable=False)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, editable=False)
    message = models.CharField(max_length=1000)
    is_confirmed = models.BooleanField(default=False)


class Sign(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, editable=False)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, editable=False)
    message = models.CharField(max_length=1000)
    is_confirmed = models.BooleanField(default=False)
