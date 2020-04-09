from django.shortcuts import render, redirect

from .forms import ProductForm
from .models import Product


def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products_list.html', context)


# CRUD - Create, Retrieve, Update, Delete or List


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
    return redirect('/products/')
