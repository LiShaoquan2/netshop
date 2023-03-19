from django.urls import path

from userapp import views

urlpatterns ={
    path('login/',views.login),
    path('register/',views.register),
    path('center/',views.center),
    path('checkUname/',views.checkUname),
    path('logout/',views.logout),
    path('loadCode/',views.loadCodeView.as_view()),
    path('checkcode/',views.CheckCodeView.as_view()),
    path('address/',views.address),
    path('loadArea/',views.loadarea),
    path('updateDefaultAddr/',views.updateDefault)
}