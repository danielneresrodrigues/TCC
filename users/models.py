from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group

class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class Status(models.Model):
    
    status = models.CharField(max_length = 20)

    def __str__(self):
        return (f'{self.status}')

class Tipo(models.Model):
    
    tipo = models.CharField(max_length = 20)

    def __str__(self):
        return (f'{self.tipo}')

class CustomUser(AbstractUser):

    objects = UserManager()

    first_name = models.CharField(max_length=120, verbose_name=_('first name'))
    last_name = models.CharField(max_length=120, verbose_name=_('last name'))

    cpf = models.CharField(max_length=11, verbose_name = 'CPF')

    username = None

    email = models.EmailField(verbose_name = _('email address'), unique=True)

    status = models.ForeignKey(Status, on_delete = models.PROTECT)
    tipo = models.ForeignKey(Tipo, on_delete = models.PROTECT)

    administrador = models.IntegerField(choices = ((0,'Não'),(1,'Sim')), default = 0)

    entrada = models.TimeField()
    saida = models.TimeField()
    almoco = models.TimeField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        admin = Group.objects.get(name = 'admin')

        if self.administrador:
            admin.user_set.add(self)
        else:
            admin.user_set.remove(self)

    def __str__(self):
        return (f'{self.first_name} {self.last_name}')