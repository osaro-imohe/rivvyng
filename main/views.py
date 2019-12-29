from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import logout as auth_logout
from moderator.models import Store_detail
from moderator.models import Store_image
from main.models import Cart_item
from moderator.models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import math
from django.http import JsonResponse
import handler404, handler500




def home(request):
    if request.method == "POST" and request.POST.get("lat") is not '' and request.POST.get("lng") is not '':
        lat = request.POST.get("lat")
        lng = request.POST.get("lng")
        location = request.POST.get("location")
        request.session['lat'] = lat
        request.session['lng'] = lng
        request.session['location'] = location
        return redirect("main:feed")
    if request.user.is_authenticated:
        usercartitems = request.user.cart_item_set.all()
        numberofitemsincart = len(usercartitems)
    elif not request.user.is_authenticated and request.session.get('cart'):
        cartitems = request.session['cart']
        numberofitemsincart = len(cartitems)
    else:
        numberofitemsincart = 0
    return render(request, 'main/home.html', {'numberofitemsincart':numberofitemsincart,})

def signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            if User.objects.filter(email = request.POST.get("email")).exists() == False:
                user = User.objects.create_user(first_name=first_name,last_name=last_name,email = email, password = password, username = email,)
                newuser = authenticate(username=email,password=password,)
                auth_login(request, newuser)
                return redirect('main:home')
            elif User.objects.filter(username = request.POST.get("email")).exists():
                error_message2 = "A user with this email adress already exists"
                return render(request, "main/signup.html",  {"error_message2": error_message2,})
        return render(request, 'main/signup.html')
    else:
        return redirect("main:account")


def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(username=username,password=password,)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('main:home')
            else:
                error_message3 = "Your login details are incorrect"
                return render(request,"main/login.html",{"error_message3":error_message3})
        else:
            return render(request, 'main/login.html')
    else:
        return redirect('main:account')

def feed(request):
    # template = loader.get_template("main/feed.html")
    latitude = request.session['lat']
    longitude = request.session['lng']
    location = request.session['location']
    lat = float(latitude) # Central point latitude
    lng = float(longitude) # Central point longitude
    if request.method == "POST":
        searchquery = request.POST.get("searchquery")
        request.session['storesearchsession'] = searchquery
        storesearchsession = request.session['storesearchsession']
        print(storesearchsession)
        return redirect("main:storesearch")

    if request.user.is_authenticated:
        usercartitems = request.user.cart_item_set.all()
        numberofitemsincart = len(usercartitems)
    elif not request.user.is_authenticated and request.session.get('cart'):
        cartitems = request.session['cart']
        numberofitemsincart = len(cartitems)
    else:
        numberofitemsincart = 0
    radius = 10
    point = Point(lng, lat)
    queryset5 = Store_detail.objects.filter(store_location_point__distance_lt=(point, Distance(km=radius)))
    queryset2 = []
    for query in queryset5:
        distance = point.distance(query.store_location_point) * 100
        if distance >= 0 and distance <= 1:
            distance = 1.00
            deliverytime = "15 - 20 minutes"
            unitprice = 200
            price = distance * unitprice
            deliveryprice = round(price)
        elif distance > 1:
            unitprice = 200
            deliverytime = "35 - 40 minutes"
            price = distance * unitprice
            deliveryprice = math.ceil(price/100)*100
        else :
            unitprice = 200
            deliverytime = "35 - 40 minutes"
            price = distance * unitprice
            deliveryprice = math.ceil(price/100)*100
        update = {"query":query, "deliveryprice":deliveryprice,"deliverytime":deliverytime,}
        queryset2.append(update)
    page = request.GET.get('page',1)
    queryset3 = Paginator(queryset2, 5)
    try:
        queryset = queryset3.page(page)
    except PageNotAnInteger:
        queryset = queryset3.page(1)
    except EmptyPage:
        queryset = Store_detail.objects.none()
    # return HttpResponse(template.render(context,request))
    return render(request, 'main/feed.html', {'queryset': queryset, 'location':location,'numberofitemsincart':numberofitemsincart,})
