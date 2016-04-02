from flask import current_app
from resources import ProtectedResource
from ..models import Task
from .namespaces import ns_task
from .fields.task import fields


@ns_task.route('', endpoint='tasks')
class TaskListAPI(ProtectedResource):
    @ns_task.marshal_with(fields)
    def get(self):
        return [task for task in Task.objects.all()]


@ns_task.route('/<id>', endpoint='task')
class TaskAPI(ProtectedResource):
    @ns_task.marshal_with(fields)
    def get(self, id):
        task = current_app.onelove.celery.AsyncResult(id=id)
        return task
