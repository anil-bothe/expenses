from rest_framework import serializers
from app.models import Roles

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = "__all__"
    
    def validate(self, data):
        if not data.get("name"):
            raise serializers.ValidationError({"name": "This field is required."})
        return data 