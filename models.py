from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email,first_name,last_name,address,password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            address=address,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email,first_name,last_name,address, password):
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            address=address,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email,first_name,last_name,address,password):
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            address=address,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.TextField()
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False) # a superuser

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','address',]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

class Collection(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    review_rating = models.IntegerField()
    review = models.TextField()
    favourite = models.BooleanField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Collection"

    def __str__(self):
        return self.title

