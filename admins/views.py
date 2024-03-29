from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, AddCategory, AddProduct, EditSettings
from users.models import User
from mainapp.models import ProductCategory, Product
from admins.models import Custom_Settings
from geekshop.mixin import CustomDispatchMixin
from django.db import connection

def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


class AdminsSettins(CreateView, CustomDispatchMixin):
    model = Custom_Settings
    form_class = EditSettings
    template_name = 'admins/settings.html'
    success_url = reverse_lazy('admins:admins_settings')

    """def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            cs = Custom_Settings.objects.all()
            print('ok')

            Custom_Settings = form.save()
        else:print('bad')
        return redirect(self.success_url)"""



    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminsSettins, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Настройки сайта'
        return context


class Index(ListView):
    model = User
    template_name = 'admins/admin.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['count_user'] = User.objects.all().count()
        context['count_user_active'] = User.objects.all().filter(is_active=True).count()
        context['count_user_staff'] = User.objects.all().filter(is_staff=True)
        context['count_category'] = ProductCategory.objects.all().count()
        context['count_product'] = Product.objects.all().count()
        context['high_product'] = Product.objects.order_by("-price")[:1]
        context['end_product'] = Product.objects.all().filter(quantity=0)
        context['title'] = 'Админка'
        return context


class UserListView(ListView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-read.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Пользователи'
        return context


class UserCreateView(CreateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admins_user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Регистрация'
        return context


class UserUpdateView(UpdateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admins_user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Обновление пользователя'
        return context


class UserDeleteView(DeleteView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admins_user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Обновление пользователя'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

# Категории
class CategoryListView(ListView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-categories-read.html'
    context_object_name = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Категории товаров'
        return context


class CategoryUpdateView(UpdateView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-categories-update-delete.html'
    form_class = AddCategory
    success_url = reverse_lazy('admins:admins_category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Обновление категории товара'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                print(f'применяется скидка {discount} % к товарам категории {self.object.name}')
                self.object.product_set.update(price=F('price')*(1-discount/100))
                db_profile_by_type(self.__class__,'UPDATE',connection.queries)
        return HttpResponseRedirect(self.get_success_url())


class CategoryCreateView(CreateView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-categories-create.html'
    form_class = AddCategory
    success_url = reverse_lazy('admins:admins_category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Создание новой категории'
        return context


class CategoryDeleteView(DeleteView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-categories-update-delete.html'
    success_url = reverse_lazy('admins:admins_category')


# Продукты
class ProductListView(ListView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-products-read.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Товары'
        return context


class ProductUpdateView(UpdateView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-update-delete.html'
    form_class = AddProduct
    success_url = reverse_lazy('admins:admins_products')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Обновление карточки товара'
        return context

class ProductDeleteView(DeleteView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-update-delete.html'
    success_url = reverse_lazy('admins:admins_products')

class ProductCreateView(CreateView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-create.html'
    form_class = AddProduct
    success_url = reverse_lazy('admins:admins_products')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Создание нового продукта'
        return context