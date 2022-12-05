from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from global_utils.constants import GENDER_LIST
# Create your models here.


class AdvancedUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class AdvancedUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(_('Username'), unique=True, max_length=50)
    email = models.EmailField(_('Email address'), unique=True)
    first_name = models.CharField(_('First name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('Date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True, blank=True)
    is_staff = models.BooleanField(_('is_staff'), default=False, blank=True)
    is_blocked = models.BooleanField(_('is_blocked'), default=False, blank=True)
    login_attempts = models.PositiveSmallIntegerField(_('login attempts'), default=0, blank=True)

    objects = AdvancedUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('Users')

class Profile(models.Model):
    def upload_image(self, filename):
        return f'user_{self.user.id}/{filename}'

    DEFAULT_IMG = '../global_utils/img/unknown.png'

    user = models.OneToOneField('AdvancedUser', on_delete=models.CASCADE, related_name='profile')
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveIntegerField(choices=GENDER_LIST, default=None, null=True, blank=True)
    avatar = models.ImageField(upload_to=upload_image, default=DEFAULT_IMG)
    detail = models.OneToOneField('ProfileDetail',  on_delete=models.CASCADE, related_name='profile', 
    null=True, blank=True)


@receiver(post_save, sender=AdvancedUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.detail = ProfileDetail.objects.create()
        profile.save()
    
class ProfileDetail(models.Model):

    def upload_file(self, filename):
        return f'user_{self.profile.user.id}/{filename}'
    
    iin = models.CharField(max_length=12, null=True, blank=True)
    
    hospital = models.ForeignKey(
        'med_management.Hospital', on_delete=models.SET_NULL, related_name='doctor_profile', 
        null=True, blank=True)
    specialization = models.ForeignKey(
        'med_management.Specialization', on_delete=models.SET_NULL, related_name='doctor_profile',
        null=True, blank=True)
    license_file = models.FileField(upload_to=upload_file, blank=True, null=True)