def account(request):
    if request.user.is_authenticated:
        email = request.user.email
        first_name = request.user.first_name
        last_name = request.user.last_name
        first_initial = first_name[0].upper()
        last_initial = last_name[0].upper()
        error_message = ""
        success_message = ""
        if request.method == "POST":
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            password = request.POST.get("password")
            password_verification = request.POST.get("password_verification")
            error_message = ""
            success_message = ""
            if password is not '' and password_verification is not '' and password == password_verification:
                user = request.user
                user.set_password(password)
                user.save()
                error_message = ""
                success_message = "Your password has been changed successfully"
            elif password != password_verification:
                error_message = "Your passwords don't match"
                success_message = ""
            else:
                error_message = ""
                success_message = ""
        return render(request,'main/account.html',{"email":email,"first_name":first_name,"last_name":last_name,"first_initial":first_initial, "last_initial":last_initial,"error_message":error_message,"success_message":success_message,})
    else:
        return redirect("main:login")

def storeinfo(request,slug,pk):
    template = loader.get_template("main/storeinfo.html")
    if Store_detail.objects.exists():
        query = Store_detail.objects.get(pk=pk)
        products = query.product_set.all()
        if request.user.is_authenticated:
            usercartitems = request.user.cart_item_set.all()
            numberofitemsincart = len(usercartitems)
        elif not request.user.is_authenticated and request.session.get('cart'):
            cartitems = request.session['cart']
            numberofitemsincart = len(cartitems)
        else:
            numberofitemsincart = 0
        context = {
            "products":products,
            "query":query,
            "numberofitemsincart":numberofitemsincart,
            }
        return HttpResponse(template.render(context,request))
    else:
        if request.user.is_authenticated:
            usercartitems = request.user.cart_item_set.all()
            numberofitemsincart = len(usercartitems)
        elif not request.user.is_authenticated and request.session.get('cart'):
            cartitems = request.session['cart']
            numberofitemsincart = len(cartitems)
        else:
            numberofitemsincart = 0
        context = {
            "numberofitemsincart":numberofitemsincart,
        }
        return HttpResponse(template.render(context,request))
    return render(request,'main/storeinfo.html')

def restaurantcategory(request):
    category = "Restaurants"
    latitude = request.session['lat']
    longitude = request.session['lng']
    location = request.session['location']
    lat = float(latitude) # Central point latitude
    lng = float(longitude) # Central point longitude
    if request.user.is_authenticated:
        usercartitems = request.user.cart_item_set.all()
        numberofitemsincart = len(usercartitems)
    elif not request.user.is_authenticated and request.session.get('cart'):
        cartitems = request.session['cart']
        numberofitemsincart = len(cartitems)
    else:
        numberofitemsincart = 0
    radius = 10
    point = Point(lng, lat)
    queryset2 = Store_detail.objects.filter(store_location_point__distance_lt=(point, Distance(km=radius)))
    queryset4= queryset2.filter(store_category="restaurants")
    for query in queryset4:
        print(point.distance(query.store_location_point)*100)
    page = request.GET.get('page',1)
    queryset3 = Paginator(queryset4, 20)
    try:
        queryset = queryset3.page(page)
    except PageNotAnInteger:
        queryset = queryset3.page(1)
    except EmptyPage:
        queryset = Store_detail.objects.none()
    return render(request, 'main/filterbycategory.html',{"category":category,"queryset":queryset,'numberofitemsincart':numberofitemsincart,})

def groceries(request):
    category = "Groceries"
    latitude = request.session['lat']
    longitude = request.session['lng']
    location = request.session['location']
    lat = float(latitude) # Central point latitude
    lng = float(longitude) # Central point longitude
    if request.user.is_authenticated:
        usercartitems = request.user.cart_item_set.all()
        numberofitemsincart = len(usercartitems)
    elif not request.user.is_authenticated and request.session.get('cart'):
        cartitems = request.session['cart']
        numberofitemsincart = len(cartitems)
    else:
        numberofitemsincart = 0
    radius = 10
    point = Point(lng, lat)
    queryset2 = Store_detail.objects.filter(store_location_point__distance_lt=(point, Distance(km=radius)))
    queryset4= queryset2.filter(store_category="grocery")
    for query in queryset4:
        print(point.distance(query.store_location_point)*100)
    page = request.GET.get('page',1)
    queryset3 = Paginator(queryset4, 20)
    try:
        queryset = queryset3.page(page)
    except PageNotAnInteger:
        queryset = queryset3.page(1)
    except EmptyPage:
        queryset = Store_detail.objects.none()
    return render(request, 'main/filterbycategory.html',{"category":category,"queryset":queryset,'numberofitemsincart':numberofitemsincart,})

