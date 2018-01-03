import random
from django import template

register = template.Library()


@register.filter
def shuffle(arg):
    """Shuffles a collection of items, and returns the result.

    :param arg: ordered collection of items
    :return: shuffled collection
    """
    aux = list(arg)[:]
    random.shuffle(aux)
    return aux
