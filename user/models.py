from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):

        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class Meta:
        db_table = 'User'
    
    username = models.CharField(
        verbose_name='username',
        max_length=128,
        unique=True,
    )

    rank = models.SmallIntegerField(
        default=1000,
    )
    
    win = models.PositiveIntegerField(default=0)
    lose = models.PositiveIntegerField(default=0)
    draw = models.PositiveIntegerField(default=0)

    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD='username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

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