import math
from functools import wraps

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from goodsapp.models import Category, Goods


def IndexView(request,categoryid=12,num=1):
    if request.method == 'GET':
        categoryid=int(categoryid)
        # print(categoryid)
        categoryName = Category.objects.filter(id = categoryid).first()
        # print(categoryName)
        #获取商品信息
        categoryList =  Category.objects.all().order_by('id')
        #获取类别下的商品
        goodsList = Goods.objects.filter(category=categoryid)
        #添加分页
        paginatorObj = Paginator(object_list=goodsList,per_page=8)
        page_good_obj = paginatorObj.page(num)
        start = num-math.ceil(10/2)
        # 如果第一个页码小于1强制设置为1
        start = start if  start > 1 else 1
        # 最后一个页码最大为start+9
        end = start + 9
        #如果最大页码超过总页数，将总页数作为最大页码
        end = end if end<paginatorObj.num_pages else paginatorObj.num_pages
        #如果最大页码在10内，开始页码作为1
        #如果终止页码超过10，开始页码为end-9
        start = 1 if end <10 else (end-9)

        page_list = range(start,end+1)

        # print(len(goodsList))
        context={
            'goodsList':page_good_obj,
            'cateoryList':categoryList,
            'currentCid':categoryid,
            'page_list':page_list
        }
        return render(request,'index.html',context=context)

def recommand(func):
    def _wrapper(request,goodsid,*args,**kwargs):
        #获取cookie中的goodsid
        c_goodsid = request.COOKIES.get('c_goodsid','')

        #存放访问过的商品ID列表
        goodIdList = [id for id in c_goodsid.split() if id.strip()]
        #存放用户访问过的商品对象列表
        goodsObjList = [Goods.objects.get(id = gid) for gid in goodIdList[:4] if gid!=goodsid and Goods.objects.get(id = gid).category_id ==Goods.objects.get(id=goodsid).category_id]
        # print(goodsid)
        goodsid = str(goodsid)
        # print(type(goodsid))
        # print(goodIdList)
        if goodsid in goodIdList:
            goodIdList.remove(goodsid)
            goodIdList.insert(0,goodsid)
        else :
            goodIdList.insert(0,goodsid)
        # 调用视图方法
        # print(type(goodIdList[0]))
        goodIdList=[str(id) for id in goodIdList ]
        response = func(request,goodsid,recommand_list = goodsObjList,*args,**kwargs)
        #将用户访问难过的商品ID列表存放之cookie中
        response.set_cookie('c_goodsid',' '.join(goodIdList),max_age = 3*24*60*60)
        return response
    return _wrapper


@recommand
def DetailView(request,goodsid,recommand_list):
    if request.method == 'GET':
        goodsid = int(goodsid)
        #根据商品id查询信息
        try:
            goods = Goods.objects.get(id = goodsid)
            return render(request,'detail.html',{'goods':goods,'recommand_list':recommand_list})
        except Goods.DoesNotExist:
            return HttpResponse(status=404)
