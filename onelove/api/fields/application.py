from flask_restplus.fields import String
from .. import api


fields = api.model(
    'Application', {
        'galaxy_role': String(required=True),
        'name': String(required=True),
    }
)
