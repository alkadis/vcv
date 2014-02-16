'''
Implements configuration options for mapping shibboleth attributes to user
data, e.g. badges and display names. Configuration values have to be given in
JSON.

For examples, see docs/development/use_cases/shibboleth_authentication.rst.

'''

import random
from string import ascii_uppercase

from adhocracy.model import meta
from adhocracy.model.user import User


def _attribute_equals(request, key, value):
    """
    exact match
    """
    return request.headers.get(key) == value


def _attribute_contains(request, key, value):
    """
    contains element
    """
    elements = (e.strip() for e in request.headers.get(key).split(';'))
    return value in elements


def _attribute_contains_substring(request, key, value):
    """
    contains substring
    """
    return value in request.headers.get(key)


USERBADGE_MAPPERS = {
    'attribute_equals': _attribute_equals,
    'attribute_contains': _attribute_contains,
    'attribute_contains_substring': _attribute_contains_substring,
}


def _full_name(request, name_attr, surname_attr):
    return u"%s %s" % (request.headers.get(name_attr),
                       request.headers.get(surname_attr))


def _full_name_random_suffix(request, name_attr, surname_attr):

    letter = lambda: random.choice(ascii_uppercase)

    base = _full_name(request, name_attr, surname_attr)

    display_name = None
    while display_name is None:

        suffix = letter() + letter()
        try_display_name = '%s %s' % (base, suffix)

        if (meta.Session.query(User)
                .filter(User.display_name == try_display_name).first()  # noqa
                is None):
            display_name = try_display_name

    return display_name


DISPLAY_NAME_FUNCTIONS = {
    "full_name": _full_name,
    "full_name_random_suffix": _full_name_random_suffix,
}
