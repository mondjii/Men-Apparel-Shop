from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from django.views.generic import (TemplateView,
                                  ListView, DetailView,
                                  FormView, UpdateView, DeleteView )

from django.contrib.auth.mixins import LoginRequiredMixin #for CBV
from django.shortcuts import get_object_or_404
from .extras import send_email

from django.contrib.auth.models import Group, User

from .models import Apparel, CartItem, UserInfo, OrderHistoryList
from .forms import (ContactForm,
                    BotwearForm,TopwearForm,FootwearForm,
                    TopUpdateForm, BotUpdateForm, FootUpdateForm,
                    NewUserForm)

from decimal import Decimal

def redirecthome(request):
    return redirect('apparelapp:home')

#class views for template only
class HomeView(TemplateView):
    template_name = "apparelapp/index.html"

class ApparelsView(TemplateView):
    template_name = "apparelapp/apparels.html"

#classview that display the model
class BottomwearListView(ListView):
    model = Apparel
    template_name = "apparelapp/bottomwear_list.html"
    context_object_name = 'apparels'
    
    #to filter by type, in this case it will only select all bottomwears
    def get_queryset(self):
        queryset = super().get_queryset().filter(type='Bottomwear')
        sortbased = self.request.GET.get('radiofilter')

        #radio form that pass the value then sort by using order_by
        if sortbased == 'htol':
            queryset = queryset.order_by('-price')
        elif sortbased == 'ltoh':
            queryset = queryset.order_by('price')
        else:
            queryset = queryset
        return queryset

class TopwearListView(ListView):
    model = Apparel
    template_name = "apparelapp/topwear_list.html"
    context_object_name = 'apparels'

    def get_queryset(self):
        queryset = super().get_queryset().filter(type='Topwear')
        sortbased = self.request.GET.get('radiofilter')

        if sortbased == 'htol':
            queryset = queryset.order_by('-price')
        elif sortbased == 'ltoh':
            queryset = queryset.order_by('price')
        else:
            queryset = queryset
        return queryset

class FootwearListView(ListView):
    model = Apparel
    template_name = "apparelapp/footwear_list.html"
    context_object_name = 'apparels'

    def get_queryset(self):
        queryset = super().get_queryset().filter(type='Footwear')
        sortbased = self.request.GET.get('radiofilter')

        if sortbased == 'htol':
            queryset = queryset.order_by('-price')
        elif sortbased == 'ltoh':
            queryset = queryset.order_by('price')
        else:
            queryset = queryset
        return queryset

#used mixin enable for the user to login first to view this view
#detail view passes 1 object
class ApparelDetailView(LoginRequiredMixin, DetailView):
    model = Apparel
    context_object_name = 'apparel_details'
    template_name = "apparelapp/apparel_detail.html"

    # add another data which is form base on the subtype
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        if item.sub_type.strip() in ['Jeans','Trousers','Shorts','Underwears']:
            context["cart_form"] = BotwearForm()
        elif item.sub_type.strip() in ['Shirts','Coats','Jackets']:
            context['cart_form'] = TopwearForm()
        elif item.sub_type.strip() in ['Shoes']:
            context['cart_form'] = FootwearForm()
        return context
    
    #pass the answer base on subtype
    def post(self, request, *args, **kwargs):
        #get object get the currect objet selected
        apparel = self.get_object()
      
        if apparel.sub_type.strip() in ['Jeans','Trousers','Shorts','Underwears']:
            form = BotwearForm(request.POST)
        elif apparel.sub_type.strip() in ['Shirts','Coats','Jackets']:
            form = TopwearForm(request.POST)
        elif apparel.sub_type.strip() in ['Shoes']:
            form = FootwearForm(request.POST)
        buyer = UserInfo.objects.get(user=self.request.user)
       
       #if valid, check if the purchase and size were same, if not add another object, else, update
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
            return redirect('apparelapp:cart')
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
        numofitem = len([x for x in total_eachitems])
        context["total"] = total
        context['numofitems'] = numofitem
        return context
    

class CartUpdateView(LoginRequiredMixin, UpdateView):
    model = CartItem
    template_name = "apparelapp/cart_update.html"
    context_object_name = 'items'

    success_url = reverse_lazy('apparelapp:cart')

#overwrite the form_class
    def get_form_class(self) -> type[BaseModelForm]:
        item = self.object
        if item.product_purchase.sub_type.strip() in ['Jeans','Trousers','Shorts','Underwears']:
            return BotUpdateForm
        elif item.product_purchase.sub_type.strip() in ['Shirts','Coats','Jackets']:
            return TopUpdateForm
        elif item.product_purchase.sub_type.strip() in ['Shoes']:
            return FootUpdateForm
        return super().get_form_class()
    
    #call the form_class then add a name as updateform fopr templating
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['updateform'] = self.get_form()
        return context   

    def form_valid(self, form):
        #get the object
        cartitem = self.get_object()

        # to check if the qrty is zero, if yes, delete
        if cartitem.quantity <= 0:
            # CartItem.objects.filter(product_purchase=cartitem.product_purchase).delete() #or use this
            cartitem.delete()
            return HttpResponseRedirect(self.success_url)
        #to update the totalvalue of the item by calling the4 function
        cartitem.update_total_amount()
        return super().form_valid(form)
    
#use for direct delete in model
class CartDeleteView(LoginRequiredMixin, DeleteView):
    model = CartItem
    template_name = "apparelapp/cart_delete.html"
    context_object_name = 'items'

    success_url = reverse_lazy('apparelapp:cart')

class OrderHistoryListView(ListView):
    model = OrderHistoryList
    template_name = "apparelapp/orderhistory.html"
    context_object_name = 'itemhistory'

    def get_queryset(self):
        return OrderHistoryList.objects.filter(owner__user=self.request.user)

class CheckOutView(ListView):
    model = CartItem
    template_name = 'apparelapp/checkout.html'
    context_object_name = 'itemcheckout'

    def get_queryset(self):
        return CartItem.objects.filter(owner__user=self.request.user)
    


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

    def checkuserexists(self, username) -> bool:
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
            #assign each key to variable
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