def mobilephonesandtablets(request):
    category = "Mobile phones"
    latitude = request.session['lat']
    longitude = request.session['lng']
    location = request.session['location']
    lat = float(latitude) # Central point latitude
    lng = float(longitude) # Central point longitude
    if request.user.is_authenticated:
        usercartitems = request.user.cart_item_set.all()
        numberofitemsincart = len(usercartitems)
    elif not request.user.is_authenticated and request.session.get('cart'):
        cartitems = request.session['cart']
        numberofitemsincart = len(cartitems)
    else:
        numberofitemsincart = 0
    radius = 10
    point = Point(lng, lat)
    queryset2 = Store_detail.objects.filter(store_location_point__distance_lt=(point, Distance(km=radius)))
    queryset4= queryset2.filter(store_category="phonesandtablets")
    for query in queryset4:
        print(point.distance(query.store_location_point)*100)
    page = request.GET.get('page',1)
    queryset3 = Paginator(queryset4, 20)
    try:
        queryset = queryset3.page(page)
    except PageNotAnInteger:
        queryset = queryset3.page(1)
    except EmptyPage:
        queryset = Store_detail.objects.none()
    return render(request, 'main/filterbycategory.html',{"category":category,"queryset":queryset,'numberofitemsincart':numberofitemsincart,})

def computers(request):
    category = "Computers"
    latitude = request.session['lat']
    longitude = request.session['lng']
    location = request.session['location']
    lat = float(latitude) # Central point latitude
    lng = float(longitude) # Central point longitude
    if request.user.is_authenticated:
        usercartitems = request.user.cart_item_set.all()
        numberofitemsincart = len(usercartitems)
    elif not request.user.is_authenticated and request.session.get('cart'):
        cartitems = request.session['cart']
        numberofitemsincart = len(cartitems)
    else:
        numberofitemsincart = 0
    radius = 10
    point = Point(lng, lat)
    queryset2 = Store_detail.objects.filter(store_location_point__distance_lt=(point, Distance(km=radius)))
    queryset4= queryset2.filter(store_category="computers")
    for query in queryset4:
        print(point.distance(query.store_location_point)*100)
    page = request.GET.get('page',1)
    queryset3 = Paginator(queryset4, 20)
    try:
        queryset = queryset3.page(page)
    except PageNotAnInteger:
        queryset = queryset3.page(1)
    except EmptyPage:
        queryset = Store_detail.objects.none()
    return render(request, 'main/filterbycategory.html',{"category":category,"queryset":queryset,'numberofitemsincart':numberofitemsincart,})

def electronics(request):
    category = "Electronics"
    latitude = request.session['lat']
    longitude = request.session['lng']
    location = request.session['location']
    lat = float(latitude) # Central point latitude
    lng = float(longitude) # Central point longitude
    if request.user.is_authenticated:
        usercartitems = request.user.cart_item_set.all()
        numberofitemsincart = len(usercartitems)
    elif not request.user.is_authenticated and request.session.get('cart'):
        cartitems = request.session['cart']
        numberofitemsincart = len(cartitems)
    else:
        numberofitemsincart = 0
    radius = 10
    point = Point(lng, lat)
    queryset2 = Store_detail.objects.filter(store_location_point__distance_lt=(point, Distance(km=radius)))
    queryset4= queryset2.filter(store_category="electronics")
    for query in queryset4:
        print(point.distance(query.store_location_point)*100)
    page = request.GET.get('page',1)
    queryset3 = Paginator(queryset4, 20)
    try:
        queryset = queryset3.page(page)
    except PageNotAnInteger:
        queryset = queryset3.page(1)
    except EmptyPage:
        queryset = Store_detail.objects.none()
    return render(request, 'main/filterbycategory.html',{"category":category,"queryset":queryset,'numberofitemsincart':numberofitemsincart,})

