from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class PayHereUserManager(BaseUserManager):

    def base_create_user(self, email, name, phone, birthday, gender, password):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
            birthday=birthday,
            gender=gender
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
        user = self.base_create_user(**kwargs)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class PayHereUser(AbstractBaseUser):
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