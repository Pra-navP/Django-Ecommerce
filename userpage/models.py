from django.db import models
from django.core.validators import MinLengthValidator
from product.models import *

# Create your models here.

class Setting(models.Model):
    name = models.CharField(max_length=130)
    favicon = models.ImageField(upload_to='static/uploads/')
    logo = models.ImageField(upload_to='static/uploads/')
    email = models.EmailField()
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=14, validators=[MinLengthValidator(9)])
    fb_link = models.URLField(blank=True)
    insta_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    

    def __str__(self):
        return self.name


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user.username} - {self.product.title}"
    
class Order(models.Model):
    # STATUS = (('On the way', 'On the way')
    #           ('Completed', 'Completed')
    #           ('Failed', 'Failed'))
    
    PAYMENT = (('Cash', 'Cash'),
               ('Esewa','Esewa'),
               ('Stripe', 'Stripe'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=14, validators=[MinLengthValidator(10)])
    status = models.CharField(max_length=100, default = 'In process', null = True)
    payment_method = models.CharField(max_length=50, choices = PAYMENT)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    # 17:34
    

