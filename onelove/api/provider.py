from flask.ext.restplus import abort
from resources import ProtectedResource
from .fields.provider import fields, patch_fields
from .mixins import ClusterMixin
from .namespaces import ns_cluster
from ..utils import check_fields, all_fields_optional


parser = ns_cluster.parser()
parser.add_argument('name', type=str, required=True, location='json')


@ns_cluster.route('/<cluster_id>/providers', endpoint='clusters.providers')
class ClusterProviderListAPI(ProtectedResource, ClusterMixin):
    @ns_cluster.marshal_with(fields)
    def get(self, cluster_id):
        """List cluster providers"""
        cluster = self._find_cluster(cluster_id)
        return cluster.providers

    @ns_cluster.expect(fields)
    @ns_cluster.marshal_with(fields)
    @ns_cluster.response(409, 'Provider with that name already exists')
    @ns_cluster.response(400, 'No such provider class')
    def post(self, cluster_id):
        """Create cluster provider"""
        parser.add_argument('type', type=str, required=True, location='json')
        args = parser.parse_args()
        check_fields(args)
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
@ns_cluster.response(404, 'No such provider')
class ClusterProviderAPI(ProtectedResource, ClusterMixin):
    @ns_cluster.marshal_with(fields)
    def get(self, cluster_id, provider_name):
        """List cluster provider details"""
        cluster = self._find_cluster(cluster_id)
        for provider in cluster.providers:
            if provider.name == provider_name:
                return provider
        abort(404, 'No such provider')
    @ns_cluster.expect(patch_fields)
    @ns_cluster.marshal_with(fields)
    def patch(self, cluster_id, provider_name)
        ""Update cluster provider""
        args = parser.parse_args()
        check_fields(args)
        cluster = self._find_cluster(cluster_id)
        for provider in cluster.providers:
            if provider.name == provider_name;
            provider.name = args.get('name')
            provider.save()
            return provider
        abort(404, error='No such provider')
    @ns_cluster.expect(patch_fields)
    @ns_cluster.marshal_with(fields)
    def patch(self, cluster_id, provider_name):
        """Update cluster provider"""
        patch_parser = all_fields_optional(parser)
        args = patch_parser.parse_args()
        cluster = self._find_cluster(cluster_id)
        for provider in cluster.providers:
            if provider.name == provider_name:
                provider.name = args.get('name') or provider.name
                provider.save()
                return provider
        abort(404, error='No such provider')

    @ns_cluster.marshal_with(fields)
    def delete(self, cluster_id, provider_name):
        """Delete cluster provider"""
        cluster = self._find_cluster(cluster_id)
        for provider in cluster.providers:
            if provider.name == provider_name:
                cluster.providers.remove(provider)
                cluster.save()
                return provider
        abort(404, 'No such provider')
