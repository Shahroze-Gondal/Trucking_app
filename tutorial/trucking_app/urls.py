from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.api_root),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    path('dispatches/', views.DispatchList.as_view(), name='dispatch-list'),
    path('dispatches/<int:pk>/', views.DispatchDetail.as_view(), name='dispatch-detail'),
    path('orders/<int:pk>/', views.OrderList.as_view(), name='order-detail'),
]
urlpatterns = format_suffix_patterns(urlpatterns)