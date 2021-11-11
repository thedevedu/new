from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from myadmin.models import Region, Languages

class UserManager(BaseUserManager):

    # create_user이나 create_superuser에서 self.model, self.create_user 모두는 필수적인 argument로 작용함
    def create_user(self, email, password=None):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        """
        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여한다. 
        """
        user = self.create_user(
            email=email,
            password=password
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(
        primary_key=True
    )
    user_id = models.CharField(
        max_length=255, unique=True, editable=False
    )
    is_active = models.BooleanField(
        verbose_name=_('Is active'), default=True
    )
    email = models.EmailField(
        verbose_name=_('Email address'), max_length=255, unique=True,
    )
    nickname = models.CharField(
        verbose_name=_('nickname'), max_length=30
    )
    name = models.CharField(
        verbose_name=_('name'), max_length=30
    )
    region = models.ForeignKey(
        Region, on_delete=models.SET_NULL, null=True
    )
    language = models.CharField(
        verbose_name=_('language'), max_length=100
    )
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        verbose_name=_('date_joined'), default=timezone.now
    )
    date_latest = models.DateTimeField(
        verbose_name=_('date_latest'), default=timezone.now
    )
    auth_token = models.CharField(max_length=100, null=True)
    # 이 필드는 레거시 시스템 호환을 위해 추가할 수도 있다.
    salt = models.CharField(
        verbose_name=_('Salt'), max_length=10, blank=True
    )
    addition1 = models.CharField(
        max_length=100, null=True
    )
    addition2 = models.CharField(
        max_length=100, null=True
    )
    addition3 = models.CharField(
        max_length=100, null=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    
    # createsuperuser에서도 반드시 요구하게 됨
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-date_joined',)

    def __str__(self):
        return self.email

    def get_full_name(self):        
        return self.email

    def get_short_name(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All superusers are staff
        return self.is_superuser

    get_full_name.short_description = _('User')
