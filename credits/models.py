from django.db import models
import uuid
from random import seed
from django.contrib.auth.models import User

class AccountBalance(models.Model):
    user = models.ForeignKey(User, on_delete='CASCADE')
    balance = models.FloatField(null=False, default=0)

    def __str__(self):
        return self.user.username


class Statement(models.Model):

    date = models.DateTimeField(auto_now=True)
    amount = models.CharField(max_length=10)
    transaction_id = models.CharField(max_length=12)
    user = models.CharField(max_length=30,null=False)

    def __str__(self):
        return str(self.user)


def random_transaction_id():
    seed()
    transaction_id = "ADD" + uuid.uuid4().hex[:9].upper()
    return transaction_id


class Pending_transactions(models.Model):
    transaction_date = models.DateTimeField(auto_now=True)
    key = models.CharField(max_length=12, default=0, unique=True)
    transaction_id = models.CharField(max_length=14, default=random_transaction_id())
    user = models.CharField(max_length=30,null=False)
    pending_amount = models.FloatField(null=False)

    def __str__(self):
        return str(self.user)


class Pending_redeem(models.Model):
    transaction_date = models.DateTimeField(auto_now=True)
    code = models.IntegerField(default=666781, unique=True)
    transaction_id = models.CharField(max_length=14, default=uuid.uuid4().hex[:12].upper())
    user = models.CharField(max_length=30,null=False)
    redeem_amount = models.FloatField(null=False)

    def __str__(self):
        return str(self.user)
