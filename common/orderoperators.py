from market.models import Order, Shop, Food


def create_order(request):
    new_order = Order(customer=request.user, status='paid')
    new_order.save()
    shop = Shop()

    for food_name, food_id in request.POST.items():
        if food_name != 'csrfmiddlewaretoken':
            food = Food.objects.get(id=food_id)
            shop = food.seller
            new_order.food_list.add(food)
            food.sale_num += 1
            food.save()

    # The sales volume of this shop has accordingly increased by 1
    shop.sale_num += 1
    shop.save()


def accept_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'accepted'
    order.save()


def finish_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'finished'
    order.save()


def fetch_orders_for_customer(request):
    # Get orders with status 'paid'
    paid_orders = Order.objects.filter(
        customer=request.user,
        status='paid',
    ).order_by('-time')

    # Get orders with status 'accepted'
    accepted_orders = Order.objects.filter(
        customer=request.user,
        status='accepted',
    ).order_by('-time')

    # Get orders with status 'finished'
    finished_orders = Order.objects.filter(
        customer=request.user,
        status='finished',
    ).order_by('-time')

    return paid_orders, accepted_orders, finished_orders


def fetch_orders_for_shop(request):
    '''Helps to fetch orders with different status of one shop'''
    shop = request.user.shop

    new_orders = Order.objects.filter(
        food_list__seller__name=shop.name,
        status='paid',
    ).distinct().order_by('-time')

    accepted_orders = Order.objects.filter(
        food_list__seller__name=shop.name,
        status='accepted',
    ).distinct().order_by('-time')

    finished_orders = Order.objects.filter(
        food_list__seller__name=shop.name,
        status='finished',
    ).distinct().order_by('-time')

    return new_orders, accepted_orders, finished_orders
