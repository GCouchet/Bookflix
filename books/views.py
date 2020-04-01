from django.shortcuts import render, redirect
from .models import Author, Genre, Book, Chapter, Comment, FinishedBooks, Calification
from .forms import CommentForm, CalificationForm
from django.contrib.auth.decorators import login_required


def index(request):
    """Home page of library"""
    return render(request, 'books/index.html')


def books(request):
    """Show all books"""
    bookslst = Book.objects.order_by('title')
    context = {'books': bookslst}
    return render(request, 'books/books_list.html', context)


@login_required
def book(request, book_id):
    bk = Book.objects.get(id=book_id)
    chapters = Chapter.objects.filter(book=bk).order_by('num')
    comments = Comment.objects.filter(book=bk).order_by('date_added')
    comform = CommentForm
    finished = FinishedBooks.objects.get(user=request.user)
    calform = None
    if finished.books.filter(title=bk.title).exists():
        calform = CalificationForm
    genres = bk.genre.all().order_by('genre')
    context = {'book': bk, 'chapters': chapters, 'comments': comments,
               'calform': calform, 'comform': comform, 'genres': genres}
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


def search(request):
    search = request.GET.get('q')
    books = Book.objects.filter(title__icontains=search)
    authors = Author.objects.filter(name__icontains=search)
    genres = Genre.objects.filter(genre__icontains=search)
    context = {'search': search, 'books': books, 'authors': authors, 'genres': genres}
    return render(request, 'books/search.html', context)


def new_comment(request, book_id):
    book = Book.objects.get(id=book_id)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        new_comm = form.save(commit=False)
        new_comm.book = book
        new_comm.user = request.user
        new_comm.save()
    return redirect('books:book', book_id=book_id)


@login_required
def calification(request, book_id):
    book = Book.objects.get(id=book_id)
    old_cal = Calification.objects.filter(book=book, user=request.user).first()
    form = CalificationForm(data=request.POST)
    if form.is_valid():
        user_cal = int(request.POST.get('value'))
        votes = book.votes
        bk_cal = book.calif
        if not old_cal:
            new_cal = round(((bk_cal * votes) + user_cal) / (votes + 1), 1)
            book.votes = votes + 1
            new_ObjCalification = Calification(book=book, user=request.user, value=user_cal)
            new_ObjCalification.save()
        else:
            old_cal = old_cal.value
            new_cal = round((((bk_cal * votes) - old_cal + user_cal) / votes), 1)
            existent_calobj = Calification.objects.get(book=book, user=request.user)
            existent_calobj.value = user_cal
            existent_calobj.save()
        book.calif = new_cal
        book.save()
    return redirect('books:book', book_id=book_id)
