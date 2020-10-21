from django.shortcuts import render,redirect
from .forms import *
def home(request):
    context = {}
    return render(request, 'home.html', context)

def list_items(request):
    form = StockSearchForm(request.POST or None)
    qs = Stock.objects.all()
    header = 'List of all products'
    if request.method == 'POST':
        qs = Stock.objects.filter(category__icontains=form['category'].value(),
                                        item_name__icontains=form['item_name'].value()
                                        )
        context = {'qs':qs,'header':header,"form": form,}

    context = {'qs':qs,'header':header,"form": form,}
    return render(request, 'list_items.html', context)

def add_item(request):
    form = StockCreateForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('list_items')
    context = {'form':form}
    return render(request, 'add_item.html', context)

def update_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = StockUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = StockUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			return redirect('list_items')

	context = {
		'form':form
	}
	return render(request, 'add_item.html', context)