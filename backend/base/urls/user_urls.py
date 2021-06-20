from django.urls import path
from base.views import user_views as views

urlpatterns = [
    path('users/login/',views.MyTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('users/register/',views.registerUser,name="register"),
    path('users/profile/',views.getUserProfile,name='user-profile'),
    path('allusers/',views.getUsers,name='all-user-profile'),
    path('users/profile/update/',views.updateUserProfile,name='update-user-profile'),

# """only accessible by admin"""
    path('users/<str:pk>/',views.getUserById,name='user'),
    path('users/update/<str:pk>/',views.updateUser,name='user-deleted'),
    path('users/delete/<str:pk>/',views.deleteUser,name='user-deleted'),

]