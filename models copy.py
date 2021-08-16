from django.db import models
from django.utils import timezone
import uuid
from django import forms
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# カラムとして必要なものはすべて引数で持ってくる
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
        # カラムとして必要なものはすべて引数で持ってくる
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

class m_department(models.Model):
    department_id = models.IntegerField('id',primary_key=True)
    name = models.CharField('department_name',notnull=True)
    def __str__(self):
        return self.name

class m_training(models.Model):
    training_id = models.IntegerField('id',primary_key=True)
    training_name = models.CharField('training_name',notnull=True)
    members = models.ManyToManyField(
        "m_employee_detail",
        through="t_training_history",  # 追加
    )
    def __str__(self):
        return self.name

class m_skill(models.Model):
    skill_id = models.IntegerField('id',primary_key=True)
    skill_name = models.CharField('training_name',notnull=True)
    members = models.ManyToManyField(
        "m_employee_detail",
        through="t_skill_career",  # 追加
    )
    def __str__(self):
        return self.name

class t_training_history(models.Model):
    training_id = models.ForeignKey("m_training", on_delete=models.CASCADE)
    id = models.ForeignKey("m_employee_detail", on_delete=models.CASCADE)
    training_id = models.IntegerField('')
    def __str__(self):
        return self.name

class t_skill_career(models.Model):
    skill_career_id = models.IntegerField('id',primary_key=True)
    id = models.ForeignKey("m_training", on_delete=models.CASCADE)
    training_id = models.IntegerField('')
    def __str__(self):
        return self.name

class m_employee_detail(AbstractBaseUser):
    # primary keyを変えられるのか検証中
    pk = models.IntegerField(primary_key=True, default=uuid.uuid4, editable=False)
    password = forms.CharField(widget=forms.PasswordInput)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField('First Name', max_length=20)
    last_name = models.CharField('Last Name', max_length=20)
    created_at = models.DateField('Date Registered', default=timezone.now)

    objects = EmployeeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth',]

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