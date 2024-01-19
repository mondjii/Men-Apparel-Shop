from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (TemplateView,
                                  ListView, DetailView,
                                  FormView, CreateView, UpdateView, DeleteView )
from django.views.generic.edit import ModelFormMixin
from .models import Apparel, Cart
from .forms import ContactForm, AddCartForm

from decimal import Decimal

def redirecthome(request):
    return redirect('apparelapp:home')

class HomeView(TemplateView):
    template_name = "apparelapp/index.html"

class ApparelsView(TemplateView):
    template_name = "apparelapp/apparels.html"
    
class BottomwearListView(ListView):
    model = Apparel
    template_name = "apparelapp/bottomwear_list.html"
    context_object_name = 'apparels'
    
    def get_queryset(self):
        return super().get_queryset().filter(type='Bottomwear')

class TopwearListView(ListView):
    model = Apparel
    template_name = "apparelapp/topwear_list.html"
    context_object_name = 'apparels'

    def get_queryset(self):
        return super().get_queryset().filter(type='Topwear')
    
class FootwearListView(ListView):
    model = Apparel
    template_name = "apparelapp/footwear_list.html"
    context_object_name = 'apparels'

    def get_queryset(self):
        return super().get_queryset().filter(type='Footwear')
    
class ApparelDetailView(DetailView):
    model = Apparel
    context_object_name = 'apparel_details'
    template_name = "apparelapp/apparel_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_form"] = AddCartForm()
        return context
    
    def post(self, request, *args, **kwargs):
        apparel = self.get_object()
        form = AddCartForm(request.POST)
        
        if form.is_valid(): 
            qty = form.cleaned_data['quantity']
            total_price = Decimal(apparel.price) * Decimal(qty)
            sz = form.cleaned_data['size']

            cart_item = Cart.objects.filter(product_purchase=apparel).first()

            if cart_item:
                cart_item.quantity += int(qty)
                cart_item.total_amount += Decimal(total_price)
                cart_item.save()
            else:
                Cart.objects.create(product_purchase=apparel,quantity=qty,size=sz,total_amount=float(total_price))
            return redirect('apparelapp:thankyou')
        else:
            context = self.get_context_data()
            context['cart_form'] = form
            return self.render_to_response(context)

    
class CartListView(ListView):
    model = Cart
    template_name = "apparelapp/cart_list.html"
    context_object_name = 'items'

class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'apparelapp/contact_form.html'
    success_url = reverse_lazy('apparelapp:thankyou')

    def form_valid(self, form):
        print(form.cleaned_data)
        #send email to me
        return super().form_valid(form)

def thankyoupage(request):
    return render(request,'apparelapp/thankyou.html')

