from django.shortcuts import render, redirect
from .models import Author, Genre, Book, Chapter, Comment, FinishedBooks, Calification
from .forms import CommentForm, CalificationForm
from django.contrib.auth.decorators import login_required
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io


def verificateUser(funcion):

    def verificate(req):
        if not req.user.is_authenticated:
            return redirect('users:login')
        else:
            #acá deje preparado el if para la falta de pago para cuando esté el atributo ya validado
            #if !(req.user.expiredPay < datetime.now)
            #    return render(req, 'restrictions/needPayment.html')
            if 'myProfile' in req.session:
                #profile = req.session.get['myProfile']
                return funcion(req)
            else:
                return redirect('profiles:selectProfile')

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
    comform = CommentForm
    finished = FinishedBooks.objects.get(user=request.user)
    calform = None
    if finished.books.filter(title=bk.title).exists():
        calform = CalificationForm
    genres = bk.genre.all().order_by('genre')
    context = {'book': bk, 'chapters': chapters, 'comments': comments,
               'calform': calform, 'comform': comform, 'genres': genres}
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
    form = CommentForm(data=request.POST)
    if form.is_valid():
        new_comm = form.save(commit=False)
        new_comm.book = book
        new_comm.user = request.user
        new_comm.save()
    return redirect('books:book', book_id=book_id)


@verificateUser
def calification(request, book_id):
    book = Book.objects.get(id=book_id)
    old_cal = Calification.objects.filter(book=book, user=request.user).first()
    form = CalificationForm(data=request.POST)
    if form.is_valid():
        user_cal = int(request.POST.get('value'))
        if not old_cal:
            new_ObjCalification = Calification(book=book, user=request.user, value=user_cal)
            new_ObjCalification.save()
        else:
            existent_calobj = Calification.objects.get(book=book, user=request.user)
            existent_calobj.value = user_cal
            existent_calobj.save()
        book.calif = sum(map(lambda x: x.value, Calification.objects.filter(book=book))) / len(Calification.objects.filter(book=book))
        book.save()
    return redirect('books:book', book_id=book_id)