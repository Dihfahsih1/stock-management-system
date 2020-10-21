from django.shortcuts import render,redirect
from .forms import *
def home(request):
    context = {}
    return render(request, 'home.html', context)

def list_items(request):
    qs = Stock.objects.all()
    context = {'qs':qs}
    return render(request, 'list_items.html', context)

def add_item(request):
    form = StockCreateForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            form.save
            return redirect('list_items')
    context = {'form':form}
    return render(request, 'add_item.html', context)