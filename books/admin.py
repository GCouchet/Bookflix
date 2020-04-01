from django.contrib import admin
from .models import Author, Genre, Book, Chapter, Comment, Publisher, FinishedBooks, Calification, ReadingBook


admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Comment)
admin.site.register(Publisher)
admin.site.register(FinishedBooks)
admin.site.register(Calification)
admin.site.register(ReadingBook)
