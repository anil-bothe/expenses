from rest_framework import serializers
from app.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "name", "email", "mobile",
    
    def validate(self, data):
        self.validate_mobile(data.get("mobile"))
        return data 
    
    @classmethod
    def validate_mobile(cls, mobile):
        if not mobile or len(mobile) != 10 or not mobile.isdigit() or mobile[0] not in "987":
            raise serializers.ValidationError({"name": "This field is required."})
        return mobile


class SignUpSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    mobile = serializers.CharField(max_length=10)
    password = serializers.CharField(max_length=50)

    def cleaned_mobile(self, mobile):
        UserSerializer.validate_mobile(mobile)
        return mobile