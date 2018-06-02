import json

from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from resorders.forms import OrderAddForm


def order_add(request):
    context = {
        'url_ajax_category_list': reverse('resproducts:ajax_category_list'),
        'url_ajax_product_list': reverse('resproducts:ajax_product_list'),
        'url_ajax_customer_list': reverse('resusers:ajax_customer_list'),
        'url_ajax_order_add': reverse('resorders:ajax_order_add'),
    }
    return render(request, 'resorders/order/order_add.html', context)


@csrf_exempt
def ajax_order_add(request):
    if request.is_ajax() and request.method == 'POST':
        json_body = json.loads(request.body.decode('utf-8'))
        form = OrderAddForm(json_body)

        if form.is_valid():
            return JsonResponse(json.loads(request.body.decode('utf-8')), safe=False)
        return JsonResponse(form.errors, safe=False, status=400)

    else:
        pass


