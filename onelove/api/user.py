from flask_security.utils import encrypt_password
from flask_restplus import Resource, abort
from mongoengine.queryset import NotUniqueError
from mongoengine.errors import ValidationError
from .namespaces import ns_user
from .fields.user import body_fields, response_fields


from ..models import User
from resources import ProtectedResource
import uuid
from ..email import send_email


parser = ns_user.parser()
parser.add_argument('email', type=str, required=True, location='json')
parser.add_argument('first_name', type=str, required=False, location='json')
parser.add_argument('last_name', type=str, required=False, location='json')
parser.add_argument('password', type=str, required=False, location='json')


@ns_user.route('', endpoint='users')
class UserListAPI(ProtectedResource):
    @ns_user.marshal_with(response_fields)
    def get(self):
        """List users"""
        return [user for user in User.objects.all()]


@ns_user.route('/<id>', endpoint='user')
class UserAPI(ProtectedResource):
    @ns_user.marshal_with(response_fields)
    def get(self, id):
        """Show user details"""
        try:
            user = User.objects.get(id=id)
        except (User.DoesNotExist, ValidationError):
            abort(404, message='User does not exist')
        return user

    @ns_user.expect(body_fields)
    @ns_user.marshal_with(response_fields)
    def put(self, id):
        """Update user"""
        try:
            user = User.objects.get(id=id)
        except (User.DoesNotExist, ValidationError):
            abort(404, message='User does not exist')

        args = parser.parse_args()
        user.email = args.get('email')
        user.save()
        return user

    @ns_user.marshal_with(response_fields)
    def delete(self, id):
        """Delete user."""
        try:
            user = User.objects.get(id=id)
        except (User.DoesNotExist, ValidationError):
            abort(404, message='User does not exist')
        user.delete()
        return user


@ns_user.route('/confirm/<uuid>', endpoint='user.confirm')
class UserConfirmAPI(Resource):
    @ns_user.marshal_with(response_fields)
    def get(self, uuid):
        """Update user"""
        try:
            user = User.objects.get(register_uuid=uuid)
        except (User.DoesNotExist, ValidationError):
            abort(404, message='User does not exist')

        user.active = True
        user.register_uuid = None
        user.save()
        return user


@ns_user.route('/register', endpoint='user.register')
class UserRegisterAPI(Resource):
    @ns_user.doc(
        model=response_fields,
        body=body_fields,
        responses={
            409: 'User with that email exists',
            422: 'Validation error'
        }
    )
    @ns_user.marshal_with(response_fields)
    def post(self):
        """Create user"""
        args = parser.parse_args()
        try:
            user = User(
                email=args.get('email'),
                first_name=args.get('first_name'),
                last_name=args.get('last_name'),
                password=encrypt_password(args.get('password')),
            )
            user.active = False
            user.register_uuid = uuid.uuid4()
            user.save()
            print(user.register_uuid)
        except NotUniqueError:
            abort(409, message='User with that email exists')
        except (ValidationError):
            abort(422, message='ValidationError')
        send_email(user.email, 'Registration', 'mail/confirm', user=user)
        return user, 201
