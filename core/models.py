from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from portfolioLab import settings
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


ORG_TYPES = (
    ('Fundacja', 'Fundacja'),
    ('NGOs', 'NGOs'),
    ('Zbiórka', 'Zbiórka lokalna')
)


class Institution(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField()
    type = models.CharField(choices=ORG_TYPES,
                            default='Fundacja', max_length=15)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, default=None)
    is_taken = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quantity} dla {self.institution}'

    def get_taken_item_url(self):
        return reverse("core:taken", kwargs={
            'id': self.id
        })
