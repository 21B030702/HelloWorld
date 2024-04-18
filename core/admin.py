from django.contrib import admin
from .models import Supplier, Category, Item, Auction, Review, User, Purchase

admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Auction)
admin.site.register(Review)
admin.site.register(User)
admin.site.register(Purchase)

