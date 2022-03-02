from django.db import models
from django.conf import settings
from django.db.models.fields import DateTimeField
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='rooms', default='pix.jpg')

    def __str__(self):
        return self.title


    class Meta:
            db_table = 'category'
            managed = True
            verbose_name = 'Category'
            verbose_name_plural = 'Categories'


class Room(models.Model):
    ROOM_CATEGORIES=(
        ('ECO', 'ECONOMY'),
        ('FAM', 'FAMILY'),
        ('BUS', 'BUSINESS'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    number = models.IntegerField()
    image = models.ImageField(upload_to='products', default='pix.jpg')
    beds = models.IntegerField()
    capacity = models.IntegerField()
    price = models.IntegerField()
    description = models.TextField()
    available = models.BooleanField(default=True)
    eco = models.BooleanField(default=False)
    fam = models.BooleanField(default=False)
    biz = models.BooleanField(default=False)
    min_order = models.IntegerField(default=1)
    max_order = models.IntegerField(default=3)

    def __str__(self):
        return f'{self.number}.  {self.category} with {self.beds} for {self.capacity} people'


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    rooms = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField()
    check_in = models.DateField()
    check_out = models.DateField()
    days=models.IntegerField(blank=True, null=True)
    paid_order = models.BooleanField(default=False)
    order_no = models.CharField(max_length=36)

    def __str__(self):
        return self.user.username
        

class Payment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.IntegerField()
    order_no=models.CharField(max_length=36)
    pay_code=models.CharField(max_length=36)
    paid_order=models.BooleanField(default=False)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)

def __str__(self):
    return self.user.username



class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=50, blank=True, null=True)
    address=models.CharField(max_length=100, blank=True, null=True)
    city=models.CharField(max_length=50, blank=True, null=True)
    state=models.CharField(max_length=50, blank=True, null=True)

def __str__(self):
    return self.user.username