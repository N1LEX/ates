from uuid import uuid4

import attrs
from django.db.models import TextChoices

from task_app import validators


@attrs.define(kw_only=True)
class UserV1:
    public_id: str = attrs.field(validator=validators.uuid_validator, converter=str)
    username: str = attrs.field(validator=attrs.validators.instance_of(str))
    full_name: str = attrs.field(default=None)
    role: str = attrs.field(validator=attrs.validators.instance_of(str))
    email: str = attrs.field(validator=attrs.validators.instance_of(str))


@attrs.define(kw_only=True)
class TaskV1:
    public_id: str = attrs.field(converter=str, default=attrs.Factory(uuid4))
    user_id: str = attrs.field(converter=str)
    description: str = attrs.field()
    status: str = attrs.field()
    date: str = attrs.field(converter=str)


class SerializerNames(TextChoices):
    USER = 'User'
    TASK = 'Task'


SERIALIZERS = {
    'v1': {
        SerializerNames.USER: UserV1,
        SerializerNames.TASK: TaskV1,
    }
}


def get_serializer(model_name: str, event_version: str):
    return SERIALIZERS[event_version][model_name]