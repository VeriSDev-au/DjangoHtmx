from shoppingitems.models import UserShoppingItems


def get_max_order(user) -> int:
    return UserShoppingItems.objects.filter(user=user).count()
