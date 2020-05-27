from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)

    TYPE_CHOICES = [
        (0, 'Seller'),
        (1, 'Buyer')
    ]

    type = models.IntegerField(choices=TYPE_CHOICES, default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    company_seller = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='seller')
    company_buyer = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='buyer')

    def __str__(self):
        return str(self.id)


class OrderPosition(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=8, decimal_places=3)
    elem_price = models.DecimalField(max_digits=8, decimal_places=2)
    sum_price = models.DecimalField(max_digits=8, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name + ' ' + str(self.quantity)