def fashion(request):
    category = "Fashion"
    latitude = request.session['lat']
    longitude = request.session['lng']
    location = request.session['location']
    lat = float(latitude) # Central point latitude
    lng = float(longitude) # Central point longitude
    if request.user.is_authenticated:
        usercartitems = request.user.cart_item_set.all()
        numberofitemsincart = len(usercartitems)
    elif not request.user.is_authenticated and request.session.get('cart'):
        cartitems = request.session['cart']
        numberofitemsincart = len(cartitems)
    else:
        numberofitemsincart = 0
    radius = 10
    point = Point(lng, lat)
    queryset2 = Store_detail.objects.filter(store_location_point__distance_lt=(point, Distance(km=radius)))
    queryset4= queryset2.filter(store_category="fashion")
    for query in queryset4:
        print(point.distance(query.store_location_point)*100)
    page = request.GET.get('page',1)
    queryset3 = Paginator(queryset4, 20)
    try:
        queryset = queryset3.page(page)
    except PageNotAnInteger:
        queryset = queryset3.page(1)
    except EmptyPage:
        queryset = Store_detail.objects.none()
    return render(request, 'main/filterbycategory.html',{"category":category,"queryset":queryset,'numberofitemsincart':numberofitemsincart,})

def healthandbeauty(request):
    category = "Health & Beauty"
    latitude = request.session['lat']
    longitude = request.session['lng']
    location = request.session['location']
    lat = float(latitude) # Central point latitude
    lng = float(longitude) # Central point longitude
    if request.user.is_authenticated:
        usercartitems = request.user.cart_item_set.all()
        numberofitemsincart = len(usercartitems)
    elif not request.user.is_authenticated and request.session.get('cart'):
        cartitems = request.session['cart']
        numberofitemsincart = len(cartitems)
    else:
        numberofitemsincart = 0
    radius = 10
    point = Point(lng, lat)
    queryset2 = Store_detail.objects.filter(store_location_point__distance_lt=(point, Distance(km=radius)))
    queryset4= queryset2.filter(store_category="healthandbeauty")
    for query in queryset4:
        print(point.distance(query.store_location_point)*100)
    page = request.GET.get('page',1)
    queryset3 = Paginator(queryset4, 20)
    try:
        queryset = queryset3.page(page)
    except PageNotAnInteger:
        queryset = queryset3.page(1)
    except EmptyPage:
        queryset = Store_detail.objects.none()
    return render(request, 'main/filterbycategory.html',{"category":category,"queryset":queryset,'numberofitemsincart':numberofitemsincart,})

def games(request):
    category = "Games"
    latitude = request.session['lat']
    longitude = request.session['lng']
    location = request.session['location']
    lat = float(latitude) # Central point latitude
    lng = float(longitude) # Central point longitude
    if request.user.is_authenticated:
        usercartitems = request.user.cart_item_set.all()
        numberofitemsincart = len(usercartitems)
    elif not request.user.is_authenticated and request.session.get('cart'):
        cartitems = request.session['cart']
        numberofitemsincart = len(cartitems)
    else:
        numberofitemsincart = 0
    radius = 10
    point = Point(lng, lat)
    queryset2 = Store_detail.objects.filter(store_location_point__distance_lt=(point, Distance(km=radius)))
    queryset4= queryset2.filter(store_category="gaming")
    for query in queryset4:
        print(point.distance(query.store_location_point)*100)
    page = request.GET.get('page',1)
    queryset3 = Paginator(queryset4, 20)
    try:
        queryset = queryset3.page(page)
    except PageNotAnInteger:
        queryset = queryset3.page(1)
    except EmptyPage:
        queryset = Store_detail.objects.none()
    return render(request, 'main/filterbycategory.html',{"category":category,"queryset":queryset,'numberofitemsincart':numberofitemsincart,})

