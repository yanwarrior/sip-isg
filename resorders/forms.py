import json

from django import forms


class OrderAddForm(forms.Form):
    order = forms.CharField(widget=forms.Textarea)
    customer = forms.CharField(widget=forms.Textarea)
    items = forms.CharField(widget=forms.Textarea)

    def clean_order(self):
        order = self.cleaned_data['order']
        print(order)
        print(type(order))
        return order

    def clean_customer(self):
        customer = self.cleaned_data['customer']
        return customer

    def clean_items(self):
        from ast import literal_eval
        items = self.cleaned_data['items']
        print(literal_eval(items))
        try:
            items = literal_eval(items)
            if isinstance(items, list):
                print(type(items))
                if items:
                    return items
                raise forms.ValidationError("Items tidak boleh kosong")
            raise forms.ValidationError("Item harus berupa list")
        except ValueError:
            raise forms.ValidationError("Items harus berupa list")
        except:
            raise forms.ValidationError("Item tidak valid")

