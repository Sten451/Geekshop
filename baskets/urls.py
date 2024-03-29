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

from baskets.views import Basket_view

app_name = 'baskets'

urlpatterns = [

    path('add/<int:product_id>/', Basket_view.basket_add, name='basket_add'),
    path('edit/<int:id>/<int:quantity>/', Basket_view.basket_edit, name='basket_edit'),
    path('remove/<int:product_id>/', Basket_view.basket_remove, name='basket_remove'),
    path('clear/', Basket_view.basket_clear, name='basket_clear'),

]
