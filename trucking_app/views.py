from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import auth

from trucking_app import exceptions
from django.contrib.auth import login, authenticate
from rest_framework.permissions import AllowAny

from trucking_app.models import Dispatch, Order
from trucking_app.serializers import DispatchSerializer, OrderSerializer, UserSerializer, RegisterSerializer, LoginSerializer
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from trucking_app.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import generics
from .utils import Util
# from django.views.decorators.csrf import csrf_exempt


class DispatchList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Dispatch.objects.all()
    serializer_class = DispatchSerializer
    #
    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class DispatchDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    """/home/shahroze
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Dispatch.objects.get(pk=pk)
        except Dispatch.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        serializer_context = {
            'request': request,
        }
        dispatch = self.get_object(pk)
        serializer = DispatchSerializer(dispatch, context=serializer_context)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        dispatch = self.get_object(pk)
        serializer_context = {
            'request': request,
        }
        serializer = DispatchSerializer(dispatch, data=request.data, partial=True, context=serializer_context)
        if serializer.is_valid():
            if 'pod' in request.data:
                if dispatch.status == "In Transit":
                    serializer.save()
                    dispatch.status = "Delivered"
                    serializer = DispatchSerializer(dispatch, data=request.data, partial=True,
                                                    context=serializer_context)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                return Response(serializer.data, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            elif "status" in request.data and request.data['status'] == "In Transit":
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.data, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk, format=None):
        dispatch = self.get_object(pk)
        dispatch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'snippets': reverse('dispatch-list', request=request, format=format)
    })


class OrderList(generics.ListCreateAPIView):
    permission_classes = [AllowAny, ]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetail(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SignUp(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, **kwargs):
        user = User.objects.filter(username=request.data['email'].lower()).first()
        if user and user.is_active:
            raise exceptions.UseralreadyExists('email')

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class Signin(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, **kwargs):
        # user = auth.authenticate(username=request.data['username'], password=request.data['password'])
        # if not user:
        #     raise exceptions.InvalidUser()
        refresh = RefreshToken.for_user(request.user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

# class RegisterView(generics.GenericAPIView):
#     serializer_class = RegisterSerializer
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         user_data = serializer.data
#         user = User.objects.get(email=user_data['email'])
#         password = User.objects.make_random_password()
#         user.set_password(password)
#         user.save()
#         email_body = "hi " + user.username + " your credetials are: Username: " + user.username + ' & password: ' + password
#         data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Credentials for Tailwind app'}
#         Util.send_email(data)
#         return Response(user_data, status=status.HTTP_201_CREATED)


# class LoginAPIView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = authenticate(username=request.data['username'], password=request.data['password'])
#         if not user:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         return Response(RegisterSerializer(user).data, status=status.HTTP_200_OK)
