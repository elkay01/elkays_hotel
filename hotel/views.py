import uuid
import json
import requests

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from hotel.booking_functions.availability import check_availability
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from . forms import AvailabilityForm
from . models import Category,Room,Booking,Payment,Client
from django.contrib import messages
from . forms import SignupForm

# Create your views here.
def index(request):
    available = Room.objects.filter(available=True)
    eco = Room.objects.filter(eco=True).first()
    fam = Room.objects.filter(fam=True).first()
    biz = Room.objects.filter(biz=True).first()
    context = {
        'available':available,
        'eco':eco,
        'fam':fam,
        'biz':biz,
    }
    return render(request, 'index.html', context)



def categories(request):
    categories = Category.objects.all()
    context = {
        'categories':categories
    }
    return render(request, 'categories.html',context)


def category(request,id):
    category=Room.objects.filter(category_id=id,available=True)
    single_cat = Category.objects.get(pk=id)
    context={
        'category':category,
        'single_cat':single_cat,
    }
    return render(request, 'category.html', context)


def rooms(request):
    room = Room.objects.all().filter(available=True)
    return render(request, 'rooms.html', {'room':room})

    

def details(request, id):
    details=Room.objects.get(pk=id)
    context={
        'details':details
    }
    return render(request, 'details.html',context)


def logoutfunc(request): 
    logout(request)
    return redirect('loginform')


