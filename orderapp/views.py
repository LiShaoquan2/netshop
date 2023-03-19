import jsonpickle
from django.http import HttpResponseRedirect
from django.shortcuts import render
from cartapp.cartmanager import DBCartManger

# Create your views here.
def toOrder(request):
    cartitems = request.GET.get('cartitems','')
    # 获取支付总金额
    totalPrice = request.GET.get('totalPrice','')

    #判断是否登录
    if not request.session.get('user'):
        print('没有用户')
        # return HttpResponseRedirect(f'/user/login/?reflag=order&cartitems={cartitems}')
        return render(request,'login.html',{'reflag':'order','cartitems':cartitems})

    #反序列化cartiItems
    cartitemsList = jsonpickle.loads(cartitems)

    #获取默认收货地址
    user = jsonpickle.loads(request.session.get('user',''))
    addrObj = user.address_set.filter(isdefault = True)[0]
    print(addrObj)
    #获取订单内容
    cartItemObjList = [DBCartManger(user).get_cartitems(**(jsonpickle.loads(item))) for item in cartitemsList if item ]

    context ={
        'cartitemsObjList':cartItemObjList,
        'addrObj':addrObj,
        'totalPrice':totalPrice,

    }
    return render(request,'order.html',context)