from flask_restplus.fields import String
from .. import api

patch_fields = api.model(
     'Patch provider',
      {
          'name': String(required=True),
      },
)
fields = api.clone(
    'Provider',
    patch_fields,
    {
        'type': String(required=True),
    },
)
