from django.urls import path
from shoppingitems import views
from users import views as user_views

urlpatterns = [
    path("", views.IndexView.as_view(), name="vsd-home"),
    path("shoppinglist/", views.ShoppingListView.as_view(), name="vsd-shoppinglist"),
    path("about/", views.AboutView.as_view(), name="vsd-about"),
    path("register/", user_views.register, name="vsd-register"),
]

htmx_urlpatterns = [
    path(
        "add-shoppingitem-and-usershoppingitem",
        views.add_shoppingitem_and_usershoppingitem,
        name="add-shoppingitem-and-usershoppingitem",
    ),
    path(
        "add-usershoppingitem/<int:pk>/",
        views.add_usershoppingitem,
        name="add-usershoppingitem",
    ),
    path(
        "del-usershoppingitem/<int:pk>/",
        views.del_usershoppingitem,
        name="del-usershoppingitem",
    ),
    path(
        "put-usershoppingitem/<int:pk>/",
        views.put_usershoppingitem,
        name="put-usershoppingitem",
    ),
    path(
        "sort-usershoppingitem/",
        views.sort_usershoppingitem,
        name="sort-usershoppingitem",
    ),
    path(
        "del-shoppingitem/<int:pk>/",
        views.del_shoppingitem,
        name="del-shoppingitem",
    ),
    path("get-shoppingitem", views.get_shoppingitem, name="get-shoppingitem"),
]

urlpatterns += htmx_urlpatterns
