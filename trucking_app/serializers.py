from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from trucking_app.models import Dispatch, Order
from rest_framework import serializers
from django.contrib.auth.models import User


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class DispatchSerializer(serializers.HyperlinkedModelSerializer):
    # owner = serializers.ReadOnlyField(source='User.username')
    orders = serializers.HyperlinkedIdentityField(view_name='order-detail')
    url = serializers.HyperlinkedIdentityField(view_name='dispatch-detail')

    class Meta:
        model = Dispatch
        fields = ['url', 'dispatch_id', 'title', 'status', 'orders',
                  'tractor', 'pickup_location', 'action', 'commodity',
                  'delivery_location', 'pickup_arrival_date', 'pickup_departure_date',
                  'pickup_arrival', 'departure_from_pickup', 'delivery_arrival_date',
                  'delivery_departure_date', 'delivery_arrival', 'delivery_departure', 'pod'
                  ]

    def create(self, validated_data):
        return Dispatch.objects.create(**validated_data)


# class UserSerializer(serializers.ModelSerializer):
#     dispatches = serializers.PrimaryKeyRelatedField(many=True, queryset=Dispatch.objects.all())
#
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'dispatches']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=68, min_length=6)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def validate_password(self, value):
        if value:
            return make_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create(**validated_data)


# class LoginSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(max_length=68, min_length=6, write_only=True)
#     username = serializers.CharField(max_length=255, min_length=3, read_only=True)
#
#     class Meta:
#         model = User
#         fields = ['password', 'username']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name',
                  'last_name', 'username', 'is_active')
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'write_only': True, 'validators': []}
        }

    def validate_password(self, value):
        if value:
            return make_password(value)
        return value


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token