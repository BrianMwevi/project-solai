from django.contrib import admin
from accounts.models import User, Admin, Investor, Trader

# Register your models here.
admin.site.register(User)
admin.site.register(Trader)
admin.site.register(Investor)
admin.site.register(Admin)
