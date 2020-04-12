from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProductForm, UserRegisterForm, UserLoginForm
from .models import Product


def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            # password = request.POST.get('password')  # above is more sucured
            user.set_password(password)
            user.save()
            auth_user = authenticate(username=user.username, password=password)
            login(request, auth_user)
            messages.info(request, 'Successfully Registered')
            return redirect('/products/')
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


def login_view(request):
    # login required next url which is the 'back' url after login
    next_back_url = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # username = request.POST.get('username')
            # password = request.POST.get('password')
            auth_user = authenticate(username=username, password=password)
            login(request, auth_user)
            messages.info(request, 'Successfully Logged In')
            if next_back_url:
                return redirect(next_back_url)
            return redirect('/products/')
    context = {
        'form': form
    }
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    messages.info(request, 'Successfully Logged Out')
    return redirect('/products/')


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products_list.html'

    # auto html file is 'app_name (which is optical)' / 'model_name'(product) _list
    # the context passed in will be "object_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        # for adding onther data pass to html
        context = super().get_context_data(**kwargs)
        context['addition_var'] = 123123
        return context

    def get_queryset(self):
        # do filtering
        objs = Product.objects.all()
        return objs


def product_list(request):
    # same as ProductListView
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products_list.html', context)


# CRUD - Create, Retrieve, Update, Delete or List

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object()
        # perform logic
        # obj.price += 2
        return obj


def product_detail(request, product_id):
    # same as ProductDetailView
    product = Product.objects.get(id=product_id)
    context = {
        "product": product
    }
    return render(request, 'product_detail.html', context)


class ProductCreateView(LoginRequiredMixin, CreateView):
    template_name = 'product_create.html'
    model = Product
    form_class = ProductForm
    # fields = ['name', 'category', 'description', 'price', 'inventory', 'image']
    success_url = '/products/'

    def form_valid(self, form):
        form.save()
        # do something like send email
        return super().form_valid(form)


# class ProductCreateView(FormView):
#     # same as above ProductCreateView with CreateForm
#     template_name = 'product_create.html'
#     form_class = ProductForm
#     success_url = '/products/'
#
#     def form_valid(self, form):
#         form.save()
#         # do something like send email
#         return super().form_valid(form)


@login_required
def product_create(request):
    # same as ProductCreateView
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        # print(form.cleaned_data)
        # new_product = Product.objects.create(
        #     name=form.cleaned_data['name'],
        #     category=form.cleaned_data['category'],
        #     description=form.cleaned_data['description'],
        #     price=form.cleaned_data['price'],
        #     inventory=form.cleaned_data['inventory']
        # ) # same as below
        form.save()
        return redirect('/products/')
    context = {"form": form}
    return render(request, 'product_create.html', context)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'product_update.html'
    model = Product
    form_class = ProductForm
    # fields = ['name', 'category', 'description', 'price', 'inventory', 'image']
    success_url = '..'

    def form_valid(self, form):
        form.instance.event_agency = self.request.user.pk
        form.save()
        return super().form_valid(form)


# class ProductUpdateView(FormView):
#     # same as above ProductUpdateView with UpdateForm
#     template_name = 'product_update.html'
#     form_class = ProductForm
#     success_url = '..'
#
#     def get_form_kwargs(self):
#         form_kwargs = super(ProductUpdateView, self).get_form_kwargs()
#         if 'pk' in self.kwargs:
#             form_kwargs['instance'] = Product.objects.get(pk=int(self.kwargs['pk']))
#         return form_kwargs
#
#     def form_valid(self, form):
#         # form.instance = self.get_object
#         form.save()
#         return super().form_valid(form)


@login_required
def product_update(request, product_id):
    # same as ProductUpdateView
    product = Product.objects.get(id=product_id)
    # instance put the old info into the form
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        # return redirect('/products/' + str(id) + '/')
        return redirect('..')  # back the parent level, same as above
    context = {"form": form}
    return render(request, 'product_update.html', context)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'product_confirm_delete.html'
    model = Product
    success_url = '/products/'


@login_required
def product_delete(request, product_id):
    # same as ProductDeleteView
    product = Product.objects.get(id=product_id)
    product.delete()
    # return redirect('/products/')  # same below
    return redirect('optical:product_list')