def homeanddecor(request):
    category = "Home & Decor"
    latitude = request.session['lat']
    longitude = request.session['lng']
    location = request.session['location']
    lat = float(latitude) # Central point latitude
    lng = float(longitude) # Central point longitude
    if request.user.is_authenticated:
        usercartitems = request.user.cart_item_set.all()
        numberofitemsincart = len(usercartitems)
    elif not request.user.is_authenticated and request.session.get('cart'):
        cartitems = request.session['cart']
        numberofitemsincart = len(cartitems)
    else:
        numberofitemsincart = 0
    radius = 10
    point = Point(lng, lat)
    queryset2 = Store_detail.objects.filter(store_location_point__distance_lt=(point, Distance(km=radius)))
    queryset4= queryset2.filter(store_category="homeanddecor")
    for query in queryset4:
        print(point.distance(query.store_location_point)*100)
    page = request.GET.get('page',1)
    queryset3 = Paginator(queryset4, 20)
    try:
        queryset = queryset3.page(page)
    except PageNotAnInteger:
        queryset = queryset3.page(1)
    except EmptyPage:
        queryset = Store_detail.objects.none()
    return render(request, 'main/filterbycategory.html',{"category":category,"queryset":queryset,'numberofitemsincart':numberofitemsincart,})

def addtocart(request):
    if request.method =="POST" and request.user.is_authenticated:
        store_id = request.POST.get("store_id")
        product_id = request.POST.get("product_id")
        print(product_id)
        quantity = request.POST.get("quantity")
        if request.user.cart_item_set.filter(product_id = product_id):
            cart_item_set = request.user.cart_item_set.filter(product_id = product_id)
            for item in cart_item_set:
                updated_item_number = int(item.product_quantity) + int(quantity)
                print(updated_item_number)
                item.product_quantity = updated_item_number
                item.save()
        else:
            cart_item = request.user.cart_item_set.create(
                store_id = store_id,
                product_id = product_id,
                product_quantity = quantity,
            )
        return HttpResponse("")
    elif request.method == "POST" and not request.user.is_authenticated:
        store_id = request.POST.get("store_id")
        product_id = request.POST.get("product_id")
        textquantity = request.POST.get("quantity")
        cart = request.session.get('cart')
        if not cart:
            cart = {}
            request.session['cart'] = cart
            quantity = int(textquantity)
            cart[product_id] = {'store_id':store_id, 'quantity':quantity,'product_id':product_id,}
            return HttpResponse("")
        elif product_id not in cart:
            quantity = int(textquantity)
            cart[product_id] = {'store_id':store_id, 'quantity':quantity,'product_id':product_id,}
            request.session.modified = True
            return HttpResponse("")
        elif product_id in cart:
            quantity = int(textquantity)
            cart[product_id]['quantity'] += quantity
            request.session.modified = True
            return HttpResponse("")
        else:
            return HttpResponse("")
    else:
        return HttpResponse("")

def cart(request):
    template = loader.get_template("main/cart.html")
    if request.user.is_authenticated:
        email = request.user.email
        usercartitems = request.user.cart_item_set.all()
        cartitems = []
        store = ""
        totalprice = 0
        your_json_data = []
        numberofitemsincart = len(cartitems)
        for item in usercartitems:
            quantity = item.product_quantity
            store_id = item.store_id
            product_id = item.product_id
            storedetail = Store_detail.objects.get(pk = store_id)
            product = Product.objects.get(pk = product_id)
            # item = {"quantity":quantity, "product":product}
            # cartitems.extend([item])
            store = storedetail
            numberofitemsincart = len(cartitems)
            product = Product.objects.get(pk = product_id)
            totalproductprice = product.price * int(quantity)
            totalprice += totalproductprice

            product_price = int(product.price) * int(quantity)
            product_price = str(product_price)
            store_name = str(store.store_name)
            print(product.price)
            print(item.product_quantity)
            store_id = str(store_id)
            product_id = str(product_id)
            product_name = str(product.name)
            product_quantity = str(quantity)
            total_price = str(totalprice)

            cart_details = {'store_id':store_id,'product_id':product_id,'product_name':product_name,'product_quantity':product_quantity,'product_price':product_price,'total_price':total_price,'store_name':store_name,'total_price':total_price,}
            your_json_data.extend([cart_details])
        return JsonResponse(your_json_data, safe=False)
    elif request.user.is_authenticated is False:
        your_json_data = []
        if request.session.get('cart'):
            allitems = request.session['cart']
            your_json_data = []
            cartitems = []
            totalprice = 0
            for item in allitems.values():
                print(item)
                store_id = item['store_id']
                quantity = item['quantity']
                product_id = item['product_id']
                product = Product.objects.get(pk = product_id)
                store = Store_detail.objects.get(pk = store_id)
                totalproductprice = product.price * int(quantity)
                totalprice += totalproductprice
                cartdict = {'store':store,'product':product,'quantity':quantity,}
                cartitems.append(cartdict)
                product_price = int(product.price) * int(quantity)
                store_id = str(store_id)
                product_id = str(product_id)
                product_name = str(product.name)
                product_quantity = str(quantity)
                total_price = str(totalprice)
                store_name = str(store.store_name)
                cart_details = {'store_id':store_id,'product_id':product_id,'product_name':product_name,'product_quantity':product_quantity,'product_price':product_price,'total_price':total_price,'store_name':store_name,'total_price':total_price,}
                your_json_data.extend([cart_details])
        return JsonResponse(your_json_data, safe=False)
    else:
        return JsonResponse(your_json_data, safe=False)
