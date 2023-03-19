from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from cartapp.cartmanager import getCartManger


def cart(request):
    if request.method == 'POST':
        # del request.session['cart']
        print(request.session.keys())
        #获取变量
        flag = request.POST.get('flag')
        if flag == 'add':
            cartMangerObj = getCartManger(request)
            cartMangerObj.add(**request.POST.dict())

        elif flag == 'plus':
            cartMangerObj = getCartManger(request)
            cartMangerObj.update(step=1 , **request.POST.dict())

        elif flag == 'minus':
            cartMangerObj = getCartManger(request)
            cartMangerObj.update(step=-1, ** request.POST.dict())

        elif flag == 'delete':
            cartMangerObj = getCartManger(request)
            cartMangerObj.delete(**request.POST.dict())

        # print(request.session['cart'])
        try:
            request.session['cart'] = request.session['cart']
        except:
            print('cart添加失败')
        return  HttpResponseRedirect('/cart/queryAll/')


def queryAll(request):
    # del request.session['cart']['11,22,17']
    if request.method == 'GET':
        # print('删除前')
        # print(request.session['cart'])
        # print('删除后')
        # print(request.session['cart'])
        # print(request.session['cart'].keys())
        cartMangerObj = getCartManger(request)
        cartItemList = cartMangerObj.queryAll()

        return render(request,'cart.html',{'cartItemList':cartItemList})