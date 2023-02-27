from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Lower


class ShoppingItem(models.Model):
    name = models.CharField(max_length=128, unique=True)
    users = models.ManyToManyField(
        User, related_name="shoppingitems", through="UserShoppingItems"
    )
    photo = models.ImageField(upload_to="shoppingitem_photos", null=True, blank=True)

    class Meta:
        ordering = [Lower("name")]


class UserShoppingItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shoppingitem = models.ForeignKey(ShoppingItem, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()
    checked = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]
