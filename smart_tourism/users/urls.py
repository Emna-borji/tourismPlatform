from django.urls import path, include
from . import views  # Import the views you defined
from rest_framework.routers import DefaultRouter
from .views import UserViewSet



# Create a router and register our viewset with it
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),  # Update profile
    path('profile/change-password/', views.change_password, name='change_password'),  # Change password
    path('logout/', views.logout, name='logout'),
    path('users/', include(router.urls)),
    path("users/<int:pk>/block/", UserViewSet.as_view({"post": "block_user"})),
]
