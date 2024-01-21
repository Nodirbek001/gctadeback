from django.db.models import Count
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.product.filters import ManufacturerFilter, ProductFilter
from apps.product.models import Banner, Manufacturer, Product, ParentCategory, ProductView, LastSeenProduct, \
    SavedProduct, Cart, CartItem, Order, SearchHistory
from apps.product.serializer import BannerSerializer, ManufacturerSerializer, ProductSerializer, \
    ParentCategorySerializer, LastSeenProductSerializer, SavedProductSerializer, SavedProductCreateSerializer, \
    CartSerializer, CartItemCreateSerializer, CartItemListSerializer, OrderSerializer, SearchHistorySerializer


# Create your views here.
class BannerListView(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

    def get_queryset(self):
        return Banner.objects.filter(is_active=True).order_by('order')


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filterset_class = ProductFilter
    ordering_fields = ('price', "views_count", "created_at", "-price", "-view_count", "-created_at")
    search_fields = ('title', "manufacturer__title", "category__title", "product_code")

    def get_queryset(self):
        return Product(
            Product.objects.filter(is_active=True)
            .order_by("-created_at")
            .select_related("manufacturer", "category")
            .prefetch_related("gallery")
        )


class ManufacturerListView(generics.ListAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ManufacturerFilter


class ParentCategoryListView(generics.ListAPIView):
    queryset = ParentCategory.objects.all()
    serializer_class = ParentCategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("id", "categories__id", "slug", "categories__slug")


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"

    def get_filtered_queryset(self):
        fingerprint = self.request.Meta.get("HTTP_fingerprint", None)
        if fingerprint:
            ProductView.objects.get_or_create(product=self.get_object(), fingerprint=fingerprint)
            LastSeenProduct.objects.get_or_create(product=self.get_object(), fingerprint=fingerprint)
        return ProductView.objects.filter(is_active=True)

    def get(self, request, *args, **kwargs):
        self.queryset = self.get_filtered_queryset()
        return super().get(request, *args, **kwargs)


class LastSeenProductListView(generics.ListAPIView):
    queryset = LastSeenProduct.objects.all()
    serializer_class = LastSeenProductSerializer

    def get_queryset(self):
        fingerprint = self.request.Meta.get("HTTP_fingerprint", None)
        if fingerprint:
            return LastSeenProduct.objects.filter(fingerprint=fingerprint).order_by("-created_at")
        return LastSeenProduct.objects.none()


class SavedProductListView(generics.ListAPIView):
    queryset = SavedProduct.objects.all()
    serializer_class = SavedProductSerializer

    def get_queryset(self):
        fingerprint = self.request.Meta.get("HTTP_fingerprint", None)
        if fingerprint:
            return SavedProduct.objects.filter(fingerprint=fingerprint).order_by("-created_at")
        return SavedProduct.objects.none()


class SavedProductCreateView(generics.CreateAPIView):
    queryset = SavedProduct.objects.all()
    serializer_class = SavedProductCreateSerializer


class SavedProductDeleteView(generics.UpdateAPIView):
    queryset = SavedProduct.objects.all()
    serializer_class = SavedProductCreateSerializer
    lookup_field = 'product_id'

    def delete(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        fingerprint = self.request.Meta.get("HTTP_fingerprint", None)
        if fingerprint:
            saved_product = SavedProduct.objects.filter(fingerprint=fingerprint, product_id=product_id).first()
            if saved_product:
                saved_product.delete()
                return Response({"status": "deleted"})
            return Response({"status": "not found"})
        return Response({"status": "please provide fingerprint"})


class CartCreateView(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartListView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        fingerprint = self.request.Meta.get("HTTP_fingerprint", None)
        if fingerprint:
            return Cart.objects.filter(fingerprint=fingerprint).order_by("-created_at")
        return Cart.objects.none()


class CartItemCreateView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemCreateSerializer


class CartItemUpdateView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemCreateSerializer


class CartItemDeleteView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemCreateSerializer


class CartItemListView(generics.ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemListSerializer
    lookup_field = "cart_id"

    def get_queryset(self):
        cart_id = self.kwargs.get("cart_id")
        return CartItem.objects.filter(cart_id=cart_id).order_by("-created_at")


class CartTotalPriceView(APIView):
    def get(self, request, *args, **kwargs):
        fingerprint = self.request.Meta.get("HTTP_fingerprint", None)
        cart_id = self.kwargs.get("cart_id")
        if fingerprint:
            cart = Cart.objects.get(pk=cart_id)
            if cart:
                total_quantity = cart.items.count()
                total_price = cart.total_price

                total_savings = 0
                for cart_item in cart.items.all():
                    product = cart_item.product
                    if product.sale_price is not None:
                        savings_par_item = (product.price - product) * cart_item.quantity
                        total_savings += savings_par_item
                return Response({
                    "quantity": total_quantity,
                    "total_price": total_price,
                    "total_savings": total_savings,
                })
        return Response({"total_price": 0, "total_savings": 0, 'quantity': 0})


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class SearchHistoryCreateView(generics.CreateAPIView):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer


class SearchHistoryListView(generics.ListAPIView):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer

    def get_queryset(self):
        fingerprint = self.request.Meta.get("HTTP_fingerprint", None)
        if fingerprint:
            return SearchHistory.objects.filter(fingerprint=fingerprint).order_by("-created_at")
        return SearchHistory.objects.none()


class SearchHistoryDeleteView(generics.DestroyAPIView):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer
    lookup_field = "ok"

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        fingerprint = self.request.Meta.get("HTTP_fingerprint", None)
        if fingerprint:
            search_history = SearchHistory.objects.filter(fingerprint=fingerprint).first()
            if search_history:
                search_history.delete()
                return Response({"status": "deleted"})
            return Response({"status": "not found"})
        return Response({"status": "please provide fingerprint"})


class PopularSearchHistoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            popular_searches = (
                SearchHistory.objects.values("query").annotate(count=Count("query")).order_by("-count")[:5]
            )
            popular_searches_list = list({"popular_searches": popular_searches})
            return Response({"popular_searches_list": popular_searches_list})
        except Exception as e:
            return Response({"error": str(e)})


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class PopularSearchHistoryListView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        try:
            popular_searches = (
                SearchHistory.objects.values("query").annotate(count=Count("query")).order_by("-count")[:5]
            )
            popular_searches_list = list(popular_searches.values("query", "count"))
            return Response({"popular_searches_list": popular_searches_list})
        except Exception as e:
            return Response({"error": str(e)})
