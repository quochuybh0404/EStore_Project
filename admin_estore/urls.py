from django.urls import path
from admin_estore.views import *

app_name = 'admin_estore'
urlpatterns = [
    path('user-auth/', user_auth, name = 'user_auth'),
    path('user-logout/', logout_user_auth, name = 'logout_user_auth'),
]