import django_filters

from .models import Product

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    keyword = django_filters.filters.CharFilter(field_name="name",lookup_expr="icontains")
    minPrice = django_filters.filters.NumberFilter(field_name="newprice" or 0,lookup_expr="gte")
    maxPrice = django_filters.filters.NumberFilter(field_name="newprice" or 100,lookup_expr="lte")
    category = django_filters.CharFilter(field_name="category",  lookup_expr="exact")
    subcategory = django_filters.CharFilter(field_name="subcategory",  lookup_expr="exact")

    class Meta:
        model = Product
        fields = ( 'keyword', 'minPrice', 'maxPrice', 'category', 'subcategory')