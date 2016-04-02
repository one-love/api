from flask_restplus.fields import String, Nested
from .. import api
from .application import fields as application_fields
from .user import response_fields as user_fields


fields = api.model(
    'Service',
    {
        'name': String(required=True),
    },
)

get_fields = api.clone(
    'Get Services',
    fields,
    {
        'id': String(),
        'applications': Nested(application_fields),
        'user': Nested(user_fields),
    },
)
