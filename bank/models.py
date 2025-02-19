from django.db import models
from django.contrib.auth.models import User, AbstractUser
from pydantic import BaseModel

# Create your models here.

class User(AbstractUser):

    name = models.CharField("Name", max_length=250, blank=True)
    state = models.CharField(max_length=100, blank=True)
    NAICS = models.CharField(max_length=100, blank=True)
    urbanrural = models.CharField(max_length=50, null = True, default=0)
    lowdoc = models.CharField(max_length=50, null = True, default=0)
    bank_loan = models.IntegerField(null = True, default=0)
    sba_loan = models.IntegerField(null = True, default=0)
    state = models.CharField("state", max_length=100, blank=True)
    state = models.CharField("state", max_length=100, blank=True)
    franchisecode = models.CharField(max_length=50, null = True, default=0)
    revlinecr = models.CharField(max_length=50, null = True, default=0)
    term = models.IntegerField(null = True, default=0)
    is_company = models.BooleanField(null = True, default=0)
    is_advisors = models.BooleanField(null = True, default=0)

class Loan_requests(models.Model):
    id_company









    