from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,name, username, country, password=None):
        if not username:
            raise ValueError('Users must have an username')
        
        if not name:
            raise ValueError('Users must have a name')
        
        if not country:
            raise ValueError('Users must have a country')

        country_instance = Country.objects.get(id=country)

        user = self.model(
            name=name,
            username=username,
            country=country_instance,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name,country, username, password=None):
        user = self.create_user(
            username=username,
            name=name,
            country=country,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user
    

class Country(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


    def __str__(self):
        return self.name
    
class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name','country',]

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
class DocumentSet(models.Model):
    name = models.CharField(max_length=255)
    country = models.ManyToManyField(Country)
    has_backside = models.BooleanField(default=False)
    OCRLabels = models.JSONField()

    def __str__(self) -> str:
        return self.name
    
    def sides(self):
        if self.has_backside:
            return 'Both Side'
        
        return 'Front Side'