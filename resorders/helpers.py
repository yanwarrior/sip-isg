from resorders.models import Item


def update_stock_product(quantity, product):
    product.stock = product.stock - quantity
    product.save()
    return product


def update_total_order(order):
    items = Item.objects.filter(order=order)
    summary = sum([item.subtotal for item in items])
    order.total = summary
    order.save()