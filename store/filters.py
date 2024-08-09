from django_filters.rest_framework import FilterSet
from .models import Product, Category, UserProfle


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'category': ['exact'],
            'price': ['gt', 'lt'],
            'date': ['gt', 'lt'],
            'active': ['exact'],
        }




