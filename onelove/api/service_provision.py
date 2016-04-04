from flask_restplus import abort
from resources import ProtectedResource

from .fields.task import fields
from .mixins import ClusterMixin
from .namespaces import ns_cluster


@ns_cluster.route(
    '/<cluster_id>/services/<username>/<service_name>/provision',
    endpoint='cluster.service.provision',
)
class ClusterServiceProvisionAPI(ProtectedResource, ClusterMixin):
    @ns_cluster.marshal_with(fields)
    def get(self, cluster_id, username, service_name):
        from ..tasks.provision import provision
        cluster = self._find_cluster(cluster_id)
        task = {
            'id': '123',
            'celery_id': '456',
        }
        for service in cluster.services:
            if (
                service.name == service_name and
                username == service.user.username
            ):
                task['celery_id'] = provision.delay(
                    cluster_id,
                    username,
                    service_name
                )
                return task
        abort(
            404,
            'Service %s with user %s not found' % (
                service_name,
                username,
            )
        )
