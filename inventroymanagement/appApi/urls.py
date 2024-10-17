from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    #MyTokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    

    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   
    path('user/login/', views.userLogin, name='postUserLogin'),# For Api token and login

    path('getAllItem/', views.getAllItem, name='getAllItem'), 
    path('getItem/<str:id>/', views.getItem, name='getItem'), 
    path('createItem/', views.createItem, name='createItem'),
    path('updateItem/<str:id>/', views.updateItem, name='updateItem'),
    path('deleteItem/<str:id>/', views.deleteItem, name='deleteItem'), 

]