from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Currency(models.Model):
    name = models.CharField(max_length=40)
    symbol = models.CharField(max_length=3)

    def __repr__(self):
        return self.name + " " + self.symbol

    def __str__(self):
        return self.name + " " + self.symbol

class  Country(models.Model):
    name=models.CharField(max_length=100)
    capital = models.CharField(max_length=50)
    wiki_link = models.URLField()
    currency = models.ForeignKey(Currency,null=True,on_delete=models.SET_NULL)

    def __repr__(self):
        return self.name + ' ' + self.capital + ' ' + self.currency.name

    def __str__(self):
        return self.name + ' ' + self.capital + ' ' + self.currency.name + ' ' + self.wiki_link

class Rates(models.Model):
    currency = models.ForeignKey(Currency,on_delete=models.CASCADE)
    x_currency = models.CharField(max_length=3)
    rate = models.FloatField(default=1.0)
    last_update_time = models.DateTimeField()

    def __repr__(self):
        return self.currency.symbol + " " + self.x_currency + " " + str(self.rate)

    def __str__(self):
        return self.currency.symbol + " " + self.x_currency + " " + str(self.rate)


from django.db import models


# Create your models here.

class Stock(models.Model):
    ticker = models.CharField(max_length=15)

    def __repr__(self):
        return self.ticker


class Exchange(models.Model):
    name = models.CharField(max_length=40)
    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=40)
    stock = models.ForeignKey(Stock, null=True, on_delete=models.SET_NULL)
    exchange = models.ForeignKey(Exchange, null=True, on_delete=models.SET_NULL)

    def __repr__(self):
        return self.name + " " + self.stock.ticker + " " + self.exchange.name

    def __str__(self):
        return self.name + " " + self.stock.ticker + " " + self.exchange.name

class AccountHolder(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    def __str__(self):
        return self.user.username
    def __repr__(self):
        return self.user.username


...
