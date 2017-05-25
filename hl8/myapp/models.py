from django.db import models
import datetime
from django import utils
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from please.settings import AUTH_USER_MODEL


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    phone = models.CharField(max_length=16, unique=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    region = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, unique=True)
    last_name = models.CharField(max_length=30, unique=True)
    USERNAME_FIELD = 'email'
    objects = UserManager()
    tmp_password = models.CharField(max_length=30, blank=True, null=True)
    flag_for_change = models.BooleanField(default=False)


class RoadMap(models.Model):
    rd_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    us = models.ForeignKey(User, related_name='roadmaps')

    def __str__(self):
        return self.name



class Task(models.Model):
    STATE_CHOICES = (('in progress', 'in progress'), ('ready', 'ready'),)
    title = models.CharField(max_length=100)
    state = models.CharField(max_length=11, choices=STATE_CHOICES, default='in progress')
    estimate = models.DateField(default=utils.timezone.now)
    my_id = models.AutoField(primary_key=True)
    road_map = models.ForeignKey(RoadMap, related_name='tasks')
    create_date = models.DateField(default=utils.timezone.now)

    class Meta:
        ordering = ['state', 'estimate']

    def calculate_points(self, max_estimate):
        if self.state == "ready":
            try:
                points = ((datetime.date.today() - self.create_date) / (self.estimate - self.create_date)) + (
                (self.estimate - self.create_date) / max_estimate)
                return points
            except ZeroDivisionError:
                return 0
        else:
            return 0


class Scores(models.Model):
    task = models.ForeignKey(Task)
    date = models.DateTimeField(default=utils.timezone.now())
    points = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        ordering = ['date']


class Account(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='accounts')
