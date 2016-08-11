from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import os
import shutil


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, nickname, email_address, password, **extra_fields):
        """
        Creates and saves a User with the given nickname, email and password.
        """
        if not nickname:
            raise ValueError('The given nickname must be set')
        email_address = self.normalize_email(email_address)
        user = self.model(nickname=nickname, email_address=email_address, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, nickname, email_address=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(nickname, email_address, password, **extra_fields)

    def create_superuser(self, nickname, email_address, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(nickname, email_address, password, **extra_fields)


def upload_to(instance, filename):
    name_without_extension, extension = filename.split(".")
    # if a user with sign-in email = user@email.com uploads file name.png
    # the file will be store at media/portrait/user@email.com/portrait.png
    return '{0}/{1}/{2}.{3}'.format("portrait", instance.email_address, "portrait", extension)


class User(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField(max_length=254, unique=True)

    email_address = models.EmailField(max_length=254, unique=True)

    # field "password" inherited from AbstractBaseUser

    following_users = models.ManyToManyField("User", related_name="follower_set", blank=True, symmetrical=False)

    level = models.IntegerField(default=0)

    portrait = models.ImageField(upload_to=upload_to, blank=True, null=True)

    @property
    def portrait_url(self):
        if self.portrait and hasattr(self.portrait, 'url'):
            return self.portrait.url[1:]
        else:
            return "media/portrait/default_portrait.png"

    USERNAME_FIELD = "email_address"

    REQUIRED_FIELDS = ["nickname"]

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=True,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    def get_full_name(self):
        return self.nickname + "<" + self.email_address + ">" + "level:" + str(self.level) + " superuser:" + str(self.is_superuser) + " staff:" + str(self.is_staff)

    def get_short_name(self):
        return self.nickname

    def set_nickname(self, nickname):
        self.nickname = nickname

    def set_email_address(self, email_address):
        self.email_address = email_address

    # set_password method inherited from super class

    def __unicode__(self):
        return self.get_full_name()


@receiver(models.signals.pre_delete, sender=User)
# "sender" and "**kwargs" are required though they are of no use here, do not delete them
def delete_local_portrait(sender, instance, **kwargs):
    # delete the local image files for this user's portrait
    if instance.portrait and hasattr(instance.portrait, 'url'):
        portrait = instance.portrait
        img_local_location = portrait.storage.path(portrait)
        img_local_dirname, file_name_and_extension = os.path.split(img_local_location)

        if os.path.isdir(img_local_dirname):
            shutil.rmtree(img_local_dirname)