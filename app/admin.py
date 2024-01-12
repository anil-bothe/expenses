from django.contrib import admin

from app.models import Balance, Expense, User, Roles

admin.site.register(Balance)
admin.site.register(Expense)
admin.site.register(User)
admin.site.register(Roles)