from django.shortcuts import render, redirect
from .models import Author, Genre, Book, Chapter, Comment


def index(request):
    """Home page of library"""
    return render(request, 'books/index.html')


def books(request):
    """Show all books"""
    bookslst = Book.objects.order_by('title')
    context = {'books': bookslst}
    return render(request, 'books/books_list.html', context)


def book(request, book_id):
    bk = Book.objects.get(id=book_id)
    chapters = Chapter.objects.filter(book=bk).order_by('num')
    comments = Comment.objects.filter(book=bk).order_by('date_added')
    context = {'book': bk, 'chapters': chapters, 'comments': comments}
    return render(request, 'books/book.html', context)


def chapter(request, chap_id):
    chap = Chapter.objects.get(id=chap_id)
    context = {'chapter': chap}
    return render(request, 'books/chapter.html', context)


def authors(request):
    authrs = Author.objects.order_by('name')
    context = {'authors': authrs}
    return render(request, 'books/authors.html', context)


def genres(request):
    gnres = Genre.objects.order_by('genre')
    context = {'genres': gnres}
    return render(request, 'books/genres.html', context)


def author(request, author_id):
    author = Author.objects.get(id=author_id)
    books = Book.objects.filter(author=author).order_by('title')
    context = {'author': author, 'books': books}
    return render(request, 'books/author.html', context)


def genre(request, genre_id):
    gnre = Genre.objects.get(id=genre_id)
    books = Book.objects.filter(genre=gnre).order_by('title')
    context = {'genre': gnre, 'books': books}
    return render(request, 'books/genre.html', context)