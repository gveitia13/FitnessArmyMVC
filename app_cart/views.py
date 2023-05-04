import json

from django.contrib import messages
from django.http import HttpRequest, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from FitnessArmyMVC.settings import CART_SESSION_ID
from app_cart.cart import Cart
from app_main.models import Product
from app_main.serializers import ProductSerializer


# @require_POST
@method_decorator(csrf_exempt, require_POST)
def add(request: HttpRequest, id: int):
    cart = Cart(request)
    print(str(cart))
    cart.add(product=Product.objects.filter(id=id).first())
    return JsonResponse({
        'product': ProductSerializer(Product.objects.get(id=id)).data,
        "result": "ok",
        "amount": cart.session[CART_SESSION_ID].get(id, {"quantity": 0})["quantity"]
    })


@require_POST
def cart_detail(request: HttpRequest, id: int):
    return JsonResponse({"result": Cart(request).get_item(id)})


@method_decorator(csrf_exempt, require_POST)
def cart_clear(request: HttpRequest):
    Cart(request).clear()
    return JsonResponse({"result": "ok", "amount": 0})


# @require_POST
@method_decorator(csrf_exempt, require_POST)
def item_clear(request: HttpRequest, id: int):
    cart = Cart(request)
    cart.remove(product=Product.objects.filter(id=id).first())
    return JsonResponse({
        'product': ProductSerializer(Product.objects.filter(id=id).first()).data,
        "result": "ok",
        "amount": cart.get_sum_of("quantity")
    })


@require_POST
def remove_quant(request: HttpRequest, id: int, quantity: int):
    Cart(request).add(product=Product.objects.filter(id=id).first(), quantity=quantity, action="remove")
    return JsonResponse({"result": "ok"})


@method_decorator(csrf_exempt, require_POST)
def update_quant(request: HttpRequest, id: int, value: int):
    cart = Cart(request)
    product = Product.objects.get(pk=id)
    cart.update_quant(product=product, value=value)
    total = 0
    for item in cart.session[CART_SESSION_ID]:
        total = total + (float(cart.session[CART_SESSION_ID].get(item)['product']['price']) *
                         float(cart.session[CART_SESSION_ID].get(item)['quantity']))
    print(request.path)
    if not request.path.__contains__('cart'):
        messages.success(request, f'{product.name} fue actualizado en el carrito')
    return JsonResponse({
        "result": "ok",
        "total": total,
        'product': ProductSerializer(product).data,
        "amount": cart.session[CART_SESSION_ID].get(id, {"quantity": value})["quantity"],
    })


@method_decorator(csrf_exempt, require_POST)
def update_cart(request: HttpRequest):
    cart = Cart(request)
    lista = json.loads(request.body)
    for i in lista:
        product = Product.objects.get(pk=i['id'])
        cart.update_quant(product=product, value=i['cant'])
    return JsonResponse({
        "result": "ok",
    })


@method_decorator(csrf_exempt, require_POST)
def remove(request: HttpRequest, id: int):
    Cart(request).decrement(product=Product.objects.filter(id=id).first())
    return JsonResponse({"result": "ok"})


@method_decorator(csrf_exempt, require_POST)
def cart_pop(request: HttpRequest, ):
    cart = Cart(request)
    cart.pop()
    return JsonResponse({
        "result": "ok",
        "amount": cart.get_sum_of("quantity")
    })


@method_decorator(csrf_exempt, require_POST)
def add_quant(request: HttpRequest, id: int, quantity: int):
    cart = Cart(request)
    product = Product.objects.filter(id=id).first()
    cart.add(product, quantity)
    total = 0
    for item in cart.session[CART_SESSION_ID]:
        total = total + (float(cart.session[CART_SESSION_ID].get(item)['product']['price']) *
                         float(cart.session[CART_SESSION_ID].get(item)['quantity']))
    messages.success(request, f'{product.name} fue añadido al carrito')
    # return redirect('catalog')
    return JsonResponse({"result": "ok",
                         'product': ProductSerializer(product).data,
                         "amount": cart.session[CART_SESSION_ID].get(id, {"quantity": quantity})["quantity"],
                         "total": total,
                         'url': reverse_lazy('catalog')
                         })
