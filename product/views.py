from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.db.models import Q
from django.forms import modelformset_factory
from braces.views import SuperuserRequiredMixin
from .forms import ProductForm, ColorsGalleryForm, ImagesForm
from .models import Product, CATEGORY_CHOICES, ColorsGallery, Images, Color, Contact


# only filter for Sun Glasses
class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    # template_name = 'product/products_list.html'

    paginate_by = 6

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_list = self.get_queryset().filter(category='S')

    def get(self, request, *args, **kwargs):
        # categories = [row[1] for row in CATEGORY_CHOICES]
        search_text = request.GET.get('search_text')
        # category = request.GET.get('category')
        women = request.GET.get('women')
        men = request.GET.get('men')
        kid = request.GET.get('kid')
        # sun = request.GET.get('sun')
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
            objs_women = self.object_list.filter(gender='W').union(self.object_list.filter(gender='U'))
        else:
            objs_women = Product.objects.none()
        if men == 'on':
            objs_men = self.object_list.filter(gender='M').union(self.object_list.filter(gender='U'))
        else:
            objs_men = Product.objects.none()
        if kid == 'on':
            objs_kid = self.object_list.filter(gender='K')
        else:
            objs_kid = Product.objects.none()
        # if sun == 'on':
        #     objs_sun = self.object_list.filter(category='S')
        # else:
        #     objs_sun = Product.objects.none()
        if onsale == 'on':
            objs_onsale = self.object_list.filter(label='S')
        else:
            objs_onsale = Product.objects.none()

        if (search_text == '' or search_text is None) and (
                women is None and men is None and kid is None and onsale is None):
            # self.object_list = self.get_queryset()
            self.object_list = self.object_list.filter(category='S')
        else:
            self.object_list = Product.objects.none().union(
                objs_search, objs_women, objs_men, objs_kid, objs_onsale
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
    template_name = 'product/product_create.html'
    # model = Product
    # form_class = ProductForm
    success_url = '/product/'

    def get(self, *args, **kwargs):
        colors = get_list_or_404(Color)
        product_form = ProductForm()
        color_gallery_form = ColorsGalleryForm()
        image_forset = modelformset_factory(Images, form=ImagesForm, extra=3)
        context = {
            'colors': colors,
            'product_form': product_form,
            'color_gallery_form': color_gallery_form,
            'image_forset': image_forset,

        }
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):

        product_form = ProductForm(self.request.POST or None)
        color_gallery_form = ColorsGalleryForm(self.request.POST or None)
        image_forset = modelformset_factory(Images, form=ImagesForm, extra=3)
        images_formset = image_forset(self.request.POST or None, self.request.FILES, queryset=Images.objects.none())

        print(self.request.POST)

        if product_form.is_valid() and color_gallery_form.is_valid() and images_formset.is_valid():
            product = product_form.save(commit=False)
            product.save()
            color_gallery = color_gallery_form.save(commit=False)
            color_gallery.save()

            for form in images_formset.cleaned_data:
                image = form['image']
                photo = Images(color_gallery=color_gallery, image=image)
                photo.save()
            messages.success(self.request, "Posted!")
            return redirect('product:product_list')
        else:
            print(product_form.errors, color_gallery_form.errors, images_formset.errors)

            # else:
            #     postForm = PostForm()
            #     formset = ImageFormSet(queryset=Images.objects.none())

            # context = {
            #     'product_form': product_form,
            #     'color_gallery': color_gallery,
            #     'formset': formset,
            # }
            return redirect('product:product_create')

        # return render(self.request, 'index.html',
        #               {'postForm': postForm, 'formset': formset},
        #               context_instance=RequestContext(request))

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


class ContactListView(ListView):
    model = Contact
    context_object_name = 'contacts'
    template_name = 'product/contacts_list.html'

    paginate_by = 6

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_list = self.get_queryset().filter(category='C')

    def get(self, request, *args, **kwargs):
        # categories = [row[1] for row in CATEGORY_CHOICES]
        search_text = request.GET.get('search_text')
        # category = request.GET.get('category')
        women = request.GET.get('women')
        men = request.GET.get('men')
        kid = request.GET.get('kid')
        # sun = request.GET.get('sun')
        onsale = request.GET.get('onSale')
        # self.object_list = None

        if search_text != '' and search_text is not None:
            objs_search = self.object_list.filter(
                Q(name__icontains=search_text) | Q(description__icontains=search_text)).distinct()
        else:
            objs_search = Contact.objects.none()

        # if category != '' and category is not None and category != 'Choose...':
        #     self.object_list = self.object_list.filter(category=category)

        if women == 'on':
            objs_women = self.object_list.filter(gender='W').union(self.object_list.filter(gender='U'))
        else:
            objs_women = Contact.objects.none()
        if men == 'on':
            objs_men = self.object_list.filter(gender='M').union(self.object_list.filter(gender='U'))
        else:
            objs_men = Contact.objects.none()
        if kid == 'on':
            objs_kid = self.object_list.filter(gender='K')
        else:
            objs_kid = Contact.objects.none()
        # if sun == 'on':
        #     objs_sun = self.object_list.filter(category='S')
        # else:
        #     objs_sun = Contact.objects.none()
        if onsale == 'on':
            objs_onsale = self.object_list.filter(label='S')
        else:
            objs_onsale = Contact.objects.none()

        if (search_text == '' or search_text is None) and (
            women is None and men is None and kid is None and onsale is None):
            # self.object_list = self.get_queryset()
            self.object_list = self.object_list.filter(category='C')
        else:
            self.object_list = Contact.objects.none().union(
                objs_search, objs_women, objs_men, objs_kid, objs_onsale
            )

        context = self.get_context_data()

        # return self.render_to_response(context)  # work with template_name
        return render(request, self.template_name, context)

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
        # objs = Contact.objects.all()
        # only show the instock product with Manager Objects
        objs = Contact.objects.instock()
        return objs
        # return objs.filter(category=self.kwargs['category'])
