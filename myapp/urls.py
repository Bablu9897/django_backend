from django.urls import path
from .views import (SignupView, LoginView, UserListView, UserDetailAPI, DataAPI)

urlpatterns = [
    path('api/auth/signup/', SignupView.as_view()), # POST /api/auth/signup/
    path('api/auth/login/', LoginView.as_view()), # POST /api/auth/signup/
    path('api/users/', UserListView.as_view(), name='user-list'),             # GET /api/users only for admin
    path('api/users/<int:id>', UserDetailAPI.as_view(), name='user-detail'), # GET,PUT,DELETE /api/users/<id>
    path('api/data', DataAPI.as_view()), # POST /api/data
    path('api/data/<int:id>', DataAPI.as_view()), # GET,PUT,DELETE /api/data/<id>
    
]
