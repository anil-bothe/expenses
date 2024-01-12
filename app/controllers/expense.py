import traceback
from app.models import Expense
from app.serializers.expense_serializer import ExpenseSerializer
from utility.response import ApiResponse
from utility.utils import MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, get_pagination_resp, get_serielizer_error, calculate_splits, update_balances
from utility.scheduler import EmailScheduler
from rest_framework.permissions import IsAuthenticated


class ExpenseView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    """
    Assuming logged-in users can create/edit/manage expenses
    """

    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated] 

    singular_name = "Expense"

    def get_object(self, pk):
        try:
            return Expense.objects.get(pk=pk)
        except:
            return None

    def retrieve(self, request, *args, **kwargs):
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

    def list(self, request, *args, **kwargs):
        try:
            # capture data
            sort_by = request.query_params.get("sort_by") if request.query_params.get("sort_by") else "id"
            sort_direction = request.query_params.get("sort_direction") if request.query_params.get("sort_direction") else "ascending"
            
            if sort_direction == "descending":
                sort_by = "-" + sort_by

            data = request.query_params
            search_keyword = data.get("keyword")
            queryset = Expense.objects.all().order_by(sort_by)

            if search_keyword:
                queryset = queryset.filter(payer__name__icontains=search_keyword)

            resp_data = get_pagination_resp(queryset, request)
            response_data = self.transform_list(resp_data.get("data"))

            return ApiResponse.response_ok(self, data=response_data, paginator=resp_data.get("paginator"))

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])

    def partial_update(self, request, *args, **kwargs):
        try:
            data = request.data
            get_id = self.kwargs.get("id")

            """ get instance """
            instance = self.get_object(get_id)

            if instance is None:
                return ApiResponse.response_not_found(self, message=self.singular_name + " not found")

            """ capture data """
            data = request.data

            """ validate serializer """
            serializer = ExpenseSerializer(instance, data=data, partial=True)
            if not serializer.is_valid():
                error_resp = get_serielizer_error(serializer)
                return ApiResponse.response_bad_request(self, message=error_resp)
        
            serializer.save()
            """ success response """
            response_data = self.transform_single(serializer.instance)
            return ApiResponse.response_ok(self, data=response_data, message=self.singular_name + " updated")

        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])
        
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = ExpenseSerializer(data=data)

            if not serializer.is_valid():
                error_resp = get_serielizer_error(serializer)
                return ApiResponse.response_bad_request(self, message=error_resp)
            
            exact_amounts = {}
            if data.get("split_type") == 'PERCENT' or data.get("split_type") == 'EXACT':
                exact_amounts = data.get('shares')
        
            expense = Expense.objects.create(
                payer_id=data.get("payer"), amount=data.get("amount"), split_type=data.get("split_type"), shares=exact_amounts
            )
            expense.participants.set(data.get("participants"))

            splits = calculate_splits(expense)  # Calculate individual amounts
            update_balances(expense, splits)  # Update balances

            # email scheduler
            # scheduler = EmailScheduler(expense)
            # scheduler.start()

            response_data = self.transform_single(expense)
            return ApiResponse.response_created(self, data=response_data, message=self.singular_name + " created successfully.")

        except Exception as e:
            traceback.print_exception(e)
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])]) 


    def delete(self, request, *args, **kwargs):
        try:
            get_id = self.kwargs.get('id')

            ''' get instance '''
            instance = self.get_object(get_id)
            if instance is None:
                return ApiResponse.response_not_found(self, message=self.singular_name + ' not found')

            instance.delete()

            ''' return success '''
            return ApiResponse.response_ok(self, message=self.singular_name + ' deleted')
        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])

    
    def transform_single(self, instance: Expense):
        resp_dict = dict()
        resp_dict["id"] = instance.id
        resp_dict["created_at"] = instance.created_at
        resp_dict["updated_at"] = instance.updated_at
        resp_dict["amount"] = instance.amount
        resp_dict["payer"] = instance.payer.pk if instance.payer else None
        resp_dict["participants"] = [i.pk for i in instance.participants.all()]
        resp_dict["split_type"] = instance.split_type
        resp_dict["shares"] = instance.shares
        return resp_dict

    def transform_list(self, data):
        return map(self.transform_single, data)
