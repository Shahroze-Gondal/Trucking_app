import factory
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory
from pytest_factoryboy import register

faker = FakerFactory.create()


@register
class DispatchFactory(DjangoModelFactory):
    created = factory.Sequence(lambda x: 'created{}'.format(x))
    title = factory.Sequence(lambda x: 'title{}'.format(x))
    status = factory.Sequence(lambda x: 'Scheduled'.format(x))
    action = factory.Sequence(lambda x: 'Pickup'.format(x))
    dispatch_id = factory.Sequence(lambda x: x)


    class Meta:
        model = 'trucking_app.Dispatch'
