from rest_framework import serializers
from .models import Sector, Grave, Deceased


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = "__all__"


class GraveSerializer(serializers.ModelSerializer):
    sector_name = serializers.ReadOnlyField(source="sector.name")

    class Meta:
        model = Grave
        fields = "__all__"


class DeceasedSerializer(serializers.ModelSerializer):
    grave_code = serializers.ReadOnlyField(source="grave.code")

    class Meta:
        model = Deceased
        fields = "__all__"
