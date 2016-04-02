from flask_restplus.fields import String
from .. import api


fields = api.model(
    'Host',
    {
        'hostname': String(),
        'ip': String(),
    },
)
