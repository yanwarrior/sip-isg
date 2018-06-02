import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from resusers.models import Customer


def ajax_customer_list(request):
    customers = Customer.objects.all()
    page = request.GET.get('page', 1)
    name = request.GET.get('name')

    if name:
        customers = customers.filter(name__contains=name)

    paginator = Paginator(customers, 2)

    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)

    json_context = [{
        'id': customer.id,
        'name': customer.name,
        'email': customer.email
    } for customer in customers]

    response = JsonResponse(json_context, safe=False)

    link = {
        'next': None,
        'prev': None
    }

    if customers.has_next():
        link['next'] = customers.next_page_number()
    else:
        link['next'] = None

    if customers.has_previous():
        link['prev'] = customers.previous_page_number()
    else:
        link['prev'] = None

    response['Link'] = json.dumps(link)

    return response



