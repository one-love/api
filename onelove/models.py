from flask_mongoengine import Document
from flask_security import UserMixin, RoleMixin
from mongoengine.fields import (
    BaseField,
    BooleanField,
    EmailField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    ListField,
    ReferenceField,
    StringField,
    UUIDField,
)


field_types = {
    'BooleanField': 'boolean',
    'DateTimeField': 'date_time',
    'EmailField': 'email',
    'ReferenceField': 'reference',
    'StringField': 'string',
    'UUIDField': 'uuid',
}


class Application(EmbeddedDocument):
    name = StringField(max_length=512)
    galaxy_role = StringField(max_length=1024)

    def __repr__(self):
        return '<Application %r>' % self.name

    # Required for administrative interface
    def __unicode__(self):
        return self.__repr__()


class Provider(EmbeddedDocument):
    name = StringField(max_length=512)
    type = 'BASE'
    meta = {'allow_inheritance': True}

    def list(self):
        return []

    def update(self, **kwargs):
        pass

    def create(self, **kwargs):
        pass

    def destroy(self, id):
        pass

    @classmethod
    def _check_field(cls, field):
        if isinstance(field, BaseField):
            if isinstance(field, EmbeddedDocument):
                return False
            if isinstance(field, EmbeddedDocumentField):
                return False
            if isinstance(field, EmbeddedDocumentListField):
                return False
            if isinstance(field, ListField):
                return False
            return True
        return False

    @classmethod
    def fields(cls):
        result = []
        for property in dir(cls):
            if property[0] != '_':
                property_type = getattr(cls, property)
                if cls._check_field(property_type):
                    type_name = type(property_type).__name__
                    result.append(
                        {
                            'name': property_type.name,
                            'type': field_types[type_name]
                        }
                    )
        return result

    def _setup(self):
        pass

    def __init__(self, *args, **kwargs):
        super(Provider, self).__init__(*args, **kwargs)
        self._setup()

    def __repr__(self):
        return '<Provider %r>' % self.name

    # Required for administrative interface
    def __unicode__(self):
        return self.__repr__()


class Role(Document, RoleMixin):
    """
    Role
    """
    name = StringField(max_length=255)
    admin = BooleanField()
    description = StringField(max_length=255)

    # Required for administrative interface
    def __unicode__(self):
        return self.name


class User(Document, UserMixin):
    """
    User
    """
    active = BooleanField(default=False)
    email = EmailField(unique=True)
    first_name = StringField(max_length=255)
    last_name = StringField(max_length=255)
    password = StringField(max_length=255)
    roles = ListField(ReferenceField(Role), default=[])
    register_uuid = UUIDField(binary=False)
    username = StringField(max_length=255, unique=True)

    def __repr__(self):
        return '<User %r>' % self.email


class Service(Document):
    user = ReferenceField(User)
    name = StringField(max_length=512, unique_with='user')
    applications = ListField(EmbeddedDocumentField(Application))

    def __repr__(self):
        return '<Service %s/%s>' % (self.user.username, self.name)


class Cluster(Document):
    name = StringField(max_length=512, blank=False)
    username = StringField(max_length=64)
    sshKey = StringField()
    applications = ListField(EmbeddedDocumentField(Application))
    providers = ListField(EmbeddedDocumentField(Provider))
    roles = ListField(ReferenceField(Role), default=[])
    services = ListField(ReferenceField(Service), default=[])

    def __repr__(self):
        return '<Cluster %r>' % self.name


class Provision(Document):
    status = StringField(max_length=63, default='PENDING')
    cluster = ReferenceField(Cluster)
    service = ReferenceField(Service)
    user = ReferenceField(User)

class Log(EmbeddedDocument):
    status = StringField(max_length=512)
    galaxy_role = StringField(max_length=1024)

    def __repr__(self):
        return '< Log >'
