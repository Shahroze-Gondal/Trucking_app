from django.urls import path
from .views import UserList, UserDetail, Signin, SignUp, DispatchList, DispatchDetail, OrderList, \
    OrderDetail, api_root
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('',  api_root),
    path('users/',  UserList.as_view()),
    path('users/<int:pk>/',  UserDetail.as_view()),
    path('signup/',  SignUp.as_view(), name='signup'),
    path('signin/',  Signin.as_view(), name='signin'),
    # path('register/',  RegisterView.as_view(), name='auth_register'),
    # path('login/',  LoginAPIView.as_view(), name='auth_login'),
    path('dispatches/',  DispatchList.as_view(), name='dispatch-list'),
    path('dispatches/<int:pk>/',  DispatchDetail.as_view(), name='dispatch-detail'),
    path('orders/',  OrderList.as_view(), name='order-list'),
    path('orders/<int:pk>/',  OrderDetail.as_view(), name='order-detail'),
]
urlpatterns = format_suffix_patterns(urlpatterns)