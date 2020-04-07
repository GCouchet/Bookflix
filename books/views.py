from django.shortcuts import render, redirect
from .models import Author, Genre, Book, Chapter, Comment, FinishedBooks, Calification
from profiles.models import Profile
from .forms import CommentForm, CalificationForm
from django.contrib.auth.decorators import login_required
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from django.http import Http404
import io


def verificateUser(funcion):
    def verificate(req, **kwargs):
        if not req.user.is_authenticated:
            return redirect('users:login')
        else:
            #acá deje preparado el if para la falta de pago para cuando esté el atributo ya validado
            #if !(req.user.expiredPay < datetime.now)
            #    return render(req, 'restrictions/needPayment.html')
            if req.session['myProfile'] is None:                #profile = req.session.get['myProfile']
                return redirect('profiles:selectProfile')
            else:
                return funcion(req, **kwargs)
    return verificate


@verificateUser
def index(request):
    """Home page of library"""
    return render(request, 'books/index.html')


@verificateUser
def books(request):
    """Show all books"""
    bookslst = Book.objects.order_by('title')
    context = {'books': bookslst}
    return render(request, 'books/books_list.html', context)


@verificateUser
def book(request, book_id):
    bk = Book.objects.get(id=book_id)
    chapters = Chapter.objects.filter(book=bk).order_by('num')
    comments = Comment.objects.filter(book=bk).order_by('date_added')
    prof = Profile.objects.get(id=request.session['myProfile'])
    finished = FinishedBooks.objects.filter(profile=prof)
    calform = None
    comform = None
    if finished.filter(books=bk).exists():
        calform = CalificationForm
        if not Comment.objects.filter(book=bk, profile=prof).exists():
            comform = CommentForm
    genres = bk.genre.all().order_by('genre')
    context = {'book': bk, 'chapters': chapters, 'comments': comments,
               'calform': calform, 'comform': comform, 'genres': genres, 'profile': prof}
    return render(request, 'books/book.html', context)


@verificateUser
def chapter(request, chap_id):

    def convert_pdf_to_txt(path):
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=laparams)
        fp = open(path, 'rb')

        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                      password=password,
                                      caching=caching,
                                      check_extractable=True):
            interpreter.process_page(page)

        fp.close()
        device.close()
        text = retstr.getvalue()
        retstr.close()

        return text

    chap = Chapter.objects.get(id=chap_id)
    try:
        cont = convert_pdf_to_txt(str(chap.text))
    except:
        cont = 'No se pudo cargar el contenido del capítulo.'
    context = {'chapter': chap, 'cont': cont}
    return render(request, 'books/chapter.html', context)


@verificateUser
def authors(request):
    authrs = Author.objects.order_by('name')
    context = {'authors': authrs}
    return render(request, 'books/authors.html', context)


@verificateUser
def genres(request):
    gnres = Genre.objects.order_by('genre')
    context = {'genres': gnres}
    return render(request, 'books/genres.html', context)


@verificateUser
def author(request, author_id):
    author = Author.objects.get(id=author_id)
    books = Book.objects.filter(author=author).order_by('title')
    context = {'author': author, 'books': books}
    return render(request, 'books/author.html', context)


@verificateUser
def genre(request, genre_id):
    gnre = Genre.objects.get(id=genre_id)
    books = Book.objects.filter(genre=gnre).order_by('title')
    context = {'genre': gnre, 'books': books}
    return render(request, 'books/genre.html', context)


@verificateUser
def search(request):
    search = request.GET.get('q')
    books = Book.objects.filter(title__icontains=search)
    authors = Author.objects.filter(name__icontains=search)
    genres = Genre.objects.filter(genre__icontains=search)
    context = {'search': search, 'books': books, 'authors': authors, 'genres': genres}
    return render(request, 'books/search.html', context)


@verificateUser
def new_comment(request, book_id):
    book = Book.objects.get(id=book_id)
    prof = Profile.objects.get(id=request.session['myProfile'])
    if not FinishedBooks.objects.filter(books=book, profile=prof).exists() or Comment.objects.filter(book=book, profile=prof).exists():
        return redirect('books:book', book_id=book_id)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        new_comm = form.save(commit=False)
        new_comm.book = book
        new_comm.profile = prof
        new_comm.save()
    return redirect('books:book', book_id=book_id)


@verificateUser
def calification(request, book_id):
    book = Book.objects.get(id=book_id)
    prof = Profile.objects.get(id=request.session['myProfile'])
    if not FinishedBooks.objects.filter(book=book, profile=prof).exists():
        return redirect('books:book', book_id=book_id)
    old_cal = Calification.objects.filter(book=book, profile=prof).first()
    form = CalificationForm(data=request.POST)
    if form.is_valid():
        user_cal = int(request.POST.get('value'))
        if not old_cal:
            new_ObjCalification = Calification(book=book, profile=prof, value=user_cal)
            new_ObjCalification.save()
        else:
            existent_calobj = Calification.objects.get(book=book, profile=prof)
            existent_calobj.value = user_cal
            existent_calobj.save()
        book.calif = sum(map(lambda x: x.value, Calification.objects.filter(book=book))) / len(Calification.objects.filter(book=book))
        book.save()
    return redirect('books:book', book_id=book_id)


@verificateUser
def edit_comment(request, comm_id):
    prof = Profile.objects.get(id=request.session['myProfile'])
    comment = Comment.objects.get(id=comm_id)
    if comment.profile != prof:
        raise Http404
    if request.method != 'POST':
        form = CommentForm(instance=comment)
    else:
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('books:book', book_id=comment.book.id)
    context = {'comment': comment, 'form': form}
    return render(request, 'books/edit_comment.html', context)


@verificateUser
def delete_comment(request, comm_id):
    comm = Comment.objects.get(id=comm_id)
    if request.session['myProfile'] != comm.profile.id:
        raise Http404
    book = comm.book
    comm.delete()
    return redirect('books:book', book_id=book.id)
