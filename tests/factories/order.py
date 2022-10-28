import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register
from .dispatch import DispatchFactory

faker = FakerFactory.create()


@register
class OrderFactory(DjangoModelFactory):
    order_id = factory.Sequence(lambda x: x)
    title = factory.Sequence(lambda x: 'order{}'.format(x))
    company = factory.Sequence(lambda x: 'company{}'.format(x))
    dispatch_id = factory.SubFactory(DispatchFactory)

    class Meta:
        model = 'trucking_app.Order'
