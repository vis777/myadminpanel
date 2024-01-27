from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from myapp.models import Author,Book
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.serializers import AuthorSerializer, BookSerializer
from django.http import HttpResponseRedirect
# Correct import statement

# Create your views here.
def indexpage(request):
    return render(request, "index.html")

def admin_login(request):
    return render(request,"AdminLogin.html")
def adminlogin(request):
    if request.method == "POST":
        un = request.POST.get('user_name')
        pwd = request.POST.get('pass_word')
        if User.objects.filter(username__contains=un).exists():
            x = authenticate(username=un, password=pwd)
            if x is not None:
                login(request, x)
                request.session['username'] = un
                request.session['password'] = pwd

                # Directly assign the success message to messages dictionary
                messages.success(request, "Login successful")

                return redirect(indexpage)
            else:
                messages.error(request, "Invalid Username or Password")
                return redirect(admin_login)
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect(admin_login)
def admin_logout(request):
    del request.session['username']
    messages.success(request, "Logout successfull")
    return redirect(admin_login)

def authorpage(request):
    return render(request, "Add Author.html")
def saveauthor(request):
    if request.method == "POST":
        ana = request.POST.get('aname')
        obj = Author(name=ana)

        obj.save()
        messages.success(request, "Author added successfully!")
        return redirect(authorpage)

def author_display(request):
    query = request.GET.get('q')
    aut = Author.objects.all()
    if query:
        aut = aut.filter(Q(name__icontains=query))

    paginator = Paginator(aut, 10)
    page = request.GET.get('page')

    try:
        aut = paginator.page(page)
    except PageNotAnInteger:
        aut = paginator.page(1)
    except EmptyPage:
        aut = paginator.page(paginator.num_pages)

    return render(request, 'DisplayAuthor.html', {'aut': aut, 'query': query})

def deleteauthor(request, dataid):
    cats = Author.objects.filter(id=dataid)
    cats.delete()
    return redirect(author_display)

def bookpage(request):
    authdis = Author.objects.all()
    return render(request,"Add Book.html", {'authdis':authdis})

def savebook(request):
    if request.method == "POST":
        ath = request.POST.get('authorname')
        tna = request.POST.get('tname')
        pri = request.POST.get('price')
        obj = Book(author=ath, title=tna, price=pri)
        obj.save()
        messages.success(request, "Book added successfully...!")
        return redirect(bookpage)


def book_display(request):
    query = request.GET.get('q')
    books = Book.objects.all()

    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))

    page = request.GET.get('page', 1)
    paginator = Paginator(books, 10)  # Show 10 books per page
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    return render(request, 'DisplayBook.html', {'books': books, 'query': query})

def editbook(request,dataid):
    aut = Author.objects.all()
    books = Book.objects.get(id=dataid)
    return render(request,"EditBook.html",{'aut':aut, 'books':books})
def updatebook(request, dataid):
    if request.method == "POST":
        au = request.POST.get('aname')
        tnam = request.POST.get('tnam')
        pr = request.POST.get('price')

        Book.objects.filter(id=dataid).update(author=au, title=tnam, price=pr)
        return redirect(book_display)
def deletebook(request, dataid):
    books = Book.objects.filter(id=dataid)
    books.delete()
    return redirect(book_display)
class AuthorListAPIView(APIView):
    def get(self, request):
        query = request.GET.get('q')
        authors = Author.objects.all()
        if query:
            authors = authors.filter(name__icontains=query)
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

class BookListAPIView(APIView):
    def get(self, request):
        query = request.GET.get('q')
        books = Book.objects.all()
        if query:
            books = books.filter(title__icontains=query) | books.filter(author__name__icontains=query)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)