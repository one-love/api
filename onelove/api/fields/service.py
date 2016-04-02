from flask_restplus.fields import String, Nested
from .. import api
from .application import fields as application_fields


fields = api.model(
    'Service',
    {
        'service': String(required=True),
    },
)

get_fields = api.clone(
    'Get Services',
    fields,
    {
        'id': String(),
        'applications': Nested(application_fields),
    },
)
