from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from moderator.models import Store_detail
from moderator.models import Store_image
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.gis.geos import Point


def login(request):
    username = request.POST.get("email")
    password = request.POST.get("password")
    if request.method == "POST":
        try:
            user = User.objects.get(username=username)
            if user.is_superuser:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth_login(request, user,)
                return redirect( 'moderator:home')
            elif user.is_superuser == False:
                return redirect( 'main:home')
        except User.DoesNotExist:
            error_message = "Your login details are incorrect"
            return render(request,"moderator/login.html",{"error_message":error_message})
    elif request.user.is_authenticated and request.user.is_superuser:
        return redirect('moderator:home')
    else:
        return render(request, 'moderator/login.html')

def home(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request,"moderator/home.html")
    else:
        return redirect("main:home")
def logout(request):
    auth_logout(request)
    return redirect("main:home")
def create(request):
    template = loader.get_template("moderator/create.html")
    if request.method == "POST":
        if request.POST.get("name") is not '' and request.POST.get("lat") is not '' and request.POST.get("lng") is not '' and request.POST.get("opentime") is not '' and request.POST.get("closetime") is not '' and request.POST.get("location") is not '' and request.POST.get("category") is not '':
            store_name = request.POST.get("name")
            store_lat = float(request.POST.get("lat"))
            store_lng = float(request.POST.get("lng"))
            store_open = request.POST.get("opentime")
            store_close = request.POST.get("closetime")
            store_location = request.POST.get("location")
            store_category = request.POST.get("category")
            if request.FILES.get("image") is not None or '':
                store_location_point = Point(store_lng, store_lat, srid=4326)
                store_detail = Store_detail(store_name =store_name, store_lat =store_lat,store_lng =store_lng,store_open =store_open,store_close =store_close, store_location = store_location,store_category = store_category,store_location_point = store_location_point,)
                store_detail.save()
                store_image = request.FILES['image']
                image = Store_image( image=store_detail, store_image = store_image)
                image.save()
                context = {}
            else:
                error_message = "Add a store Image"
                context = {
                    "error_message":error_message,
                }
            return HttpResponse(template.render(context,request))
        else:
            error_message = "Please fill out form completely"
            context = {
                "error_message":error_message,
            }
            return HttpResponse(template.render(context,request))
    else:
        context={}

        return HttpResponse(template.render(context,request))

def modify(request):
    template = loader.get_template("moderator/modify.html")
    context = {}
    if request.method == "POST":
        query = request.POST.get("searchquery")
        try:
            queryresults = Store_detail.objects.filter( Q( store_name__icontains = query ) )
            if queryresults.exists():
                context = {
                    "queryresults":queryresults,
                }

                return HttpResponse(template.render(context,request))
            elif queryresults.exists() is False:
                couldnt_locate_store = "Sorry we couldn't find the store you're looking for"
                return render(request, 'moderator/modify.html',  {"couldnt_locate_store": couldnt_locate_store,})
            else:
                couldnt_locate_store = "Sorry we couldn't find the store you're looking for"
                return render(request, 'moderator/modify.html',  {"couldnt_locate_store": couldnt_locate_store,})
        except ObjectDoesNotExist:
            couldnt_locate_store = "Sorry we couldn't find the store you're looking for"
            return render(request, 'moderator/modify.html',  {"couldnt_locate_store": couldnt_locate_store,})

    else:
        queryresults = ""
        context = {
            "queryresults":queryresults,
        }
        return HttpResponse(template.render(context,request))

def manageproducts(request,slug,pk):
    template = loader.get_template("moderator/manageproducts.html")
    if Store_detail.objects.exists():
        queryresult = Store_detail.objects.get(pk=pk)
        context = {
            "queryresult":queryresult,
            }
    else:
        context = {}
    return HttpResponse(template.render(context,request))

def manageallproducts(request,slug,pk):
    template = loader.get_template("moderator/manageallproducts.html")
    queryresult = Store_detail.objects.get(pk=pk)
    products =  queryresult.product_set.all()
    context = {
        "products":products,
    }
    return HttpResponse(template.render(context,request))
def addproduct(request,slug,pk):
    Store = Store_detail.objects.get(pk=pk)
    if request.method == "POST":
        name = request.POST.get("name")
        price2 = int(request.POST.get("price"))
        price3 = price2/100 * 10
        price = price2 + price3
        description = request.POST.get("description")
        image = request.FILES['image']
        Store.product_set.create(name=name,price=price,description=description,product_image=image,)
    return render(request,"moderator/addproduct.html")

def deleteproduct(request,pk):
    Store = Store_detail.objects.get(pk=1)
    product = Store.product_set.get(pk=pk)
    product.delete()
    return redirect('moderator:modify')
