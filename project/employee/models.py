from django.db import models
from django.utils import timezone
import uuid
from django import forms
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class m_department(models.Model):
    name = models.CharField('所属部署', max_length=20, unique=True)
    created_at = models.DateTimeField('日付', default=timezone.now)

    def __str__(self):
        return self.name

class EmployeeManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class m_training(models.Model):
    training_name = models.CharField('トレーニング名', null=False,max_length=200, unique=True)
  
    def __str__(self):
        return self.training_name

class m_skill(models.Model):
    skill_name = models.CharField('スキル名', null=False, max_length=200, unique=True)

    def __str__(self):
        return self.skill_name

class Employee(AbstractBaseUser):
    # primary key繧貞､峨∴繧峨ｌ繧九・縺区､懆ｨｼ荳ｭ
    # id = models.IntegerField(primary_key=True,editable=False)
    # password = forms.CharField(widget=forms.PasswordInput)
    email = models.EmailField(
        verbose_name='メールアドレス',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField('生年月日')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField('名', max_length=20)
    last_name = models.CharField('姓', max_length=20)
    created_at = models.DateField('登録日', default=timezone.now)
    department = models.ForeignKey(m_department,verbose_name="所属部署",on_delete=models.PROTECT,null=True)
    training = models.ManyToManyField(m_training,verbose_name="トレーニング",blank=True)
    skill = models.ManyToManyField(m_skill,verbose_name="スキル",blank=True)

    objects = EmployeeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin