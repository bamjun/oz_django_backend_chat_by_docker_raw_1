from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)


# 유저를 생성하고 관리하는 역할
class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=30, unique=True)
    nickname = models.CharField(max_length=255)
    is_business = models.BooleanField(default=False)

    # 인증관련
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # 기존에 로그인 or 회원가입에 사용하던 username을 email로 대체하는 것
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return f"email : {self.email}, nickname : {self.nickname}"
