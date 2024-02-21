from django.shortcuts import render,HttpResponse, get_object_or_404,redirect
from . models import *
from django.http import JsonResponse
import json
import datetime
from . utils import cookieCart,guestOrder,cartData
from django.db.models import Q
from django.http import Http404

# Create your views here.

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    products = Product.objects.all()
    context = {'products':products , 'cartItems':cartItems}
    return render(request, 'shop/store.html',context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']



    context = {'items':items , 'order':order ,'cartItems':cartItems}
    return render(request, 'shop/cart.html',context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items , 'order':order , 'cartItems':cartItems}
    return render(request, 'shop/checkout.html',context)



def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == float(order.get_cart_total):
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		pincode=data['shipping']['pincode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

def product_detail(request,pk):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    query = Product.objects.filter(id=pk)
    if query.exists() and query.count() == 1:
        instance = query.first()
    else:
        return Http404("Product data does not Exists")
    context = {'items':items , 'order':order ,'cartItems':cartItems,'data':instance}
    
    return render(request,'shop/view-detail.html',context)



def search_product(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    if request.method == 'GET':
        searched_data = request.GET.get('search')
        if(len(searched_data)==0):
            return HttpResponse("NO SUCH PRODUCT")
            # return Http404("No Such Data")
        else:
            # r= Producesult t.objects.filter(name__icontains=searched_data)
            query = (Q(name__icontains=searched_data) | Q(price__icontains=searched_data))
            result = Product.objects.filter(query)
                
            context = {'items':items , 'order':order ,'cartItems':cartItems,'order':result}
            return render(request,'shop/search-list.html',context)
    else:
        return HttpResponse("Invalid Method")


def men_list(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    men_data = Product.objects.filter(cloth_type='M')
    
    context = {'items':items , 'order':order ,'cartItems':cartItems,'objects':men_data}
    return render(request,'shop/men-list.html',context)



def women_list(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    women_data = Product.objects.filter(cloth_type='W')
    
    context = {'items':items , 'order':order ,'cartItems':cartItems,'objects1':women_data}
    return render(request,'shop/women-list.html',context)

def kids_list(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    kids_data = Product.objects.filter(cloth_type='K')
    
    context = {'items':items , 'order':order ,'cartItems':cartItems,'objects2':kids_data}
    return render(request,'shop/kids-list.html',context)

def book_list(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    books_data = Product.objects.filter(cloth_type='B')
    
    context = {'items':items , 'order':order ,'cartItems':cartItems,'objects3':books_data}
    return render(request,'shop/book-list.html',context)

def delete_cart_product(request,id):
    cart = OrderItem.objects.get(id=id)
    cart.delete()
    return redirect('cart')
