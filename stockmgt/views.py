from django.shortcuts import render

def home(request):
    context = {}
    return render(request, 'home.html', context)

def list_items(request):
    context = {}
    return render(request, 'list_items.html', context)