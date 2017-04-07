from market.models import Order, Comment


def handle_comment(request, order_id):
    """Add new comment to the shop and calculate new rating for the shop
    """
    # 
    order = Order.objects.get(id=order_id)
    order.has_commented = True
    order.save()

    # Handle the comment from the posted form
    new_comment = Comment()
    new_comment.customer = request.user
    new_comment.shop = order.get_seller()
    new_comment.body = request.POST['body']
    new_comment.save()

    # Calculate new rating
    rating = float(request.POST['rating'])
    shop = Order.objects.get(id=order_id).get_seller()
    shop.rating = (shop.sale_num * shop.rating + rating) / (shop.sale_num + 1)
    shop.save()
