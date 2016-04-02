from flask_restplus.fields import String
from .. import api


fields = api.model(
    'Task',
    {
        'id': String(),
        'celery_id': String(),
    },
)
