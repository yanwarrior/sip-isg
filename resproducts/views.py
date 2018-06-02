import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render

from resproducts.models import Category, Product


def ajax_category_list(request):
    categories = Category.objects.all()
    page = request.GET.get('page', 1)
    name = request.GET.get('name')

    if name:
        categories = categories.filter(name__contains=name)

    paginator = Paginator(categories, 2)

    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    json_context = [{
        'id': category.id,
        'name': category.name
    } for category in categories]

    response = JsonResponse(json_context, safe=False)

    link = {
        'next': None,
        'prev': None
    }

    if categories.has_next():
        link['next'] = categories.next_page_number()
    else:
        link['next'] = None

    if categories.has_previous():
        link['prev'] = categories.previous_page_number()
    else:
        link['prev'] = None

    response['Link'] = json.dumps(link)

    return response


def ajax_product_list(request):
    products = Product.objects.all()
    page = request.GET.get('page', 1)
    name = request.GET.get('name')
    category_id = request.GET.get('category_id')

    if category_id:
        products = products.filter(category__pk=category_id)

    if name:
        products = products.filter(name__contains=name)

    paginator = Paginator(products, 2)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    json_context = [{
        'id': product.id,
        'name': product.name,
        'category': {
            'id': product.category.id,
            'name': product.category.name
        },
        'price': product.price,
        'stock': product.stock
    } for product in products]

    response = JsonResponse(json_context, safe=False)

    link = {
        'next': None,
        'prev': None
    }

    if products.has_next():
        link['next'] = products.next_page_number()
    else:
        link['next'] = None

    if products.has_previous():
        link['prev'] = products.previous_page_number()
    else:
        link['prev'] = None

    response['Link'] = json.dumps(link)

    return response
