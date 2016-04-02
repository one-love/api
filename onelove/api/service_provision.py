from flask_restplus import abort
from resources import ProtectedResource

from .fields.application import fields
from .mixins import ServiceMixin
from .namespaces import ns_cluster


@ns_cluster.route(
    '/<cluster_id>/services/<username>/<service_name>/provision',
    endpoint='cluster.service.provision'
)
class ServiceApplicationProvisionAPI(ProtectedResource, ServiceMixin):
    @ns_cluster.marshal_with(fields)
    def get(self, cluster_id, username, service_name):
        from ..tasks import provision
        abort(404, 'No such application')
        provision.delay(cluster_id, username, service_name)
