import json
import typing
from enum import Enum
from uuid import uuid4

import attrs
from django.conf import settings
from django.utils.timezone import now


class EventVersions(Enum):
    v1 = '1'


class Topics(Enum):
    TASK_LIFECYCLE = 'task-lifecycle'


@attrs.define(kw_only=True)
class Event:
    event_version: str = attrs.field()
    event_name: str = attrs.field()
    data: typing.Union[typing.List, typing.Dict] = attrs.field()
    event_id: str = attrs.field(default=uuid4(), converter=str)
    event_time: str = attrs.field(default=now(), converter=str)
    producer: str = attrs.field(default='task-tracker')


class EventStreaming:

    def __init__(self, version: str = EventVersions.v1):
        self.version = version

    def task_updated(self, task):
        event = Event(
            event_name=f'Task{task.status.capitalize()}',
            event_version=self.version,
            data=attrs.asdict(task),
        )
        settings.PRODUCER.produce(
            topic=Topics.TASK_LIFECYCLE,
            key=task.status,
            value=json.dumps(event).encode('utf-8'),
        )

    def get_event(self, name: str, data: dict):
        return Event(event_name=name, event_version=self.version, data=data)


EVENT_STREAMING_VERSIONS = {
    '1': EventStreaming(version='1')
}


def get_event_streaming(event_version: str) -> EventStreaming:
    return EVENT_STREAMING_VERSIONS[event_version]
