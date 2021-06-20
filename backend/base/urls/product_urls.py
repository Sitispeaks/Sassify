
from django.urls import path
from base.views import product_views as views
from base.views.product_views import ProductDocumentView

urlpatterns = [
    path('prod-search/',ProductDocumentView.as_view({'get':'list'})),
    path('products/',views.getProducts,name="products"),
    path('products/create/',views.createProduct,name="product-create"),
    path('products/upload/',views.uploadImage,name="image-upload"),
    path('products/top/',views.getTopProducts,name="top-products"),

    path('products/<str:pk>/reviews/',views.createProductReview,name="product-review"),
    path('products/<str:pk>/',views.getProduct,name="product"),
    path('products/update/<str:pk>/',views.updateProduct,name="product-update"),
    path('products/delete/<str:pk>/',views.deleteProduct,name="product-delete"),
]