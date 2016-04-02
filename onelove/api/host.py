from flask_restplus import abort
from .mixins import ClusterMixin
from resources import ProtectedResource
from ..models import HostSSH
from .fields.host import fields
from .namespaces import ns_cluster


parser = ns_cluster.parser()
parser.add_argument('hostname', type=str, required=True, location='json')
parser.add_argument('ip', type=str, required=True, location='json')


@ns_cluster.route(
    '/<cluster_id>/providers/<provider_name>/hosts',
    endpoint='cluster.provider.hosts',
)
class ClusterProviderHostListAPI(ProtectedResource, ClusterMixin):
    @ns_cluster.marshal_with(fields)
    def get(self, cluster_id, provider_name):
        cluster = self._find_cluster(cluster_id)
        provider = None
        for prov in cluster.providers:
            if prov.name == provider_name:
                provider = prov
                break
        if not provider:
            abort(404, 'No such provider')
        return provider.hosts

    @ns_cluster.expect(fields)
    @ns_cluster.marshal_with(fields)
    def post(self, cluster_id, provider_name):
        args = parser.parse_args()
        hostname = args.get('hostname')
        ip = args.get('ip')
        host = HostSSH(hostname=hostname, ip=ip)
        cluster = self._find_cluster(cluster_id)
        for provider in cluster.providers:
            if provider.name == provider_name:
                provider.hosts.append(host)
                provider.save()
                cluster.save()
                return host
        abort(404, 'No such provider')


@ns_cluster.route(
    '/<cluster_id>/providers/<provider_name>/hosts/<hostname>',
    endpoint='cluster.provider.host',
)
class ClusterProviderHostAPI(ProtectedResource, ClusterMixin):
    @ns_cluster.marshal_with(fields)
    def get(self, cluster_id, provider_name, hostname):
        cluster = self._find_cluster(cluster_id)
        for provider in cluster.providers:
            if provider.name == provider_name:
                for host in provider.hosts:
                    if host.hostname == hostname:
                        return host
                abort(404, 'No such host')
        abort(404, 'No such provider')

    @ns_cluster.expect(fields)
    @ns_cluster.marshal_with(fields)
    def put(self, cluster_id, provider_name, hostname):
        args = parser.parse_args()
        cluster = self._find_cluster(cluster_id)
        for provider in cluster.providers:
            if provider.name == provider_name:
                for host in provider.hosts:
                    if host.hostname == hostname:
                        host.hostname = args.get('hostname')
                        host.ip = args.get('ip')
                        provider.save()
                        cluster.save()
                        return host
                abort(404, 'No such host')
        abort(404, 'No such provider')

    @ns_cluster.marshal_with(fields)
    def delete(self, cluster_id, provider_name, hostname):
        cluster = self._find_cluster(cluster_id)
        for provider in cluster.providers:
            if provider.name == provider_name:
                for host in provider.hosts:
                    if host.hostname == hostname:
                        provider.hosts.remove(host)
                        provider.save()
                        cluster.save()
                        return host
                abort(404, 'No such host')
        abort(404, 'No such provider')
