from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProductForm
from .models import Product


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products_list.html'

    paginate_by = 6

    # auto html file is 'app_name (product)' / 'model_name'(product) _list
    # the context passed in will be "object_list"
    def get_context_data(self, *, object_list=None, **kwargs):
        # for adding onther data pass to html
        context = super().get_context_data(**kwargs)
        # can add anything else in the context here
        # context['addition_var'] = addition_value
        return context

    def get_queryset(self):
        # do filtering
        # objs = Product.objects.all()
        # only show the instock product with Manager Objects
        objs = Product.objects.instock()
        return objs
        # return objs.filter(category=self.kwargs['category'])


# CRUD - Create, Retrieve, Update, Delete or List

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object()
        # perform logic, like 20% 0ff
        # obj.price *= 0.80
        return obj


class ProductCreateView(LoginRequiredMixin, CreateView):
    template_name = 'product_create.html'
    model = Product
    form_class = ProductForm
    success_url = '/product/'

    def form_valid(self, form):
        form.save()
        # do something like send email
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'product_update.html'
    model = Product
    form_class = ProductForm
    success_url = '..'

    def form_valid(self, form):
        form.instance.event_agency = self.request.user.pk
        form.save()
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'product_confirm_delete.html'
    model = Product
    success_url = '/product/'

# Register and Login Form are handled by django-allauth

# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from .forms import UserRegisterForm, UserLoginForm
# from django.contrib import messages


# def register_view(request):
#     form = UserRegisterForm(request.POST or None)
#     if request.method == "POST":
#         if form.is_valid():
#             user = form.save(commit=False)
#             password = form.cleaned_data.get('password')
#             # password = request.POST.get('password')  # above is more sucured
#             user.set_password(password)
#             user.save()
#             auth_user = authenticate(username=user.username, password=password)
#             login(request, auth_user)
#             messages.info(request, 'Successfully Registered')
#             return redirect('/products/')
#     context = {
#         'form': form
#     }
#     return render(request, 'register.html', context)


# def login_view(request):
#     # login required next url which is the 'back' url after login
#     next_back_url = request.GET.get('next')
#     form = UserLoginForm(request.POST or None)
#     if request.method == "POST":
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             # username = request.POST.get('username')
#             # password = request.POST.get('password')
#             auth_user = authenticate(username=username, password=password)
#             login(request, auth_user)
#             messages.info(request, 'Successfully Logged In')
#             if next_back_url:
#                 return redirect(next_back_url)
#             return redirect('/products/')
#     context = {
#         'form': form
#     }
#     return render(request, 'login.html', context)


# def logout_view(request):
#     logout(request)
#     messages.info(request, 'Successfully Logged Out')
#     return redirect('/products/')
