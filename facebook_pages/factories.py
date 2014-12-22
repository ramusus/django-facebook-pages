from models import Page
import factory
import random

class PageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Page

    graph_id = factory.Sequence(lambda n: n)