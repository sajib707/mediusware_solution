from django.urls import path
from product.views.product import ProductListView, EditProductView, CreateProductView, UpdateProductView, product_detail
from product.views.variant import VariantView, VariantCreateView, VariantEditView

app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create/', VariantCreateView.as_view(), name='create_variant'),
    path('variant/<int:id>/edit/', VariantEditView.as_view(), name='update_variant'),

    # Products URLs
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('product/<int:product_id>/edit/', EditProductView.as_view(), name='edit_product'),
    path('create/', CreateProductView.as_view(), name='create_product'),
    path('update/<int:pk>/', UpdateProductView.as_view(), name='update_product'),
    path('list/', ProductListView.as_view(), name='product_list'),
]