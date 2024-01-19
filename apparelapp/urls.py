from django.urls import path
from .views import (HomeView, ApparelsView,
                    TopwearListView, BottomwearListView, FootwearListView,
                    ApparelDetailView, CartListView,
                    ContactFormView,
                    thankyoupage, redirecthome)

app_name = 'apparelapp'

urlpatterns = [
    path('', redirecthome, name='redirecthome'),
    path('home/', HomeView.as_view(), name='home'),

    path('apparels/', ApparelsView.as_view(), name='apparels'),
    path('apparels/topwears', TopwearListView.as_view(), name='topapparels'),
    path('apparels/bottomwears', BottomwearListView.as_view(), name='botapparels'),
    path('apparels/footwears', FootwearListView.as_view(), name='footapparels'),

    path('Addcart/<int:pk>/', ApparelDetailView.as_view(), name='addcart'),
    path('cart/', CartListView.as_view(), name='cart'),

    path('contact/', ContactFormView.as_view(), name='contact'),
    path('thankyou/', thankyoupage, name='thankyou')
]
