from django.shortcuts import render

import json
import time
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import *

from .shows import *
from .shops import *

# Create your views here.

def index(request):
    # Check if User
    if request.user in User.objects.all():
        user_products = request.user.products.all()
        user_shows = request.user.shows.all()
        return render(request, "app/index.html", {
            'products': user_products,
            'shows': user_shows,
        })
    else:
        return render(request, "app/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "app/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "app/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "app/register.html")


def shows(request):
    url = 'https://www.netflix.com/sg/browse/genre/83'
    jsonResp = returnPopularShows(url)

    if 'error' in jsonResp.keys():
        return JsonResponse({
            'message': 'Page not loaded, try again later.'
        }, status=400)
    else:
        #return JsonResponse(jsonResp, status=200)
        return render(request, "app/shows.html", jsonResp)

def shops(request):
    url = 'https://www.amazon.sg/gp/bestsellers/'
    jsonResp = returnProducts(url, 6)
    
    #return JsonResponse(jsonResp, status=200)
    return render(request, "app/shops.html", jsonResp)
    
    
@csrf_exempt
def add_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Check if User
        if request.user in User.objects.all():
            curr_user = User.objects.get(username=request.user)            
            item = Product(
                name = data['name'],
                price = data['price'],
                url = data['url'],
                img = data['img'],
            )
            if item.name not in [str(i) for i in Product.objects.all()]:
                item.save()
            else:
                item = Product.objects.get(name=item.name)
            if item.name not in [str(i) for i in curr_user.products.all()]:
                curr_user.products.add(item)
                curr_user.save()
                return JsonResponse(data, status=200)
            else:
                return JsonResponse({
                    'message': 'Item already in watchlist',
                }, status=200)
        else:
            return JsonResponse({
                'message': 'Not signed in',
            }, status=200)
    else:
        return render(request, "app/index.html")
    
    
@csrf_exempt
def add_show(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Check if User
        if request.user in User.objects.all():
            curr_user = User.objects.get(username=request.user)            
            item = Show(
                name = data['name'],
                genre = data['genre'],
                url = data['url'],
                img = data['img'],
            )
            if item.name not in [str(i) for i in Show.objects.all()]:
                item.save()
            else:
                item = Show.objects.get(name=item.name)
            if item.name not in [str(i) for i in curr_user.shows.all()]:
                curr_user.shows.add(item)
                curr_user.save()
                return JsonResponse(data, status=200)
            else:
                return JsonResponse({
                    'message': 'Item already in watchlist',
                }, status=200)
        else:
            return JsonResponse({
                'message': 'Not signed in',
            }, status=200)
    else:
        return render(request, "app/index.html")
        
        
@csrf_exempt
def remove(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Check if User
        if request.user in User.objects.all():
            curr_user = User.objects.get(username=request.user)     
            item_name = data['name']
            if data['type'] == "0":    # Product
                item = Product.objects.get(name=item_name)
                curr_user.products.remove(item)
                curr_user.save()
                return JsonResponse({
                    'message': 'Product removed from watchlist',
                }, status=201)
            elif data['type'] == "1":    # Show
                item = Show.objects.get(name=item_name)
                curr_user.shows.remove(item)
                curr_user.save()
                return JsonResponse({
                    'message': 'Show removed from watchlist',
                }, status=201)
        else:
            return JsonResponse({
                'message': 'Not signed in',
            }, status=200)
    else:
        return render(request, "app/index.html")