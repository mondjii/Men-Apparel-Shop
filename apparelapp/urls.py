from django.urls import path
from .views import (HomeView, ApparelsView,
                    TopwearListView, BottomwearListView, FootwearListView,
                    ApparelDetailView, CartListView, CartDeleteView, CartUpdateView,
                    ContactFormView, UserInfoDetailView, CreateUser, OrderHistoryListView,
                    thankyoupage, redirecthome)

app_name = 'apparelapp'

urlpatterns = [
    path('', redirecthome, name='redirecthome'),
    path('home/', HomeView.as_view(), name='home'),

    path('catalog/', ApparelsView.as_view(), name='apparels'),
    path('catalog/topwears', TopwearListView.as_view(), name='topapparels'),
    path('catalog/bottomwears', BottomwearListView.as_view(), name='botapparels'),
    path('catalog/footwears', FootwearListView.as_view(), name='footapparels'),

    path('Addcart/<int:pk>/', ApparelDetailView.as_view(), name='addcart'),
    path('delete/<int:pk>/', CartDeleteView.as_view(), name='delete'),
    path('update/<int:pk>/', CartUpdateView.as_view(), name='update'),
    path('cart/', CartListView.as_view(), name='cart'),

    path('/history', OrderHistoryListView.as_view(), name='history'),
    # path(),

    path('account/', UserInfoDetailView.as_view(), name='account'),
    path('register/', CreateUser.as_view(), name='register'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('thankyou/', thankyoupage, name='thankyou')
]
