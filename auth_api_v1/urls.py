from django.urls import path
from .views import FullProfileView, ListUsers, SignupView, LoginView, TestView, RequestPasswordReset, UserProfileView, UserProfileUpdate, RetriveUserProfile
from auth_api_v1 import views

urlpatterns = [

    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('test/', TestView.as_view(), name='test'),
    path('reset-password/', RequestPasswordReset.as_view(), name='password_reset'),
    path('reset-password/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('user/profile/view/', UserProfileView.as_view(), name='user-profile-view'),
    path('user/profile/update/', UserProfileUpdate.as_view(), name='user-profile-update'),
    path('user/full-profile/<account_id>/', FullProfileView.as_view(), name='full-profile'),
    path('user/details/<account_id>/', RetriveUserProfile.as_view(), name='full-profile'),
    path('user/list/', ListUsers.as_view(), name='user-list'),

]