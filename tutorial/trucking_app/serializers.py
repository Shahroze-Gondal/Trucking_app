from rest_framework import serializers
from trucking_app.models import Dispatch, Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['title', 'company', 'person', 'phone_no', 'dispatch_id'
                  ]


class DispatchSerializer(serializers.HyperlinkedModelSerializer):
    orders = serializers.HyperlinkedIdentityField(view_name='order-detail')
    url = serializers.HyperlinkedIdentityField(view_name='dispatch-detail')
    # pod = serializers.ImageField(required=False)

    class Meta:
        model = Dispatch
        # fields = '__all__'
        fields = ['url', 'dispatch_id', 'title', 'tractor', 'pickup_location', 'action', 'commodity',
                  'status', 'delivery_location', 'pickup_arrival_date', 'pickup_departure_date',
                  'pickup_arrival', 'departure_from_pickup', 'delivery_arrival_date',
                  'delivery_departure_date', 'delivery_arrival', 'delivery_departure', 'pod', 'orders'
                  ]

    def create(self, validated_data):
        return Dispatch.objects.create(**validated_data)


