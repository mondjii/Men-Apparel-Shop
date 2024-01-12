from django.urls import path
from .views import (HomeView,
                    ApparelListView, ApparelDetailView, CartListView,
                    ContactFormView,
                    thankyoupage, redirecthome)

app_name = 'apparelapp'

urlpatterns = [
    path('', redirecthome, name='redirecthome'),
    path('home/', HomeView.as_view(), name='home'),
    path('apparels/', ApparelListView.as_view(), name='apparels'),
    path('Addcart/<int:pk>', ApparelDetailView.as_view(), name='addcart'),
    path('cart/', CartListView.as_view(), name='cart'),

    path('contact/', ContactFormView.as_view(), name='contact'),
    path('thankyou/', thankyoupage, name='thankyou')
]
