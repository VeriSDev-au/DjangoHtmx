from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import UserShoppingItems, ShoppingItem
from django.conf import settings
from shoppingitems.utils import get_max_order


class IndexView(TemplateView):
    template_name = "shopping.html"


class AboutView(TemplateView):
    template_name = "about.html"


class ShoppingListView(ListView):
    template_name = "shopping.html"
    model = UserShoppingItems
    paginate_by = settings.PAGINATE_BY
    context_object_name = "usershoppingitems"

    def get_queryset(self):
        """Overide the queryset to filter based on the login user"""
        return UserShoppingItems.objects.filter(user_id=self.request.user.id)


def add_shoppingitem_and_usershoppingitem(request):
    """After using typing a new shopping item and since no history result
    found then user can press the add button which will add the record
    in both shopping item and user shopping item.
    """

    name = request.POST.get("shoppingitemname")

    currentshoppingitems = ShoppingItem.objects.filter(name=name)

    if currentshoppingitems.count() == 0:
        shoppingitem = ShoppingItem(name=name)
        shoppingitem.save()
    else:
        shoppingitem = currentshoppingitems.first()

    maxorder = get_max_order(request.user)
    UserShoppingItems.objects.create(
        shoppingitem=shoppingitem, user_id=request.user.id, order=maxorder + 1
    )

    usershoppingitems = UserShoppingItems.objects.filter(user_id=request.user.id)

    return render(
        request,
        "partials/shopping-list-check-list.html",
        {"usershoppingitems": usershoppingitems},
    )


def add_usershoppingitem(request, pk):
    shoppingitem = ShoppingItem.objects.get(id=pk)

    maxorder = get_max_order(request.user)

    UserShoppingItems.objects.create(
        shoppingitem=shoppingitem, user_id=request.user.id, order=maxorder + 1
    )

    usershoppingitems = UserShoppingItems.objects.filter(user_id=request.user.id)

    return render(
        request,
        "partials/shopping-list-check-list.html",
        {"usershoppingitems": usershoppingitems},
    )


def del_usershoppingitem(request, pk):
    """remove the shopping item from shopping list"""

    request.user.shoppingitems.remove(pk)

    usershoppingitem = UserShoppingItems.objects.get(id=pk)
    usershoppingitem.delete()

    usershoppingitems = UserShoppingItems.objects.filter(user_id=request.user.id)

    return render(
        request,
        "partials/shopping-list-check-list.html",
        {"usershoppingitems": usershoppingitems},
    )


def put_usershoppingitem(request, pk):
    """update usershoppingitem check field when user check the shopping item"""

    usershoppingitem = UserShoppingItems.objects.get(id=pk)

    if request.POST.get("shoppingflag") is None:
        usershoppingitem.checked = False
    else:
        usershoppingitem.checked = True

    usershoppingitem.save()

    usershoppingitems = UserShoppingItems.objects.filter(user_id=request.user.id)

    return render(
        request,
        "partials/shopping-list-check-list.html",
        {"usershoppingitems": usershoppingitems},
    )


def sort_usershoppingitem(request):
    """sorting the data after user drag and drop the usershopping list"""

    usershoppingitem_pks_order = request.POST.getlist("shoppingitem_order")

    usershoppingList = []

    for idx, usershoppingitem_pk in enumerate(usershoppingitem_pks_order, start=1):
        usershoppingitem = UserShoppingItems.objects.get(pk=usershoppingitem_pk)
        usershoppingitem.order = idx
        usershoppingitem.save()
        usershoppingList.append(usershoppingitem)

    return render(
        request,
        "partials/shopping-list-check-list.html",
        {"usershoppingitems": usershoppingList},
    )


def del_shoppingitem(request, pk):
    """remove the shopping item from the search result group list"""

    shoppingitem = ShoppingItem.objects.get(id=pk)
    shoppingitem.delete()

    return render(
        request,
        "partials/shopping-list-search-script-refresh.html",
    )


def get_shoppingitem(request):
    """populate shopping item result when user typing the new shopping item"""

    text_search = request.GET.get("shoppingitemname")

    shoppingitemsearchresults = None

    if len(text_search.strip()) != 0:
        usershoppingitems = request.user.shoppingitems.all()

        shoppingitemsearchresults = ShoppingItem.objects.filter(
            name__icontains=text_search
        ).exclude(name__in=usershoppingitems.values_list("name", flat=True))

    return render(
        request,
        "partials/shopping-list-search-result.html",
        {"shoppingitemsearchresults": shoppingitemsearchresults},
    )
