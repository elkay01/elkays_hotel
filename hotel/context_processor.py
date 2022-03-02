from .models import  Category, Booking


def booking_viewread(request):
    booking_view=Booking.objects.filter(user__username=request.user.username, paid_order=False)


    booking_viewreader=0
    for item in booking_view:
        booking_viewreader += item.days

    context={
        'booking_viewreader':booking_viewreader
    }
    return context
    

def dropdown(request):
    categories = Category.objects.all()

    context = {
        'categories':categories
    }

    return context
    

