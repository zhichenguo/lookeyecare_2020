from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

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
    product = Product.objects.get(id=id)
    context = {
        "product": product
    }
    return render(request, 'product_detail.html', context)


def product_create(request):
    form = ProductForm(request.POST or None)
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


def product_update(request, id):
    product = Product.objects.get(id=id)
    # instance put the old info into the form
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        # return redirect('/products/' + str(id) + '/')
        return redirect('..')  # back the parent level, same as above
    context = {"form": form}
    return render(request, 'product_update.html', context)


def product_delete(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    # return redirect('/products/')  # same below
    return redirect('optical:product_list')
