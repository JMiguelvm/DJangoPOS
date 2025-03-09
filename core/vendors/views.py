from django.shortcuts import render

def index(request):
    return render(request, "vendors/index.html")

def edit(request):
    return render(request, "vendors/edit.html")

def create(request):
    return render(request, "vendors/create.html")