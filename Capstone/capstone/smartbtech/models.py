from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class Building(models.Model):
    building_no = models.AutoField(primary_key=True)
    building_name = models.CharField(max_length=255)

    def __str__(self):
        return self.building_name


class UsersManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    electrical_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsersManager()

    USERNAME_FIELD = 'username'

    @property
    def id(self):
        return self.electrical_id

    def __str__(self):
        return self.username


class SmartDevice(models.Model):
    device_id = models.AutoField(primary_key=True)
    device_name = models.CharField(max_length=255)

    def __str__(self):
        return self.device_name


class Reading(models.Model):
    reading_id = models.AutoField(primary_key=True)
    device = models.ForeignKey(SmartDevice, on_delete=models.CASCADE)
    voltage_consumption = models.FloatField()
    current_consumption = models.FloatField(default=0.0)
    power_consumption = models.FloatField()
    energy_consumption = models.FloatField(default=0.0)  # Add this field
    reading_timestamp = models.DateTimeField()

    def __str__(self):
        return f"Reading {self.reading_id} for {self.device}"


class BuildingIncharge(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    device = models.ForeignKey(SmartDevice, on_delete=models.CASCADE)

    def __str__(self):
        return f"Transaction {self.transaction_id}"
