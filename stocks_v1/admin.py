from django.contrib import admin
from stocks_v1.models import Stock

from simple_history.admin import SimpleHistoryAdmin


class StockHistoryAdmin(SimpleHistoryAdmin):
    
    history_list_display = ['open', 'price', 'change', 'high', 'low']


admin.site.register(Stock, StockHistoryAdmin)
