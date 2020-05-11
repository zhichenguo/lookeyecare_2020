from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.db.models import Q
from django.forms import modelformset_factory
from braces.views import SuperuserRequiredMixin
from .forms import ProductForm, ColorsGalleryForm, ImagesForm
from .models import Product, CATEGORY_CHOICES, ColorsGallery, Images


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    # template_name = 'product/products_list.html'

    paginate_by = 6

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_list = self.get_queryset()

    def get(self, request, *args, **kwargs):
        # categories = [row[1] for row in CATEGORY_CHOICES]
        search_text = request.GET.get('search_text')
        # category = request.GET.get('category')
        women = request.GET.get('women')
        men = request.GET.get('men')
        kid = request.GET.get('kid')
        sun = request.GET.get('sun')
        onsale = request.GET.get('onSale')
        # self.object_list = None

        if search_text != '' and search_text is not None:
            objs_search = self.object_list.filter(
                Q(name__icontains=search_text) | Q(description__icontains=search_text)).distinct()
        else:
            objs_search = Product.objects.none()

        # if category != '' and category is not None and category != 'Choose...':
        #     self.object_list = self.object_list.filter(category=category)

        if women == 'on':
            objs_women = self.object_list.filter(category='W')
        else:
            objs_women = Product.objects.none()
        if men == 'on':
            objs_men = self.object_list.filter(category='M')
        else:
            objs_men = Product.objects.none()
        if kid == 'on':
            objs_kid = self.object_list.filter(category='K')
        else:
            objs_kid = Product.objects.none()
        if sun == 'on':
            objs_sun = self.object_list.filter(category='S')
        else:
            objs_sun = Product.objects.none()
        if onsale == 'on':
            objs_onsale = self.object_list.filter(label='S')
        else:
            objs_onsale = Product.objects.none()

        # filter_list = [women, men, kid, sun, onsale]

        if (search_text == '' or search_text is None) and (
                women is None and men is None and kid is None and sun is None and onsale is None):
            self.object_list = self.get_queryset()
        else:
            self.object_list = Product.objects.none().union(
                objs_search, objs_women, objs_men, objs_kid, objs_sun, objs_onsale
            )

        context = self.get_context_data()

        # return self.render_to_response(context)  # work with template_name
        return render(request, 'product/products_list.html', context)

    # auto html file is 'app_name (product)' / 'model_name'(product) _list
    # the context passed in will be "object_list"
    def get_context_data(self, *, object_list=None, **kwargs):
        # for adding onther data pass to html
        context = super().get_context_data(**kwargs)
        # can add anything else in the context here
        # context['addition_var'] = addition_value
        context['categories'] = CATEGORY_CHOICES
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
    context_object_name = 'product'
    template_name = 'product/product_detail.html'

    def get(self, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs['slug'])
        if 'color_gallery' in kwargs:
            color_gallery = get_object_or_404(ColorsGallery, slug=kwargs['color_gallery'])
        else:
            color_gallery = get_list_or_404(ColorsGallery, product=product)[0]

        context = {
            'product': product,
            'color_gallery': color_gallery,
        }
        return render(self.request, self.template_name, context)


class ProductCreateView(SuperuserRequiredMixin, CreateView):
    permission_required = "auth."
    template_name = 'product/product_create.html'
    model = Product
    form_class = ProductForm
    success_url = '/product/'

    def form_valid(self, form):
        form.save()
        # do something like send email
        return super().form_valid(form)


class ProductUpdateView(SuperuserRequiredMixin, UpdateView):
    template_name = 'product/product_update.html'
    model = Product
    form_class = ProductForm
    success_url = '..'

    def form_valid(self, form):
        form.instance.event_agency = self.request.user.pk
        form.save()
        return super().form_valid(form)


class ProductDeleteView(SuperuserRequiredMixin, DeleteView):
    template_name = 'product/product_confirm_delete.html'
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
