from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.translation import gettext_lazy as _


# FlashSaleUser type
USER_TYPE_USER = 'USER'                     # user
USER_TYPE_OWNER = 'OWNER'                   # store owner
USER_TYPE_SUPERUSER = 'SUPERUSER'           # admin

USER_TYPE_CHOICES = (
    (USER_TYPE_USER, USER_TYPE_USER),
    (USER_TYPE_OWNER, USER_TYPE_OWNER),
    (USER_TYPE_SUPERUSER, USER_TYPE_SUPERUSER),
)


# Create your models here.
# django auth customization using AbstractBaseUser.
# please refer to https://docs.djangoproject.com/en/dev/topics/auth/customizing/#a-full-example
class FlashSaleUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        if password is not None:
            user.set_password(password)

        # If you want to use anther database for security then use user.save(using="another_database")."another_database" should be define in setting.py
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, password
        """
        user = self.create_user(
            email,
            password=password,
        )

        user.type = USER_TYPE_SUPERUSER
        user.save(using=self._db)

        return user


class FlashSaleUser(AbstractBaseUser):
    email = models.EmailField(verbose_name=_('Email Address'), max_length=255, unique=True, )
    display_name = models.CharField(verbose_name=_('Display Name'), max_length=255, null=True, )
    picture = models.URLField(verbose_name=_('Picture URL'), max_length=512, null=True)
    # is_active is checked in rest_framework_simplejwt.authentication.JWTAuthentication
    # if is_active is False, JWT Authentication failed
    is_active = models.BooleanField(verbose_name=_('User Active?'), default=True)
    type = models.CharField(verbose_name=_('User Type'), max_length=20, choices=USER_TYPE_CHOICES, default=USER_TYPE_USER)
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    objects = FlashSaleUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # "Does the user have a specific permission?"
        return True if self.is_active and self.type == USER_TYPE_SUPERUSER else False

    def has_module_perms(self, app_label):
        # Returns True if the user has permission to access models in the given app.
        return True if self.is_active and self.type == USER_TYPE_SUPERUSER else False

    @property
    def is_staff(self):
        # Returns True if the user is allowed to have access to the admin site.
        return True if self.is_active and self.type == USER_TYPE_SUPERUSER else False