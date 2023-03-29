from django.db import models
import datetime

STRIKE_SIDE = (
    ("PUT", "Put"),
    ("CALL", "Call"),
)


class TickerTypes(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class StrikeSideMaster(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class TickerName(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    symbol = models.CharField(max_length=255, null=True, blank=True)
    date_of_listing = models.CharField(max_length=255, null=True, blank=True)
    series = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Trades(models.Model):
    ticker_type = models.ForeignKey(TickerTypes, null=True, blank=True, on_delete=models.DO_NOTHING)
    ticker_name = models.CharField(max_length=255, null=True, blank=True)
    entry_price = models.BigIntegerField(null=True, blank=True)
    exit_price = models.BigIntegerField(null=True, blank=True)
    target_price = models.BigIntegerField(null=True, blank=True)
    stop_loss = models.BigIntegerField(null=True, blank=True)
    strike_side = models.ForeignKey(StrikeSideMaster, on_delete=models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_sl = models.BooleanField(null=True, blank=True)
    is_target = models.BooleanField(null=True, blank=True)
    is_exit_between = models.BooleanField(null=True, blank=True)
    symbol = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.ticker_name)