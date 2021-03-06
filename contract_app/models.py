from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
)
from django.core.mail import EmailMessage
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    can_read_contracts = models.BooleanField(default=False)
    can_write_contracts = models.BooleanField(default=False)

    can_countersign = models.BooleanField(default=False)
    can_review = models.BooleanField(default=False)
    can_sign = models.BooleanField(default=False)
    can_distribute = models.BooleanField(default=False)

    can_manage_users = models.BooleanField(default=False)
    can_manage_roles = models.BooleanField(default=False)
    can_manage_clients = models.BooleanField(default=False)


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
    username = models.CharField(max_length=255, unique=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username

    role = models.ForeignKey(
        Role,
        related_name='users',
        on_delete=models.PROTECT,
        null=True,
    )

    def email_user(self, subject, message, from_email=settings.EMAIL_HOST_USER, **kwargs):
        """Send an email to this user."""
        # send_mail(subject, message, from_email, [self.email], **kwargs)
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=[self.email, ],
            cc=[settings.EMAIL_HOST_USER, ],
            **kwargs,
        )
        email.send(fail_silently=False)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Client(models.Model):
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True, null=True)

    def __str__(self):
        return ':'.join([str(self.id), self.name])


class Contract(models.Model):
    CREATED = 'created'
    DISTRIBUTED = 'distributed'
    COUNTERSIGNED = 'countersigned'
    REWRITED = 'rewrited'
    REVIEWED = 'reviewed'
    SIGNED = 'signed'
    STATUS_CHOICES = (
        (CREATED, 'created'),
        (DISTRIBUTED, 'distributed'),
        (COUNTERSIGNED, 'countersigned'),
        (REWRITED, 'rewrited'),
        (REVIEWED, 'reviewed'),
        (SIGNED, 'signed'),
    )
    title = models.CharField(max_length=50)
    date_begin = models.DateField()
    date_end = models.DateField()
    content = models.CharField(max_length=5000)
    clients = models.ManyToManyField(Client)
    status = models.CharField(
        choices=STATUS_CHOICES, default=CREATED, max_length=50,
        help_text='created (default), distributed, countersigned, rewrited, reviewed, signed'
    )
    # attachment with 10 MB max size
    # attachment = models.BinaryField(null=True, editable=True, max_length=10 * 1024 * 1024)

    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, editable=False, related_name='contracts_created')
    users_countersign = models.ManyToManyField(MyUser, through='Countersign', related_name='contracts_countersign')
    users_review = models.ManyToManyField(MyUser, through='Review', related_name='contracts_review')
    users_sign = models.ManyToManyField(MyUser, through='Sign', related_name='contracts_sign')

    def __str__(self):
        return ':'.join([str(self.id), self.title])

    def check_countersign(self):
        count = self.countersigns.filter(is_confirmed=False).count()
        if count > 0:
            raise ValidationError('%s people have not countersigned' % count)
        count = self.countersigns.filter(is_confirmed=True).count()
        if count == 0:
            raise ValidationError('no people have countersigned')

    def check_review(self):
        count = self.reviews.filter(is_confirmed=False).count()
        if count > 0:
            raise ValidationError('%s people have not reviewed' % count)
        count = self.reviews.filter(is_confirmed=True).count()
        if count == 0:
            raise ValidationError('no people have not reviewed')

    def check_sign(self):
        count = self.signs.filter(is_confirmed=False).count()
        if count > 0:
            raise ValidationError('%s people have not signed' % count)
        count = self.signs.filter(is_confirmed=True).count()
        if count == 0:
            raise ValidationError('no people have signed')

    def clean(self):
        if self.date_begin > self.date_end:
            raise ValidationError("contract finish must occur after start")

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
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, editable=False, related_name='countersigns')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, editable=False, related_name='countersigns')
    message = models.CharField(max_length=1000, null=True)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = (("user", "contract"),)


class Review(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, editable=False, related_name='reviews')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, editable=False, related_name='reviews')
    message = models.CharField(max_length=1000, null=True)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = (("user", "contract"),)


class Sign(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, editable=False, related_name='signs')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, editable=False, related_name='signs')
    message = models.CharField(max_length=1000, null=True)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = (("user", "contract"),)


@receiver(post_save, sender=Countersign)
def countersign_send_email(sender, instance=None, created=False, **kwargs):
    # def email_user(self, subject, message, from_email=None, **kwargs):
    if created:
        instance.user.email_user(
            'You are assigned to a new countersign.',
            'Contract #%s needs your countersign.' % instance.contract.id,
            settings.EMAIL_HOST_USER
        )


@receiver(post_save, sender=Review)
def review_send_email(sender, instance=None, created=False, **kwargs):
    if created:
        instance.user.email_user(
            'You are assigned to a new reivew.',
            'Contract #%s needs your review.' % instance.contract.id,
            settings.EMAIL_HOST_USER
        )


@receiver(post_save, sender=Sign)
def sign_send_email(sender, instance=None, created=False, **kwargs):
    if created:
        instance.user.email_user(
            'You are assigned to a new sign.',
            'Contract #%s needs your sign.' % instance.contract.id,
            settings.EMAIL_HOST_USER
        )


@receiver(pre_save, sender=Contract)
def contract_pre_save_clean(sender, instance, *args, **kwargs):
    instance.full_clean()


def change_contract_status(sender, instance, *args, **kwargs):
    """
    automatically change the status afer saving contract objects
    """
    try:
        if instance.status == Contract.CREATED:
            pass
        elif instance.status == Contract.DISTRIBUTED:
            instance.check_countersign()
            instance.status = Contract.COUNTERSIGNED
            instance.save()
        elif instance.status == Contract.COUNTERSIGNED:
            pass
        elif instance.status == Contract.REWRITED:
            instance.check_review()
            instance.status = Contract.REVIEWED
            instance.save()
        elif instance.status == Contract.REVIEWED:
            instance.check_sign()
            instance.status = Contract.SIGNED
            instance.save()
        elif instance.status == Contract.SIGNED:
            pass
    except ValidationError:
        pass


@receiver(post_save, sender=Countersign)
def countersign_post_save_handler(sender, instance, *args, **kwargs):
    change_contract_status(sender=None, instance=instance.contract)


@receiver(post_save, sender=Review)
def review_post_save_handler(sender, instance, *args, **kwargs):
    change_contract_status(sender=None, instance=instance.contract)


@receiver(post_save, sender=Sign)
def sign_post_save_handler(sender, instance, *args, **kwargs):
    change_contract_status(sender=None, instance=instance.contract)
