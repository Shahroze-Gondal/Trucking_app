from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse
from trucking_app.models import Dispatch, Order
from trucking_app.serializers import DispatchSerializer, OrderSerializer
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import generics


class ActivateAccount(APIView):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('login')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('account/account_activation_email.html', {
                'pass': form.cleaned_data['password1'],
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            print(form.cleaned_data['password1'])
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            print(form.cleaned_data.get('email'))
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

            return redirect('login')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="account/register.html", context={"register_form":form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return reverse('dispatch-list', request=request, format=format)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="account/login.html", context={"login_form": form})


class DispatchList(generics.ListCreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    queryset = Dispatch.objects.all()
    serializer_class = DispatchSerializer


class DispatchDetail(APIView):
    """
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
        parser_classes = (MultiPartParser, FormParser)
        if serializer.is_valid():
            if 'pod' in request.data:
                if dispatch.status != "Scheduled" and dispatch.status == "In Transit":
                    serializer.save()
                    dispatch.status = "Delivered"
                    serializer = DispatchSerializer(dispatch, data=request.data, partial=True, context=serializer_context)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                return Response(serializer.data, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            elif "status" in request.data and request.data['status'] == "Scheduled":
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.data, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dispatch = self.get_object(pk)
        dispatch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'snippets': reverse('dispatch-list', request=request, format=format)
    })


class OrderList(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
