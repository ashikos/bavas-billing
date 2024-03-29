import datetime
from django.db import models


class Bill(models.Model):

    """Model to store details of bills and create pdf
    """

    customer = models.CharField(
        max_length=200, default="", null=True, blank=True)
    amount = models.FloatField(default=0)
    reg_no = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(
        default=datetime.date.today(), null=True, blank=True)
    received = models.BooleanField(default=True)
    balance = models.FloatField(default=0)

    def __str__(self):
        return f'{self.id} - {self.customer}'


class Item(models.Model):
    """Model to store items in bill"""
    sale = models.ForeignKey(
        Bill, on_delete=models.CASCADE, null=True, blank=True,
            related_name="items")
    item = models.CharField(max_length=200, null=True, blank=True)
    amount = models.FloatField(default=0)


class Service(models.Model):
    """Service provided"""
    type = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.type}'


class Entries(models.Model):
    """Daily wash entries"""

    vehicle = models.CharField(max_length=200, null=True, blank=True)
    contact = models.CharField(max_length=200, null=True, blank=True)
    reg_no = models.CharField(max_length=200, null=True, blank=True)
    amount = models.FloatField(default=0, null=True, blank=True)
    remark = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    gpay = models.FloatField(default=0, null=True, blank=True)
    is_credit = models.BooleanField(default=False)
    is_credit_received = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id} - {self.vehicle} - {self.reg_no}'




