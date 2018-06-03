import json

from django import forms
from ast import literal_eval

from resorders.models import Order, Item
from resproducts.models import Product
from resusers.models import Customer


def validate_stock(items):
    try:
        for item in items:
            product = Product.objects.get(pk=item['product']['id'])

            if product.stock < item['quantity']:
                raise forms.ValidationError("Maaf untuk produk {} stok tidak mencukupi".format(product.name))
    except:
        raise forms.ValidationError("Pengecekan stok gagal.")


def validate_customer(order):
    pass


# class OrderAddForm(forms.Form):
#     order = forms.CharField(widget=forms.Textarea)
#     items = forms.CharField(widget=forms.Textarea)
#
#     def clean_order(self):
#         order = self.cleaned_data['order']
#         try:
#             order = literal_eval(order)
#             if isinstance(order, dict):
#                 if order:
#                     return order
#                 raise forms.ValidationError("Order tidak boleh kosong")
#             raise forms.ValidationError("Order harus berupa object")
#         except:
#             raise forms.ValidationError("Order tidak valid")
#
#     def clean_items(self):
#         items = self.cleaned_data['items']
#         try:
#             items = literal_eval(items)
#             if isinstance(items, list):
#                 if items:
#                     validate_stock(items)
#                     return items
#                 raise forms.ValidationError("Items tidak boleh kosong")
#             raise forms.ValidationError("Item harus berupa list")
#         except:
#             raise forms.ValidationError("Item tidak valid")



class OrderAddForm(forms.ModelForm):
    class Meta:
        fields = ('customer', 'total')
        model = Order


class ItemAddForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('product', 'price', 'quantity', 'subtotal')

    def clean_quantity(self):
        product = self.cleaned_data['product']
        quantity = self.cleaned_data['quantity']
        if product.stock < quantity:
            raise forms.ValidationError("Stok '{}' tidak mencukupi".format(product.name))
        return quantity

    # def clean(self):

