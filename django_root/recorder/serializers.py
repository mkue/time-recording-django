from rest_framework import serializers

from recorder.models import LabourCost


class LabourCostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = LabourCost
        depth = 1
