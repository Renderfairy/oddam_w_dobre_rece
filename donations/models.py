from django.contrib.auth import get_user_model
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from . import enums


class Category(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    type = models.SmallIntegerField(choices=enums.OrganisationType.CHOICES, default=0)
    categories = models.ManyToManyField('Category', related_name='institutions')

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.SmallIntegerField()
    categories = models.ManyToManyField('Category', related_name='donations')
    institution = models.ForeignKey('Institution', on_delete=models.PROTECT, related_name='donations')
    address = models.CharField(max_length=64)
    phone_number = PhoneNumberField(null=False, blank=False)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=6)
    picup_date = models.DateField()
    picup_time = models.TimeField()
    picup_comment = models.TextField()
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.PROTECT)
    is_taken = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} {self.institution}'
