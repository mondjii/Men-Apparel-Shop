from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (TemplateView,
                                  ListView, DetailView,
                                  FormView, CreateView, UpdateView, DeleteView)
from .models import Apparel, Cart
from .forms import ContactForm, AddCartForm

def redirecthome(request):
    return redirect('apparelapp:home')

class HomeView(TemplateView):
    template_name = "apparelapp/index.html"

class ApparelsView(ListView):
    model = Apparel
    template_name = "apparelapp/apparels.html"
    context_object_name = 'apparels'

class BottomwearListView(ListView):
    model = Apparel
    template_name = "apparelapp/bottomwear_list.html"
    context_object_name = 'apparels'

class TopwearListView(ListView):
    model = Apparel
    template_name = "apparelapp/topwear_list.html"
    context_object_name = 'apparels'

class FootwearListView(ListView):
    model = Apparel
    template_name = "apparelapp/footwear_list.html"
    context_object_name = 'apparels'

class ApparelDetailView(DetailView):
    model = Apparel
    template_name = "apparelapp/apparel_detail.html"




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
