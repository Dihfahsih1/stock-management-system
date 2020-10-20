from django.shortcuts import render

def home(request):
    context = {}
    return render(request, 'home.html', context)

def list_items(request):
    qs = Stock.objects.all()
    context = {'qs':qs}
    return render(request, 'list_items.html', context)