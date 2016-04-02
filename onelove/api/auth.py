from flask_restplus import Resource
from flask import request
from flask_jwt import _jwt, JWTError
from .namespaces import ns_auth
from .fields.auth import fields, token_response
from ..models import User


parser = ns_auth.parser()
parser.add_argument('email', type=str, required=True, location='json')
parser.add_argument('password', type=str, required=False, location='json')


@ns_auth.route('/tokens', endpoint='auth.token')
class AuthAPI(Resource):
    @ns_auth.response(401, 'Invalid credentials')
    @ns_auth.doc(body=fields, security=None)
    @ns_auth.marshal_with(token_response, code=200, description='Get a token.')
    def post(self):
        """Authenticates and generates a token."""
        args = parser.parse_args()
        data = request.get_json(force=True)
        username = args.get('email')
        password = args.get('password')
        criterion = [username, password, len(data) == 2]

        if not all(criterion):
            raise JWTError('Bad Request', 'Invalid credentials')

        identity = _jwt.authentication_callback(username, password)
        if identity is not None:
            user = User.objects.get(id=identity.id)

        if identity and user and user.active:
            access_token = _jwt.jwt_encode_callback(identity)
            token = {
                "token": access_token
            }
            return token
        else:
            raise JWTError('Bad Request', 'Invalid credentials')
