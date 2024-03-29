"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import ProductsView, ProductDetail

app_name = 'products'
urlpatterns = [

    path('', ProductsView.as_view(), name='index'),
    #path('', cache_page(3600)(ProductsView.as_view()), name='index'),
    path('category/<int:category_id>/', ProductsView.as_view(), name='category'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='detail'),
    # path('detail/<int:pk>/', cache_page(3600)(ProductDetail.as_view()), name='detail'),

]
