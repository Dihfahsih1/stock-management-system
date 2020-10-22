from django.shortcuts import render,redirect
from .forms import *
from django.http import HttpResponse
import csv
from django.contrib import messages
def home(request):
    context = {}
    return render(request, 'home.html', context)

def list_items(request):
    form = StockSearchForm(request.POST or None)
    qs = Stock.objects.all()
    header = 'List of all products'
    context = {'qs':qs,'header':header,"form": form,}
    if request.method == 'POST':
        qs = Stock.objects.filter(#category__icontains=form['category'].value(),
                                        item_name__icontains=form['item_name'].value()
                                        )

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = qs
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response
        context = {'qs':qs,'header':header,"form": form,}
        
    return render(request, 'list_items.html', context)
    
def add_item(request):
    form = StockCreateForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Saved')
            return redirect('list_items')
    context = {'form':form,'header':'Add Item'}
    return render(request, 'add_item.html', context)

def add_category(request):
    queryset = Category.objects.get(name=None)
    queryset.delete()
    form = CategoryForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Saved')
            return redirect('list_items')
    context = {'form':form,'header':'Create Item Category'}
    return render(request, 'add_category.html', context)
    

def update_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = StockUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = StockUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			return redirect('list_items')
	context = {
		'form':form,
        'header':'Update the Item details'
	}
	return render(request, 'add_item.html', context)

def delete_items(request, pk):
    
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Deleted Successfully')
        return redirect('list_items')
    context={'item':queryset}
    return render(request, 'delete_item.html', context)