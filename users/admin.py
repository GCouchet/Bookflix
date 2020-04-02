from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Membership


class MyUserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('age', 'credit_Card', 'expired_Card', 'subscription')}),
    )

admin.site.register(User, MyUserAdmin)
admin.site.register(Membership)