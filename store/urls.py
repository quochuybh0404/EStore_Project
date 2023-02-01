from django.urls import path
from store.views import *

app_name = 'store'
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', index, name = 'index'),
    path('subcategory/<int:pk>/', subcategory, name = 'subcategory'),
    path('contact/', contact, name = 'contact'),
    path('thiet-bi-gia-dinh/', thiet_bi_gia_dinh, name = 'thiet_bi_gia_dinh'),
    path('do-dung-nha-bep/', dung_cu_nha_bep, name = 'dung_cu_nha_bep'),
    path('product-detail/<int:pk>/', product_detail, name = 'product_detail'),
    path('search/', search, name = 'search'),
]