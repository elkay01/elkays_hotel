from django.contrib import admin
from . models import Category,Room,Booking, Payment, Client


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'image')

class RoomAdmin(admin.ModelAdmin):
    list_display = ('id','name','number','category','beds','eco','fam','biz','capacity','price','description','available','min_order','max_order')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user','rooms','price', 'days','paid_order','order_no', 'check_in', 'check_out')

class PaymentAdmin(admin.ModelAdmin):
    list_display=('id','user','amount','order_no','pay_code','paid_order','first_name','last_name','phone','address','city','state')


class ClientAdmin(admin.ModelAdmin):
    list_display=('id','user','first_name','last_name','phone','address','city','state')




admin.site.register(Category,CategoryAdmin)
admin.site.register(Room,RoomAdmin)
admin.site.register(Booking,BookingAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Client,ClientAdmin)