def loginform(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            messages.success(request, 'now logged in as a user!')
            return redirect('index')
        else:
            messages.info(request, 'Username/password incorrect')
            return redirect('loginform')

    return render(request, 'loginform.html')

@login_required(login_url='/loginform')
def password(request):
    update = PasswordChangeForm(request.user)
    if request.method=='POST':
        update=PasswordChangeForm(request.user, request.POST)
        if update.is_valid():
            user=update.save()
            update_session_auth_hash(request,user)
            messages.success(request, 'Password Update Successful')
            return redirect('index')
        else:
            messages.error(request, update.errors)
            return redirect('password')

    context={
        'update':update
    }
    return render(request, 'password.html', context)

def signupform(request):
    reg = SignupForm()
    if request.method == 'POST':
        reg = SignupForm(request.POST)
        if reg.is_valid():
            new = reg.save() 
            newreg = Client(user=new)
            newreg.first_name = new.first_name
            newreg.last_name = new.last_name
            newreg.save()
            messages.success(request, 'Sign-in successfull!')
            login(request, new)
            return redirect('index')
        else:
            messages.warning(request, reg.errors)
            return redirect( 'signupform')
            
    context ={
        'reg': reg
    }
    return render(request, 'signup.html', context)

def form_valid(self, form):
    data = form.cleaned_data
    room = Room.objects.filter(category=data['room_category'])
    available_rooms=[]
    for room in room:
        if check_availability(room, data['check_in'], data['check_out']):
            available_rooms.append(room)

    if len(available_rooms)>0:
        room = available_rooms[0]
        booking = Booking.objects.create(
            user=self.request.user,
            room=room,
            check_in=data['check_in'],
            check_out=data['check_out']
        )
        booking.save()
        return HttpResponse(booking)
    else:
        return HttpResponse('This category of rooms are booked!! Try another one')


@login_required(login_url='loginform')
def booking(request):
    if request.method == 'POST':
        order_no = str(uuid.uuid4())
        checkin = request.POST['checkin']
        checkout = request.POST['checkout']
        # vol = int(request.POST['quantity'])
        pid = request.POST['itemid']
        item = Room.objects.get(pk=pid)
        booking_view = Booking.objects.filter(user__username= request.user.username, paid_order=False)
        if booking_view:
            order = Booking.objects.filter(user__username=request.user.username, rooms_id=item.id).first()
            if order:
                order.check_in=checkin
                order.check_out=checkout
                if order.check_in > checkout or order.check_out < checkin:
                    order.save()
                    messages.success(request, "The room you requested is available!")
                    return redirect('booking_view') 
                else:
                    messages.info(request, "This room is not available for the dates you requested!")
                    return redirect('rooms')

            else:
                cart_num = booking_view[0].order_no
                newitem = Booking()
                newitem.user=request.user
                newitem.rooms=item
                newitem.price=item.price
                newitem.order_no= cart_num
                # newitem.quantity=vol
                newitem.paid_order=False
                newitem.check_in= checkin
                newitem.check_out= checkout
                newitem.save()
                return redirect('booking_view')

        else:
            neworder = Booking()
            neworder.user=request.user
            neworder.rooms=item
            neworder.price=item.price
            neworder.order_no=order_no
            # neworder.quantity=vol
            neworder.paid_order=False
            neworder.check_in= checkin
            neworder.check_out= checkout
            neworder.save()
            messages.success(request, 'Room added!')     
    
    return redirect('booking_view')
    

@login_required(login_url='/loginform')
def booking_view(request):
    booking_view=Booking.objects.filter(user__username=request.user.username, paid_order=False)

    for item in booking_view:
        item.days = (item.check_out - item.check_in).days
        item.save()

    subtotal=0
    vol=0
    total=0

    for item in booking_view:
        subtotal += item.rooms.price * item.days

    vat=0.075 * subtotal

    total= subtotal + vat
    context={
        'booking_view':booking_view,
        'subtotal':subtotal,
        'vat':vat,
        'total':total,
    }
    return render(request, 'booking_view.html', context)


@login_required(login_url='/loginform')
def deleteitem(request):
    itemid=request.POST['itemid']
    Booking.objects.filter(pk=itemid).delete()
    messages.success(request, 'Room deleted')
    return redirect('booking_view')


@login_required(login_url='/loginform')
def increase(request):
    itemval=request.POST['itemval']
    valid=request.POST['valid']
    update=Booking.objects.get(pk=valid)
    update.quantity=itemval
    update.save
    messages.success(request, 'Room quantity update successfully')
    return redirect('booking_view') 


@login_required(login_url='/loginform')
def checkout(request):
    booking_view=Booking.objects.filter(user__username=request.user.username, paid_order=False)
    done = Client.objects.get(user__username=request.user.username)

    subtotal=0
    vol=0
    total=0

    for item in booking_view:
        subtotal+=item.rooms.price * item.days

    vat=0.075 *subtotal

    total=subtotal + vat


    context={
        'booking_view':booking_view,
        'total':total,
        'booking_view_code':booking_view[0].order_no,
        'done':done
    }
    return render(request, 'checkout.html',context)




@login_required(login_url='/loginform')
def placeorder(request):
    if request.method=='POST':
        api_key='sk_test_11483da27a28a2304414f2ca3be5a7c88bd121a7'
        curl= 'https://api.paystack.co/transaction/initialize'
        cburl= 'http://18.221.154.166/completed/'
        total= float(request.POST['total']) *100
        booking_view_code = request.POST['booking_view_code']
        pay_code= str(uuid.uuid4())
        user= User.objects.get(username=request.user.username)
        phone= request.POST['phone']
        address= request.POST['address']
        city= request.POST['city']
        state= request.POST['state']

       #collect data that you will send to paystack
        headers={'Authorization':f'Bearer {api_key}'}
        data={'reference':pay_code,'email':user.email,'amount':int(total),'callback_url':cburl,'order_number':booking_view_code}

        #make a call to paystack
        try:
            r=requests.post(curl, headers=headers, json=data)
        except Exception:
            messages.error(request, 'Network busy, try again')
        else:
            transback= json.loads(r.text)
            rd_url= transback['data']['authorization_url']

            paid = Payment()
            paid.user=user 
            paid.amount=total 
            paid.order_no=booking_view_code 
            paid.pay_code=pay_code 
            paid.paid_order=True
            paid.first_name= user.first_name 
            paid.last_name= user.last_name 
            paid.phone= phone 
            paid.address= address 
            paid.city= city 
            paid.state= state
            paid.save()
            
            return redirect(rd_url)
    return redirect('checkout')



def completed(request):
    don = Client.objects.get(user__username=request.user.username)
    bag = Booking.objects.filter(user__username=request.user.username, paid_order=True)
        
    for item in bag:
        item.paid_order = True
        item.save()

        stock=Room.objects.get(pk=item.rooms.id)
        stock.available = False
        stock.save()
        
    context={
        'don':don,
        'bag':bag, 
        
    }
    return render(request, 'completed.html', context)


