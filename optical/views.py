from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView

from .forms import ProductForm
from .models import Product


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


def product_detail(request, id):
    # same as ProductDetailView
    product = Product.objects.get(id=id)
    context = {
        "product": product
    }
    return render(request, 'product_detail.html', context)


class ProductCreateView(CreateView):
    template_name = 'product_create.html'
    model = Product
    fields = ['name', 'category', 'description', 'price', 'inventory', 'image']
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


class ProductUpdateView(UpdateView):
    template_name = 'product_update.html'
    model = Product
    fields = ['name', 'category', 'description', 'price', 'inventory', 'image']
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


def product_update(request, id):
    # same as ProductUpdateView
    product = Product.objects.get(id=id)
    # instance put the old info into the form
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        # return redirect('/products/' + str(id) + '/')
        return redirect('..')  # back the parent level, same as above
    context = {"form": form}
    return render(request, 'product_update.html', context)


class ProductDeleteView(DeleteView):
    template_name = 'product_confirm_delete.html'
    model = Product
    success_url = '/products/'


def product_delete(request, id):
    # same as ProductDeleteView
    product = Product.objects.get(id=id)
    product.delete()
    # return redirect('/products/')  # same below
    return redirect('optical:product_list')
