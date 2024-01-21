from django.urls import path

from apps.product.views import BannerListView, ProductListView, ManufacturerListView, ParentCategoryListView, \
    ProductDetailView, LastSeenProductListView, SavedProductListView, SavedProductCreateView, SavedProductDeleteView, \
    CartCreateView, CartListView, CartItemCreateView, CartItemUpdateView, OrderCreateView, CartItemDeleteView, \
    CartItemListView, CartTotalPriceView, SearchHistoryListView, SearchHistoryCreateView, SearchHistoryDeleteView

app_name = 'product'

urlpatterns = [
    path('list/', ProductListView.as_view(), name='product-list'),
    path('banner/', BannerListView.as_view(), name='banner-list'),
    path('manufacturer/', ManufacturerListView.as_view(), name='manufacturer'),
    path('categories', ParentCategoryListView.as_view(), name='parent-category-list'),
    path("detail/<slug:slug>/", ProductDetailView.as_view(), name='product-detail'),
    path("last-seen-products/", LastSeenProductListView.as_view(), name='last-seen-products'),
    path("saved-products/", SavedProductListView.as_view(), name='saved-products'),
    path("saved-products/create/", SavedProductCreateView.as_view(), name='saved-products'),
    path("saved-products/delete/<int:product_id>/", SavedProductDeleteView.as_view()),
    path("searche/history/", SearchHistoryListView.as_view(), name='search-history'),
    path("searche-history/create/", SearchHistoryCreateView.as_view()),
    path("searche-history/delete/<int:pk>", SearchHistoryDeleteView.as_view(), name='search-history-delete'),
    path("popular-searche-history/", PopularSearcheHistoryAPIView.as_view(), name='popular'),

    # Cart & Order
    path("cart/create/", CartCreateView.as_view(), name='cart'),
    path("cart/list/", CartListView.as_view(), name='cart'),
    path("cart-item/create/", CartItemCreateView.as_view(), name="cart-item-create"),
    path("cart-item/update/<int:pk>/", CartItemUpdateView.as_view(), name="cart-item-update"),
    path("cart-item/delete/<int:pk>/", CartItemDeleteView.as_view()),
    path("cart-item/<int:cart_id>/", CartItemListView.as_view(), name='cart-item'),
    path("cart/total-price/", CartTotalPriceView.as_view(), name='cart-total-price'),
    path("order/create/", OrderCreateView.as_view(), name='order')
]
