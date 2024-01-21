import django_filters

from apps.product.models import Product, Manufacturer


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="get")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    manufacturer = django_filters.CharFilter(method="filter_manufacturer")
    category = django_filters.CharFilter(method="filter_category")
    is_recommended = django_filters.BooleanFilter(method="is_recommended")
    is_sale = django_filters.BooleanFilter(method="is_sale")
    is_active = django_filters.BooleanFilter(method="is_active")
    parent_category = django_filters.CharFilter(method="filter_parent_category")

    def filter_manufacturer(self, queryset, name, value):
        manufacturers = value.split(",")
        return queryset.filter(manufacturer__id__in=manufacturers)

    def filter_category(self, queryset, name, value):
        categories = value.split(",")
        return queryset.filter(category__id__in=categories)

    def filter_parent_category(self, queryset, name, value):
        parent_categories = value.split(",")
        return queryset.filter(parent__category__id__in=parent_categories)

    class Meta:
        model = Product
        fields: list[str] = []


class ManufacturerFilter(django_filters.FilterSet):
    parent_category = django_filters.CharFilter(method="filter_parent_category")
    child_category = django_filters.CharFilter(method="filter_child_category")

    def filter_parent_category(self, queryset, name, value):
        parent_categories = value.split(",")
        return queryset.filter(product__category__parent__id__in=parent_categories).distinct()

    def filter_child_category(self, queryset, name, value):
        child_categories = value.split(",")
        return queryset.filter(product__category__id__in=child_categories).distinct()

    class Meta:
        model = Manufacturer
        fields = ["parent_category", "child_category"]
