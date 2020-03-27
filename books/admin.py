from django.contrib.auth.admin import UserAdmin
from users.models import User
from django.contrib import admin
from .models import Author, Genre, Book, Chapter, Comment


class MyUserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('age', 'credit_Card', 'expired_Card')}),
    )


admin.site.register(User, MyUserAdmin)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Comment)
