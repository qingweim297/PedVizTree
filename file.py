from django.shortcuts import render, redirect


def file_list(request):

    return render(request,'file_list.html')

def upload_file(request):
    return render(request,'file_upload.html')

def delete_file(request):
    return redirect('file_list')

def edit_file(request):
    return render(request,'file_edit.html')