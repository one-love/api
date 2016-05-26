from flask_restplus.fields import String
from .. import api


fields = api.model(
    'Provider',

    {
        'name': String(required=True),
        'type': String(required=True),
    },
)
