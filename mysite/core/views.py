from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from .forms import BookForm
from .models import Book
import csv


class Home(TemplateView):
    template_name = 'home.html'


def upload(request):
    model = Book()
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        print(name)
        context['url'] = fs.url(name)
        with open('/Users/tomset/Documents/python/django-upload-example/media/'+uploaded_file.name, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                data = ', '.join(row)
            context['data'] = data
            model.id = context['data'][0]
            model.name = context['data'][1]
            model.author = context['data'][2]
            model.save()
    # return HttpResponse('test')
    # return render(request, 'upload.html', context)
    return render(request, 'upload.html', context)



def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {
        'books': books
    })


def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {
        'form': form
    })


def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')


class BookListView(ListView):
    model = Book
    template_name = 'class_book_list.html'
    context_object_name = 'books'


class UploadBookView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('class_book_list')
    template_name = 'upload_book.html'
