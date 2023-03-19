from django.urls import path

from goodsapp import views

urlpatterns=[
    path('',views.IndexView),
    path('category/<int:categoryid>/page/<int:num>/',views.IndexView),
    path('goodsdetails/<int:goodsid>/',views.DetailView)
]