from django.utils import timezone
from rest_framework import serializers

from .models import OrganRequest


class OrganRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganRequest
        fields = ('id', 'requesting_hospital', 'organ_type', 'priority', 'required_by', 'status', 'matched_organ', 'accepted_by', 'created_at', 'updated_at')
        read_only_fields = ('status', 'matched_organ', 'accepted_by', 'created_at', 'updated_at')

    def validate_required_by(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError('required_by must be in the future.')
        return value


class MatchSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    hospital_id = serializers.IntegerField(source='hospital.id')
    hospital_name = serializers.CharField(source='hospital.name')
