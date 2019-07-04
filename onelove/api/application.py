from flask_rest_api import abort

from ..models.service import Application, Service
from ..schemas.application import ApplicationSchema
from ..schemas.paging import PagingSchema
from .methodviews import ProtectedMethodView
from .service import blueprint


@blueprint.route('/<service_id>/applications', endpoint='applications')
class ApplicationListAPI(ProtectedMethodView):
    @blueprint.arguments(PagingSchema(), location='headers')
    @blueprint.response(ApplicationSchema(many=True))
    def get(self, pagination, service_id):
        """List applications"""
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            abort(404, error='No such service')
        return service.applications

    @blueprint.arguments(ApplicationSchema())
    @blueprint.response(ApplicationSchema())
    def post(self, args, service_id):
        """Create application"""
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            abort(404, error='No such service')
        application = Application(**args)
        service.applications.append(application)
        service.save()
        return application


@blueprint.route(
    '/<service_id>/application/<application_name>',
    endpoint='application'
)
class ApplicationAPI(ProtectedMethodView):
    @blueprint.response(ApplicationSchema())
    def get(self, service_id, application_name):
        """Get application details"""
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            abort(404, error='No such service')
        for app in service.applications:
            if app.name == application_name:
                return app
        abort(404, 'No such application')

    @blueprint.arguments(ApplicationSchema(partial=True))
    @blueprint.response(ApplicationSchema())
    def patch(self, args, service_id, application_name):
        """Edit application"""
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            abort(404, error='No such service')
        for app in service.applications:
            if app.name == application_name:
                for arg in args:
                    setattr(app, arg, args[arg])
                service.save()
                return app
        abort(404, 'No such application')

    @blueprint.response(ApplicationSchema())
    def delete(self, service_id, application_name):
        """Delete application"""
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            abort(404, error='No such service')
        for app in service.applications:
            if app.name == application_name:
                service.applications.remove(app)
                service.save()
                return app
        abort(404, 'No such application')
