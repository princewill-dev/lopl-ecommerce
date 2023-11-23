from django.urls import path
from .views import CreatePackView, ListProductView, RetrieveProductView, DeleteProductView

urlpatterns = [
    path('create-pack/', CreatePackView.as_view(), name='create_pack'),
    path('list/', ListProductView.as_view(), name='list_all_products'),
    path('detail/<str:product_id>/', RetrieveProductView.as_view(), name='retrieve_product'),
    path('delete/<str:product_id>/', DeleteProductView.as_view(), name='delete_product'),
]