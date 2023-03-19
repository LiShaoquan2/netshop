from django.urls import path

from cartapp import views

urlpatterns = [
    path('',views.cart),
    path('queryAll/',views.queryAll)
]