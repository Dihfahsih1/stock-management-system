from django.shortcuts import render,redirect
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
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

def stock_detail(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"title": queryset.item_name,
		"queryset": queryset,
	}
	return render(request, "stock_details.html", context)

def issue_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = IssueForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.quantity -= instance.issue_quantity
		#instance.issue_by = str(request.user)
		messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
		instance.save()

		return redirect('/stock-detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": 'Issue ' + str(queryset.item_name),
		"queryset": queryset,
		"form": form,
		"username": 'Issue By: ' + str(request.user),
	}
	return render(request, "add_item.html", context)



def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity += instance.receive_quantity
        messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name)+"s now in Store")
        instance.save()
        return redirect('/stock-detail/'+str(instance.id))
    context = {
            "title": 'Reaceive ' + str(queryset.item_name),
            "instance": queryset,
            "form": form,
            "username": 'Receive By: ' + str(request.user),
        }
    return render(request, "add_item.html", context)