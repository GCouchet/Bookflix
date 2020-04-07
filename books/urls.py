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
    path('search', views.search, name='search'),
    path('new_comment/<int:book_id>', views.new_comment, name='new_comment'),
    path('calification/<int:book_id>', views.calification, name='calification'),
    path('edit_comment/<int:comm_id>', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comm_id>', views.delete_comment, name='delete_comment'),
]