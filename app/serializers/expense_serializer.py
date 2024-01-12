from rest_framework import serializers
from app.models import Expense
from utility.constants import MAX_PARTICIPANTS_ALLOWED, MAX_EXPENSE_AMOUNT


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"
    
    def validate(self, data):
        if data.get("split_type") == 'EXACT' and not data.get("shares"):
            raise serializers.ValidationError({"split_type": "`EXACT` required dict `shares`"})
        
        elif data.get("participants") and len(data.get("participants")) > MAX_PARTICIPANTS_ALLOWED: 
            raise serializers.ValidationError({"participants": f"Each expense can have up to {MAX_PARTICIPANTS_ALLOWED} participants"})

        elif data.get("amount") and int(data.get("amount")) > MAX_EXPENSE_AMOUNT: 
            raise serializers.ValidationError({"participants": f"maximum amount for an expense can go up to INR {MAX_EXPENSE_AMOUNT}/-"})

        if data.get("split_type") != 'EXACT' and data.get("split_type") != "EQUAL":
            if data.get("shares") and len(data.get("shares")) != len(data.get("participants")):
                raise serializers.ValidationError({"shares": "Number of exact amounts must match the number of participants"})

            elif data.get("shares") and not isinstance(data.get("shares"), dict):
                raise serializers.ValidationError({"shares": "only accept `dict` type data"})            
        
        elif data.get("split_type") != "PERCENT" and data.get("split_type") != "EQUAL" and data.get("shares") and sum(data.get("shares").values()) != data.get("amount"):
            raise serializers.ValidationError({"shares": "Amount sum does not match"})
        
        elif data.get("split_type") == "PERCENT" and sum(data.get("shares").values()) != 100:
            raise serializers.ValidationError({"shares": "Please enter valid percentage"})

        return data 
    