import factory
from factory.django import DjangoModelFactory
from pytest_factoryboy import register


@register
class UserFactory(DjangoModelFactory):

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda a: '{0}.{1}@example.com'.format(a.first_name, a.last_name).lower())
    username = factory.LazyAttribute(lambda a: '{0}.{1}example.com'.format(a.first_name, a.last_name).lower())
    is_active = True
    is_staff = True
    is_superuser = True

    class Meta:
        model = 'auth.User'

    @factory.post_generation
    def password(self, create, extracted):
        if not create:
            # Simple build, do nothing.
            return
        if extracted:
            self.set_password(extracted)
