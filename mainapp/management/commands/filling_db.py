
import json
from django.core.management.base import BaseCommand

from mainapp.models import ProductCategory, Product
from users.models import User, AbstractUser

def load_from_json(file_name):
    with open(file_name, mode='r', encoding='utf-8') as f:
        return json.load(f)


class Command(BaseCommand):
    def handle(self, *args, **options):

        categories = load_from_json('mainapp/fixtures/categories_dump.json')
        ProductCategory.objects.all().delete()
        for category in categories:
            cat = category.get('fields')
            cat['id'] = category.get('pk')
            new_category = ProductCategory(**cat)
            new_category.save()

        products = load_from_json('mainapp/fixtures/product_dump.json')
        Product.objects.all().delete()
        for product in products:
            prod = product.get('fields')
            category = prod.get('category')
            _category = ProductCategory.objects.get(id=category)
            prod['category'] =_category
            new_category = Product(**prod)
            new_category.save()

super_user = User.objects.create_superuser(username='sten451', email='', password='1')