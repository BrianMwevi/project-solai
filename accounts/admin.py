from django.contrib import admin
from accounts.models import Developer, Admin, User, Investor, Trader

admin.site.register(Trader)
admin.site.register(Investor)
admin.site.register(Admin)
admin.site.register(Developer)
