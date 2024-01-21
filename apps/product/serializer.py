from rest_framework import serializers

from apps.common.serializer import ImageSerializer
from apps.product.choices import CartStatusChoices, OrderStatusChoices
from apps.product.models import Manufacturer, Category, ParentCategory, Product, Cart, Order, LastSeenProduct, \
    SavedProduct, Banner, CartItem, SearchHistory


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ("id", "title", "logo")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title", "slug", "parent")


class ParentCategorySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = ParentCategory
        fields = ("id", "title", "slug", "icon", "categories")


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    manufacturer = ManufacturerSerializer(read_only=True)
    gallery = ImageSerializer(many=True, source="get_gallery")
    is_in_saved = serializers.SerializerMethodField()
    is_in_cart = serializers.SerializerMethodField()
    sold_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "manufacturer",
            "category",
            "title",
            "slug",
            "description",
            "features",
            "price",
            "sale_price",
            "in_stock_count",
            "is_recommended",
            "is_active",
            "is_sale",
            "gallery",
            "is_in_saved",
            "is_in_cart",
            "sold_count",
            "product_code"
        )

    def get_is_in_saved(self, obj):
        request = self.context.get("request")
        if request:
            fingerprint = request.headers.get("Fingerprint")
            if fingerprint:
                return obj.saved.filter(fingerprint=fingerprint).exists()
        return False

    def get_is_in_cart(self, obj):
        request = self.context.get("request")
        if request:
            fingerprint = request.headers.get("Fingerprint")
            if fingerprint:
                return obj.cart_item.filter(cart__fingerprint=fingerprint,
                                            cart__status=CartStatusChoices.ACTIVE).exists()
        return False

    def get_sold_count(self, obj):
        cart = Cart.objects.filter(items__product=obj)
        order = Order.objects.filter(cart__in=cart, status=OrderStatusChoices.SOLD)
        return order.count()


class LastSeenProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = LastSeenProduct
        fields = ("id", "product")


class SavedProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = SavedProduct
        fields = ("id", "product", "fingerprint")


class SavedProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedProduct
        fields = ("id", "product", "fingerprint")


class BannerSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Banner
        fields = ("id", "title", "sub_title", "image", "is_active", "url", "product", "order")


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ("id", "fingerprint")


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("id", "cart", "product", "quantity")


class CartItemListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ("id", "cart", "product", "quantity")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "cart", "name", "phone")

    def validate(self, data):
        if not data["cart"].items.all():
            raise serializers.ValidationError("Cart should not be empty")
        return data


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ("id", "query", "fingerprint")
