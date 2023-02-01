from django.db import models

# Create your models here.
from xmlrpc.client import Boolean
from django.db import models
from customer.models import Customer
from store.models import Product

# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete= models.PROTECT)
    total = models.DecimalField(max_digits = 10, decimal_places= 2)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-created'] # sort theo cái ngày đặt hàng. Ngày mới đặt luôn được nằm ở trên

    def __str__(self):
        return f'Order {self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete= models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.pk)
