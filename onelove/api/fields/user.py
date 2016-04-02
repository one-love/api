from flask_restplus.fields import String, Nested
from .. import api
from .role import fields as role_fields


fields = api.model(
    'User', {
        'email': String(
            description='The email',
            required=True,
            default='admin@example.com'
        ),
        'username': String(
            description='Username',
            required=True,
            default='admin'
        ),
        'first_name': String(),
        'last_name': String(),
    }
)


body_fields = api.clone(
    'User password',
    fields,
    {
        'password': String(
            description='Password',
            required=True,
            default='Sekrit',
        )
    },
)

response_fields = api.clone(
    'Get User',
    fields,
    {
        'id': String(),
        'roles': Nested(role_fields),
    }
)
