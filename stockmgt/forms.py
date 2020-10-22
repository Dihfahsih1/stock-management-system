from django import forms
from .models import  *

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('This field is required')

        # for instance in Stock.objects.all():
        #     if instance.category == category:
        #         raise forms.ValidationError(category + ' is already created, choose a different name')
        return category

    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('This field is required')
        return item_name

class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    class Meta:
        model = Stock
        fields = ['category', 'item_name']

class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def clean_category(self):
        category_name = self.cleaned_data.get('name')
        if not category_name:
            raise forms.ValidationError('This field is required')

        for instance in Category.objects.all():
            if instance.name == category_name:
                raise forms.ValidationError(category_name + ' is already created, choose a different name')
        return category_name