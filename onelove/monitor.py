import zmq.green as zmq


def monitor():
    from . import current_app
    from .models import Provision,Log

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:5500')
    while True:
        task_json = socket.recv_json()
        socket.send_json({'status': 'ok'})
        provision = Provision.objects.get(pk=task_json['id'])
        data = {}
        message_type = task_json['type']
        if task_json['type'] == 'provision':
            data = {
                'id': task_json['id'],
                'status': provision.status,
                'log': provision.applications,
            }
        elif task_json['type'] == 'log':
            data = {
                'id': task_json['id'],
                'status': task_json['status'],
                'host': task_json['host'],
                'task': task_json['task'],
                'timestamp': task_json['timestamp'],
            }
            if task_json['log'] is not None:
                data['log'] = task_json['log']
        else:
            continue
        current_app.socketio.emit(
            message_type,
            data,
            namespace='/onelove',
            room=str(provision.user.pk),
        )
    socket.close()
    context.tern()
