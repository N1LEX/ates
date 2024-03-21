from enum import Enum
from uuid import uuid4

import attrs

from task_tracker import validators


@attrs.define(kw_only=True)
class UserV1:
    public_id: str = attrs.field(validator=validators.UUIDValidator, converter=str)
    username: str = attrs.field(validator=attrs.validators.instance_of(str))
    full_name: str = attrs.field(validator=attrs.validators.instance_of(str))
    role: str = attrs.field(validator=attrs.validators.instance_of(str))
    email: str = attrs.field(validator=attrs.validators.instance_of(str))


@attrs.define(kw_only=True)
class TaskV1:
    public_id: str = attrs.field(default=uuid4(), converter=str)
    user_id: str = attrs.field(validator=validators.UUIDValidator, converter=str)
    description: str = attrs.field(validator=attrs.validators.instance_of(str))
    status: str = attrs.field(validator=attrs.validators.instance_of(str))
    date: str = attrs.field(validator=validators.DatetimeValidator, converter=str)


class SerializerNames(Enum):
    USER = 'User'
    TASK = 'Task'


SERIALIZERS = {
    '1': {
        SerializerNames.USER: UserV1,
        SerializerNames.TASK: TaskV1,
    }
}


def get_serializer(model_name: str, event_version: str):
    return SERIALIZERS[event_version][model_name]
