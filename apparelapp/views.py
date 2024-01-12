from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (TemplateView,
                                  ListView, DetailView,
                                  FormView, CreateView, UpdateView, DeleteView)
from .models import Apparel, Cart
from .forms import ContactForm, AddCartForm

def redirecthome(request):
    return redirect('apparelapp:home')
# Create your views here.
class HomeView(TemplateView):
    template_name = "apparelapp/index.html"

class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'apparelapp/contact_form.html'

    def form_valid(self, form):
        print(form.cleaned_data)
        #send email to me
        return super().form_valid(form)
    
class ApparelListView(ListView):
    model = Apparel
    template_name = "apparelapp/apparel_list.html"
    context_object_name = 'apparel'

class ApparelDetailView(DetailView):
    model = Apparel
    template_name = "apparelapp/apparel_detail.html"


class CartListView(ListView):
    model = Cart
    template_name = "apparelapp/cart_list.html"
    context_object_name = 'items'


def thankyoupage(request):
    return render('apparelapp/thankyou.html')
