from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class MyAccountManager(BaseUserManager):
    def create_user(self, phone_number, username, password=None):
        if not phone_number:
            raise ValueError("Foydalanuvchilar telefon raqamiga ega bo'lishi shart")
        if not username:
            raise ValueError("Foydalanuvchilar ism hamda familiyaga ega bo'lishi shart!")
        user = self.model(
            phone_number=phone_number,
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, username, password):
        user = self.create_user(
            phone_number=phone_number,
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class Account(AbstractBaseUser):

    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=13, unique=True)
    is_send_sms = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number',]

    objects = MyAccountManager()

    class Meta:
        verbose_name_plural = "Account"

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
