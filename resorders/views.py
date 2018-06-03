import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from resorders.forms import OrderAddForm, ItemAddForm
from resorders.helpers import update_stock_product, update_total_order
from resorders.models import Order
from resusers.models import Customer

#
# def order_list(request):
#     orders = Order.objects.all()
#     page = request.GET.get('page', 1)
#     qpk = request.GET.get('qpk', '')
#     qemail = request.GET.get('qemail', '')
#     qtotal = request.GET.get('qtotal', '')
#
#     paginator = Paginator(orders, 3)
#     try:
#         orders = paginator.page(page)
#     except PageNotAnInteger:
#         orders = paginator.page(1)
#     except EmptyPage:
#         orders = paginator.page(paginator.num_pages)
#
#     return render(request, 'resorders/order/order_list.html', {
#         'orders': orders,
#         'page': page,
#         'qpk': qpk,
#         'qemail': qemail,
#         'qtotal': qtotal
#     })


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

        if form.is_valid() and all([item_form.is_valid() for item_form in items_form]):
            with transaction.atomic():
                order = form.save()
                for item_form in items_form:
                    item = item_form.save(commit=False)
                    update_stock_product(item.quantity, item.product)
                    item.order = order
                    item.save()

                update_total_order(order)

            return JsonResponse(json_body)
        else:
            err = {'order': None, 'items': None}
            if not all([item_form.is_valid() for item_form in items_form]):
                for i in [item_form.errors for item_form in items_form]:
                    if i:
                        return JsonResponse(i, safe=False, status=400)

            if not form.is_valid():
                return JsonResponse(form.errors, safe=False, status=400)

    else:
        pass


