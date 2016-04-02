from flask.ext.restplus import abort
from .mixins import ClusterMixin
from resources import ProtectedResource
from .fields.provider import fields
from .namespaces import ns_cluster


parser = ns_cluster.parser()
parser.add_argument('name', type=str, required=True, location='json')
parser.add_argument('type', type=str, required=True, location='json')


@ns_cluster.route('/<cluster_id>/providers', endpoint='clusters.providers')
class ClusterProviderListAPI(ProtectedResource, ClusterMixin):
    @ns_cluster.marshal_with(fields)
    def get(self, cluster_id):
        cluster = self._find_cluster(cluster_id)
        return cluster.providers

    @ns_cluster.expect(fields)
    @ns_cluster.marshal_with(fields)
    def post(self, cluster_id):
        args = parser.parse_args()
        cluster = self._find_cluster(cluster_id)
        provider_name = args.get('name')
        provider_type = args.get('type')
        for provider in cluster.providers:
            if provider.name == provider_name:
                abort(409, error='Provider with that name already exists')
        Provider = self._get_provider_class(provider_type)
        if not Provider:
            abort(400, error='No such provider class')
        prov = Provider(name=provider_name)
        cluster = self._find_cluster(cluster_id)
        cluster.providers.append(prov)
        cluster.save()
        return prov


@ns_cluster.route(
    '/<cluster_id>/providers/<provider_name>',
    endpoint='clusters.provider',
)
class ClusterProviderAPI(ProtectedResource, ClusterMixin):
    @ns_cluster.marshal_with(fields)
    def get(self, cluster_id, provider_name):
        cluster = self._find_cluster(cluster_id)
        for provider in cluster.providers:
            if provider.name == provider_name:
                return provider
        abort(404, 'No such provider')

    @ns_cluster.expect(fields)
    @ns_cluster.marshal_with(fields)
    def put(self, cluster_id, provider_name):
        args = parser.parse_args()
        cluster = self._find_cluster(cluster_id)
        for provider in cluster.providers:
            if provider.name == provider_name:
                provider.name = args.get('name')
                provider.type = args.get('type')
                provider.save()
                return provider
        abort(404, error='No such provider')

    @ns_cluster.marshal_with(fields)
    def delete(self, cluster_id, provider_name):
        cluster = self._find_cluster(cluster_id)
        for provider in cluster.providers:
            if provider.name == provider_name:
                cluster.providers.remove(provider)
                cluster.save()
                return provider
        abort(404, 'No such provider')
