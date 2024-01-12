import traceback
from app.models import Balance, Expense
from app.serializers.balance_serializer import BalanceSerializer
from utility.response import ApiResponse
from utility.utils import MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, get_pagination_resp, get_serielizer_error, calculate_splits, update_balances
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum


class BalanceView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    """
    Assuming logged-in users can retrieve balances
    """
    serializer_class = BalanceSerializer
    permission_classes = [IsAuthenticated] 
    singular_name = "Balance"

    def retrieve_by_id(self, request, *args, **kwargs):
        try:
            # capture id
            get_id = self.kwargs.get("id")

            # process/format on data
            instance = self.get_object(get_id)
            if instance:
                resp_dict = self.transform_single(instance)

                # return success
                return ApiResponse.response_ok(self, data=resp_dict)

            return ApiResponse.response_not_found(self, message=self.singular_name + " not found")

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])
    
    def retrieve_by_user(self, request, *args, **kwargs):
        try:
            # user1 => balances_owed
            # user2 => balances_owed_to
            balances = Balance.objects.filter(user1=request.user)
            balances = balances.values("pk", "created_at",  "user2").annotate(amount=Sum("amount")).order_by("user2")
            data = self.transform_list(balances)
            return ApiResponse.response_ok(self, data=data)

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])
    
    def transform_single(self, instance: Balance):
        resp_dict = dict()
        resp_dict["id"] = instance["pk"]
        resp_dict["created_at"] = instance["created_at"]
        resp_dict["balances_owed_to"] = instance["user2"]
        resp_dict["amount"] = instance["amount"]
        return resp_dict

    def transform_list(self, data):
        return map(self.transform_single, data)
