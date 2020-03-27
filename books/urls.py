from django.urls import path
from . import views

app_name = 'books'
urlpatterns = [
    path('', views.index, name='index'),
    path('books_list/', views.books, name='books_list'),
    path('books_list/<int:book_id>/', views.book, name='book'),
    path('chapter/<int:chap_id>', views.chapter, name='chapter'),
    path('authors/', views.authors, name='authors'),
    path('authors/<int:author_id>/', views.author, name='author'),
    path('genres/', views.genres, name='genres'),
    path('genres/<int:genre_id>/', views.genre, name='genre'),
]
