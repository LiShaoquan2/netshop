from django.db import models

# Create your models here.
from goodsapp.models import Color, Size, Goods
from userapp.models import UserInfo


class CartItem(models.Model):
    goodsid = models.PositiveIntegerField()
    colorid = models.PositiveBigIntegerField()
    sizeid = models.PositiveIntegerField()
    count = models.PositiveIntegerField(default=0)
    isdelete = models.BooleanField(default=False)
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE)

    def getColor(self):
        return Color.objects.get(id = self.colorid)

    def getSize(self):
        return Size.objects.get(id = self.sizeid)

    def getGoods(self):
        return Goods.objects.get(id = self.goodsid)

    def getSum(self):
        return int(self.count)*int(self.getGoods().price)