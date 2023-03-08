from django.contrib import admin
from .models import TickerTypes, Trades, TickerName, StrikeSideMaster, Trades


admin.site.register(TickerTypes)
admin.site.register(StrikeSideMaster)
admin.site.register(Trades)
admin.site.register(TickerName)