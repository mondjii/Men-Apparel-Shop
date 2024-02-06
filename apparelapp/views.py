from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import (TemplateView,
                                  ListView, DetailView,
                                  FormView, UpdateView, DeleteView )

from django.contrib.auth.mixins import LoginRequiredMixin #for CBV
from django.shortcuts import get_object_or_404
from .extras import send_email

from django.contrib.auth.models import Group, User

from .models import Apparel, CartItem, UserInfo
from .forms import ContactForm, AddCartForm, NewUserForm

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
    #ask if possible: want multile filters with different name
    #

class FootwearListView(ListView):
    model = Apparel
    template_name = "apparelapp/footwear_list.html"
    context_object_name = 'apparels'

    def get_queryset(self):
        return super().get_queryset().filter(type='Footwear')

class ApparelDetailView(LoginRequiredMixin, DetailView):
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
        buyer = UserInfo.objects.get(user=self.request.user)
        
        if form.is_valid(): 
            qty = form.cleaned_data['quantity']
            total_price = Decimal(apparel.price) * Decimal(qty)
            sz = form.cleaned_data['size'].strip()

            cart_item = CartItem.objects.filter(product_purchase=apparel, size=sz).first()

            if cart_item:
                cart_item.quantity += int(qty)
                cart_item.total_amount += Decimal(total_price)
                cart_item.save()
            else:
                CartItem.objects.create(cart_owner=buyer,product_purchase=apparel,quantity=qty,size=sz,total_amount=float(total_price))
            return redirect('apparelapp:thankyou')
        else:
            context = self.get_context_data()
            context['cart_form'] = form
            return self.render_to_response(context)

class CartListView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = "apparelapp/cart_list.html"
    context_object_name = 'items'

    def get_queryset(self):
        return CartItem.objects.filter(cart_owner__user=self.request.user)
    
    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        total_eachitems = self.get_queryset()
        total = Decimal(sum([Decimal(item.total_amount) for item in total_eachitems]))
        context["total"] = total
        return context
    

class CartUpdateView(LoginRequiredMixin, UpdateView):
    model = CartItem
    template_name = "apparelapp/cart_update.html"
    fields = ['quantity', 'size']
    context_object_name = 'items'

    success_url = reverse_lazy('apparelapp:cart')

class CartDeleteView(LoginRequiredMixin, DeleteView):
    model = CartItem
    template_name = "apparelapp/cart_delete.html"
    success_url = reverse_lazy('apparelapp:cart')

    context_object_name = 'items'

class UserInfoDetailView(LoginRequiredMixin, DetailView):
    model = UserInfo
    template_name = "apparelapp/account_detail.html"
    context_object_name = 'userinfo'

    def get_object(self, queryset=None):
        user_info = get_object_or_404(UserInfo, user=self.request.user)
        return user_info
    
class CreateUser(FormView):
    form_class = NewUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def checkuserexists(self, username):
        if User.objects.filter(username=username).exists():
            return True
        else:
            return False

    def form_valid(self, form):
        username = form.cleaned_data['username'].strip()

        if self.checkuserexists(username=username):
            form.add_error('username', 'This username is already taken. Please choose a different one.')
            return self.form_invalid(form)
        else:
            password = form.cleaned_data['password']
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            loc = form.cleaned_data['location']
            pnum = form.cleaned_data['pnumber']
            profpic = form.cleaned_data['profile']

            #creating user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = firstname
            user.last_name = lastname

            #adding user to the group
            group = Group.objects.get(name='customers')
            user.groups.add(group)
            user.save()
            
            #create user's info
            UserInfo.objects.create(user=user, location=loc, pnumber=pnum, profilepic=profpic)
            return super().form_valid(form)
    
class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'apparelapp/contact_form.html'
    success_url = reverse_lazy('apparelapp:thankyou')

    def form_valid(self, form):
        send_email(form.cleaned_data['fullname'],
                   form.cleaned_data['subject'],
                   form.cleaned_data['phonenumber'],
                   form.cleaned_data['gmail'],
                   form.cleaned_data['comments'])
        return super().form_valid(form)
    
def thankyoupage(request):
    return render(request,'apparelapp/thankyou.html')