def checkout(request):
    template = loader.get_template("main/checkout.html")
    if request.user.is_authenticated:
        email = request.user.email
        first_name = request.user.first_name
        last_name = request.user.last_name
        cartitems = []
        store = ""
        totalprice = 0
        if request.user.cart_item_set.all():
            usercartitems = request.user.cart_item_set.all()
            for item in usercartitems:
                quantity = item.product_quantity
                store_id = item.store_id
                product_id = item.product_id
                storedetail = Store_detail.objects.get(pk = store_id)
                product = Product.objects.get(pk = product_id)
                item = {"quantity":quantity, "product":product}
                cartitems.extend([item])
                store = storedetail
                numberofitemsincart = len(cartitems)
                product = Product.objects.get(pk = product_id)
                totalproductprice = product.price * int(quantity)
                totalprice += totalproductprice
                context={
                'store':store,
                'first_name':first_name,
                'last_name':last_name,
                'email':email,
                'cartitems':cartitems,
                'numberofitemsincart':numberofitemsincart,
                'totalprice':totalprice,
                }
        else:
            context={}
        return HttpResponse(template.render(context,request))
    elif request.user.is_authenticated is False:
        return redirect("main:login")
    else:
        return redirect("main:login")

def removecart(request,pk):
    if request.user.is_authenticated:
        if request.user.cart_item_set.filter(product_id = pk):
            cart_object = request.user.cart_item_set.filter(product_id = pk)
            cart_object.delete()
        return redirect("main:cart")
    if not request.user.is_authenticated:
        cart = request.session['cart']
        product_id = str(pk)
        del cart[product_id]
        request.session.modified = True
        return redirect("main:cart")

def storesearch(request):
    storesearchquery = request.session.get('storesearchsession')
    latitude = request.session['lat']
    longitude = request.session['lng']
    location = request.session['location']
    lat = float(latitude) # Central point latitude
    lng = float(longitude) # Central point longitude
    if request.user.is_authenticated:
        usercartitems = request.user.cart_item_set.all()
        numberofitemsincart = len(usercartitems)
    elif not request.user.is_authenticated and request.session.get('cart'):
        cartitems = request.session['cart']
        numberofitemsincart = len(cartitems)
    else:
        numberofitemsincart = 0
    radius = 10
    point = Point(lng, lat)
    queryset2 = Store_detail.objects.filter(store_location_point__distance_lt=(point, Distance(km=radius)))
    queryset4= queryset2.filter(Q( store_name__icontains = storesearchquery ))
    for query in queryset4:
        print(point.distance(query.store_location_point)*100)
    page = request.GET.get('page',1)
    queryset3 = Paginator(queryset4, 20)
    try:
        queryset = queryset3.page(page)
    except PageNotAnInteger:
        queryset = queryset3.page(1)
    except EmptyPage:
        queryset = Store_detail.objects.none()
    return render(request,"main/storesearch.html",{"storesearchquery":storesearchquery,"queryset":queryset,'numberofitemsincart':numberofitemsincart,})

def removecheckout(request,pk):
    if request.user.is_authenticated:
        if request.user.cart_item_set.filter(product_id = pk):
            cart_object = request.user.cart_item_set.filter(product_id = pk)
            cart_object.delete()
            print('deleted')
        return redirect("main:checkout")
    if not request.user.is_authenticated:
        cart = request.session['cart']
        product_id = str(pk)
        del cart[product_id]
        request.session.modified = True
        print('deleted')
        return redirect("main:checkout")
def logout(request):
    auth_logout(request)
    return redirect("main:home")
