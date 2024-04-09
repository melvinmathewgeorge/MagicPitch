from django.urls import path
from .views import register_user,user_details,user_referrals,login_view

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('user-details/', user_details, name='user_details'),
    path('referrals/', user_referrals, name='user_referrals'),
    path('login/', login_view, name='login'),
]