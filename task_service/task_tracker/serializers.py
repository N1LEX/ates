from rest_framework import serializers

from task_tracker.models import Task


class TaskSerializer(serializers.ModelSerializer):
    user_public_id = serializers.CharField(source='user.public_id', read_only=True)

    class Meta:
        model = Task
        fields = ('public_id', 'user_public_id', 'description', 'status', 'date')
        read_only_fields = ('public_id', 'status')
