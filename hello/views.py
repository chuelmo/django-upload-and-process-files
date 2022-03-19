from django.shortcuts import render, redirect
from django.conf import settings
from django.http import Http404, FileResponse
import os
from .forms import FileUploadModelForm
from .models import Greeting, File
from .procesar_csv import procesarCSV


def index(request):
    return render(request, "index.html")

def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, "db.html", {"greetings": greetings})

def view_404(request, exception=None):
    return redirect("/")

def file_list(request):
    files = File.objects.all().order_by("-id")
    deletedFiles = False
    for f in files:
        if not f.file.storage.exists(f.file.name):
            f.delete()
            deletedFiles = True
    if deletedFiles:
        files = File.objects.all().order_by("-id")
    return render(request, 'file_list.html', {'files': files})

def model_form_upload(request):
    if request.method == "POST":
        form = FileUploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/file/")
    else:
        form = FileUploadModelForm()
    return render(request, 'upload_form.html', {'form': form, 'heading': 'Subir csv para agregarle los Sizes'})

def file_response_download(request, id):
    file = File.objects.get(pk=id)
    file_path = file.file.url[1:]
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    ext = os.path.basename(file_path).split('.')[-1].lower()
    if ext in ['csv']:
        todoOK = procesarCSV(os.path.join(media_root, 'files', os.path.basename(file.file.url)))
        if todoOK[0] == 'OK':
            response = FileResponse(open(file_path, 'rb'))
            response['content_type'] = "application/octet-stream"
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
        else:
            return render(request, 'errors_list.html', {'errors': todoOK})
    else:
        raise Http404

def model_delete(request):
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    records = File.objects.all()
    for f in records:
        fileName = os.path.join(media_root, 'files', os.path.basename(f.file.url))
        if os.path.isfile(fileName):
            os.remove(fileName)
    records.delete()
    return render(request, 'file_list.html', {'files': records})