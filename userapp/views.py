import jsonpickle
from django.core.serializers import serialize
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from cartapp.cartmanager import SessionCartManager
from userapp.code import gene_code
from userapp.models import UserInfo, Area, Address


def login(request):
    if request.method == 'GET':
        reflag = request.GET.get('reflag')
        return render(request,'login.html',{'reflag':reflag})
    else:
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        reflag = request.POST.get('reflag')
        cartitems = request.POST.get('cartitems')
        #判断是否登陆成功
        user = UserInfo.objects.filter(uname=uname , pwd = pwd)
        if user:
            request.session['user'] = jsonpickle.dumps(user[0])

            #将Session中的购物车传入到数据库中
            SessionCartManager(request.session).migrateSession2DB()
            if reflag == 'cart':
                return HttpResponseRedirect('/cart/queryAll/')
            elif reflag=='order':
                return HttpResponseRedirect(f'/order/?cartitems={cartitems}')
            return HttpResponseRedirect('/user/center/')
        return HttpResponseRedirect('/user/login/')


def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')

        try:
            user = UserInfo.objects.get(uname=uname)
            print("注册失败")
            return render(request,'register.html',{'flag':True})
        except UserInfo.DoesNotExist:
            user = UserInfo.objects.create(uname=uname,pwd=pwd)
            #将对象存入session
            request.session['user'] = jsonpickle.dumps(user)
            print("注册成功")
            return HttpResponseRedirect('/user/center/')


def center(request):
    return render(request,'center.html')


def checkUname(request):
    try:
        uname = request.GET.get('uname')
        user = UserInfo.objects.get(uname=uname)
        flag = True
        return JsonResponse({'flag':flag})
    except:
        return JsonResponse({'flag':False})


def logout(request):
    request.session.flush()
    try:
        print(request.session.get('user'))
    except:
        print("已删除")
    return JsonResponse({"logout":True })


def loadcode(request):
    if request.method == 'Get':
        imgObj,code = gene_code()

        return HttpResponse(imgObj,content_type='image/png')

class loadCodeView(View):
    def get(self,request):
        imgObj,code = gene_code()
        request.session['session_code']=code
        return HttpResponse(imgObj,content_type='image/png')


class CheckCodeView(View):
    def get(self,request):
        code = request.GET.get('code',-1)
        session_code = request.session.get('session_code',-2)
        vflage = False
        if code == session_code:
            vflage = True
        return JsonResponse({'checkFlag':vflage})


def address(request):
    if request.method == 'GET':
        #获取当前登录用户的所有地址信息
        userstr = request.session.get('user','')
        if userstr:
            user = jsonpickle.loads(userstr)
        addr_list = user.address_set.all()
        context={
            'addr_list':addr_list,
        }

        return render(request,'address.html',context)
    else:
        #获取请求参数
        aname = request.POST.get('aname','')
        aphone = request.POST.get('aphone','')
        addr = request.POST.get('addr','')

        #获取当前登录对象
        userstr = request.session.get('user','')
        if userstr:
            user = jsonpickle.loads(userstr)

        #插入到数据库表
        Address.objects.create(aname=aname,aphone=aphone,addr=addr,userinfo=user,isdefault=(False if user.address_set.count() > 0 else True))

        return HttpResponseRedirect('/user/address/')



def loadarea(request):
    pid = request.GET.get('pid')
    pid = int(pid)

    areaList = Area.objects.filter(parentid = pid)
    # print(areaList)
    #序列化数据
    jareaList = serialize('json',areaList)
    # print(jareaList)
    return JsonResponse({'jareaList':jareaList})


def updateDefault(request):
    addrid = request.GET.get('addrid',-1)
    addrid = int(addrid)
    #修改数据
    Address.objects.filter(id = addrid).update(isdefault=True)
    Address.objects.exclude(id = addrid).update(isdefault=False)

    return HttpResponseRedirect('/user/address/')