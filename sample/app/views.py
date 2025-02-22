from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.



def shop_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    # if 'user' in req.session:
    #     return redirect(user_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['password']
        data=authenticate(username=uname,password=password)
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['shop']=uname    #--------------->creating session
                return redirect(shop_home)
            else:
                login(req,data)
                req.session['user']=uname
                return redirect(user_home)
        else:
            messages.warning(req,"Invalid username or password")
            return redirect(shop_login)
    else:
        return render(req,'login.html')



def shop_logout(req):
    logout(req)
    req.session.flush()
    return redirect(shop_login)
    
def shop_home(req):
    if 'shop' in req.session:
        car=Car_category.objects.all()
        return render(req,'shop/home.html',{'cars':car})
    else:
        return redirect(shop_login)


def add_car(request):
    if request.method == 'POST':
        car_id = request.POST['car_id']
        car_name = request.POST['car_name']
        car_year = request.POST['car_year']
        car_place = request.POST['car_place']
        car_rent = request.POST['car_rent']
        car_fuel = request.POST['car_fuel']
        car_img = request.FILES['car_img']
        car_category = request.POST['category'] 
        try:
            category_instance = Car_category.objects.get(id=car_category)
            new_car = Cars.objects.create(
                car_id=car_id,
                car_name=car_name,
                car_year=car_year,
                car_place=car_place,
                car_rent=car_rent,
                car_fuel=car_fuel,
                car_img=car_img,
                category=category_instance
            )
            new_car.save()
            return redirect(shop_home)
        except Car_category.DoesNotExist:
            return HttpResponse('Category not found.', status=400)
    else:
        categories = Car_category.objects.all()  
        return render(request, 'shop/addcar.html', {'categories': categories})



def edit_car(request, car_id):
    car = get_object_or_404(Cars, id=car_id)
    if request.method == 'POST':
        car.car_id = request.POST.get('car_id')
        car.car_name = request.POST.get('car_name')
        car.car_year = request.POST.get('car_year')
        car.car_place = request.POST.get('car_place')
        car.car_rent = request.POST.get('car_rent')
        car.car_fuel = request.POST.get('car_fuel')
        if 'car_img' in request.FILES:
            car.car_img = request.FILES['car_img']
        car.save()
        return redirect(shop_home)  
    return render(request, 'shop/edit_car.html', {'car': car})



def delete_car(request, id):
    car = get_object_or_404(Cars, pk=id)
    image_path = car.car_img.path 
    if os.path.exists(image_path):
        os.remove(image_path) 
    car.delete()
    return redirect(shop_home)

def budget_cars(req,id):
    category = Car_category.objects.get(id=id)
    car_details = Cars.objects.filter(category=category)
    return render(req, 'shop/car_list.html', {'category': category,'car_details':car_details})

# def medium_cars(req,id):
#     category = Car_category.objects.get(id=id)
#     car_details = Cars.objects.filter(category=category)
#     return render(req, 'shop/car_list.html', {'category': category,'car_details':car_details})

# ------------------user-------------------------



def register(req):
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        password=req.POST['password']
        try:
            data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
            data.save()
            return redirect(shop_login)
        except:
            messages.warning(req,"Email Exists")
            return redirect(register)
    else:
        return render(req,'user/register.html')
    


def user_home(req):
    car=Car_category.objects.all()
    return render(req,'user/customer_home.html',{'cars':car})


def cars_list(req,id):
    category = Car_category.objects.get(id=id)
    car_details = Cars.objects.filter(category=category)
    return render(req, 'user/cars_list.html', {'category': category,'car_details':car_details})

def about(req):
    return render(req,'shop/about.html')

# def book_car(request, car_id):
#     car = get_object_or_404(Cars, id=car_id)

#     if request.method == "POST":
#         customer_name = request.POST["customer_name"]
#         customer_email = request.POST["customer_email"]
#         customer_phone = request.POST["customer_phone"]
#         start_date = request.POST["start_date"]
#         end_date = request.POST["end_date"]

#         try:
#             # Convert dates from string to actual date format
#             start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
#             end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

#             # Save booking
#             new_booking = Booking.objects.create(
#                 car=car,
#                 customer_name=customer_name,
#                 customer_email=customer_email,
#                 customer_phone=customer_phone,
#                 start_date=start_date,
#                 end_date=end_date,
#             )
#             new_booking.save()
#             return HttpResponse("Car booked successfully!")

#         except Exception as e:
#             return HttpResponse(f"Error: {e}", status=400)

#     return render(request, "user/book_car.html",{"cars":car})



def book_car(request, car_id):
    # Check if user is logged in
    if 'user' in request.session:
        return redirect(register)

    car = get_object_or_404(Cars, id=car_id)

    if request.method == "POST":
        customer_name = request.POST["customer_name"]
        customer_email = request.POST["customer_email"]
        customer_phone = request.POST["customer_phone"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]

        try:
            # Convert dates to date format
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            # Save booking
            new_booking = Booking.objects.create(
                car=car,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                start_date=start_date,
                end_date=end_date,
            )
            new_booking.save()
            messages.success(request, "Car booked successfully!")
            return redirect("user_home")  # Redirect to user home page after booking

        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect("book_car", car_id=car_id)

    return render(request,"user/book_car.html",{"cars":car})





