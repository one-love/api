from flask_restplus.fields import Nested, String
from .. import api
from .provider import fields as provider_fields
from .role import fields as role_fields
from .service import fields as service_fields


fields = api.model(
    'Cluster', {
        'name': String(required=True),
    }
)

get_fields = api.clone('Get Clusters', fields, {
    'providers': Nested(provider_fields),
    'id': String,
    'roles': Nested(role_fields),
    'services': Nested(service_fields),
}
)
