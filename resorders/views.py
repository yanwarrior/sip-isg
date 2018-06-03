import json

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from resorders.forms import OrderAddForm, ItemAddForm
from resusers.models import Customer


def order_list(request):
    pass

def order_confirm_add(request):
    pass

def order_add(request):
    context = {
        'url_ajax_category_list': reverse('resproducts:ajax_category_list'),
        'url_ajax_product_list': reverse('resproducts:ajax_product_list'),
        'url_ajax_customer_list': reverse('resusers:ajax_customer_list'),
        'url_ajax_order_add': reverse('resorders:ajax_order_add'),
    }
    return render(request, 'resorders/order/order_add.html', context)


@csrf_exempt
@transaction.atomic
def ajax_order_add(request):
    if request.is_ajax() and request.method == 'POST':
        json_body = json.loads(request.body.decode('utf-8'))
        form = OrderAddForm(json_body)
        items_form = [ItemAddForm(obj) for obj in json_body.get('items')]

        if form.is_valid() and all([item_form.is_valid for item_form in items_form]):
            with transaction.atomic():
                order = form.save()
                for item_form in items_form:
                    item = item_form.save(commit=False)
                    item.product.stock = item.product.stock - item.quantity
                    item.product.save()
                    item.order = order
                    item.save()

            return JsonResponse(json_body)
        else:
            return JsonResponse({"kesalahan": "Terjadi kesalahan saat melakukan order."}, status=400)

    else:
        pass


