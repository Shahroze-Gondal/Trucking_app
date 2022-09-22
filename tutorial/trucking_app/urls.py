from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.api_root),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    # path('login/', views.LoginAPIView.as_view(), name='auth_login'),
    path('dispatches/', views.DispatchList.as_view(), name='dispatch-list'),
    path('dispatches/<int:pk>/', views.DispatchDetail.as_view(), name='dispatch-detail'),
    path('orders/<int:pk>/', views.OrderList.as_view(), name='order-detail'),
]
urlpatterns = format_suffix_patterns(urlpatterns)