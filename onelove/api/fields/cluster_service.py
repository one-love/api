from flask_restplus.fields import String, Nested
from .. import api


post_fields = api.model(
    'Post Service',
    {
        'service': String(),
        'username': String(),
    },
)
