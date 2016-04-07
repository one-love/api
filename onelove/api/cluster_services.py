from flask_restplus import abort
from .fields.service import get_fields
from .fields.cluster_service import post_fields
from .fields.task import fields as task_fields
from onelove.api.mixins import ClusterMixin
from onelove.api.namespaces import ns_cluster
from onelove.models import Service, User
from onelove.api.resources import ProtectedResource


parser = ns_cluster.parser()
parser.add_argument('service_id', type=str, required=True, location='json')


@ns_cluster.route(
    '/<cluster_id>/services',
    endpoint='clusters.cluster.services',
)
class ClusterServiceListAPI(ProtectedResource, ClusterMixin):
    @ns_cluster.marshal_with(get_fields)
    def get(self, cluster_id):
        cluster = self._find_cluster(cluster_id)
        return cluster.services

    @ns_cluster.doc(body=post_fields)
    @ns_cluster.marshal_with(get_fields)
    def post(self, cluster_id):
        args = parser.parse_args()
        cluster = self._find_cluster(cluster_id)
        service_id = args.get('service_id')
        for service in cluster.services:
            if str(service.id) == service_id:
                abort(
                    409,
                    'Service %s is already part of cluster %s' % (
                        service_id,
                        cluster.name,
                    )
                )

        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            abort(404, 'No such service')

        cluster.services.append(service)
        cluster.save()
        return service


@ns_cluster.route(
    '/<cluster_id>/services/<service_id>',
    endpoint='clusters.cluster.service',
)
class ClusterServiceAPI(ProtectedResource, ClusterMixin):
    @ns_cluster.marshal_with(get_fields)
    def delete(self, cluster_id, service_id):
        cluster = self._find_cluster(cluster_id)
        for service in cluster.services:
            if str(service.id) == service_id:
                cluster.services.remove(service)
                cluster.save()
                return service
        abort(404, 'Service %s not found' % service_id)
        return service
