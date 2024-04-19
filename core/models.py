from django.db import models
from django.db.models import JSONField
from django.contrib.auth.models import AbstractUser
# Create your models here.

STATUS_CHOICES = [
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('canceled', 'Canceled'),
]

class User(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=30, blank=True)
    annual_income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    multiple_addresses = models.JSONField(blank=True, null=True)  # Предполагается использование PostgreSQL
    multiple_phones = models.JSONField(blank=True, null=True)
    multiple_credit_cards = models.JSONField(blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    company_category = models.CharField(max_length=255)
    revenue = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.company_name

class Item(models.Model):
    supplier = models.ForeignKey(Supplier, related_name='items', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reserve_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=50)  # Например, 'In Stock', 'Sold', 'Auction'
    location = models.TextField(blank=True, null=True)
    photos = models.JSONField(blank=True, null=True)  # Предполагается использование PostgreSQL

    def __str__(self):
        return self.name

class Auction(models.Model):
    item = models.ForeignKey(Item, related_name='auctions', on_delete=models.CASCADE)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    def __str__(self):
        return self.item.name


class Review(models.Model):
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='reviews', on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Рейтинг от 1 до 5

class Purchase(models.Model):
    user = models.ForeignKey(User, related_name='purchases', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='purchased', on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Purchase {self.pk} by {self.user.username}"

class DeliveryStatus(models.Model):
    purchase = models.ForeignKey(
        'Purchase', 
        related_name='delivery_statuses', 
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"DeliveryStatus for {self.purchase} is {self.status}"
    
class Delivery(models.Model):
    purchase = models.ForeignKey(
        Purchase, 
        related_name='deliveries',
        on_delete=models.CASCADE
        )
    delivery_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    expected_delivery_date = models.DateField()
    actual_delivery_date = models.DateField(null=True, blank=True)
    carrier = models.CharField(max_length=255)

class Bid(models.Model):
    item = models.ForeignKey(Item, related_name='bids', on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, related_name='bids', on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.username} bids {self.bid_amount} on {self.item.name}"