from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class PayHereUserManager(BaseUserManager):

    def base_create_user(self, email, name, phone, password):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone
        )

        user.set_password(password)
        return user

    def create_user(self, **kwargs):
        user = self.base_create_user(**kwargs)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        name = 'admin'
        phone = '010-0000-000'
        user = self.base_create_user(**kwargs,name=name,phone=phone)
        user.is_admin = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class PayHereUser(AbstractBaseUser):
    objects = PayHereUserManager()
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        error_messages={'unique': "이미 존재 하는 이메일 주소 입니다."}
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    date_added = models.DateTimeField(auto_now_add=True, null=True, db_index=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        pass

    def get_short_name(self):
        pass

    @property
    def is_staff(self):
       return self.is_admin

    def has_perm(self, perm, obj=None):
       return self.is_admin

    def has_module_perms(self, app_label):
       return self.is_admin

    @is_staff.setter
    def is_staff(self, value):
        self._is_staff = value
