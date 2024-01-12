from app.models import User
from app.serializers.user_serializer import UserSerializer
from utility.response import ApiResponse
from utility.utils import MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, get_pagination_resp, get_serielizer_error

# For admin Panel - USER CRUD; 

class UserView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    serializer_class = UserSerializer
    singular_name = "User"

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except:
            return None

    def retrieve(self, request, *args, **kwargs):
        try:
            # capture data
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
            queryset = User.objects.all().order_by(sort_by)

            if search_keyword:
                queryset = queryset.filter(name__icontains=search_keyword)

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
            serializer = UserSerializer(instance, data=data, partial=True)
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
            """capture data"""
            req_data = request.data
            data = req_data.copy()
            serializer = UserSerializer(data=data)

            """ validate serializer """
            if not serializer.is_valid():
                """serializer error"""
                error_resp = get_serielizer_error(serializer)
                return ApiResponse.response_bad_request(self, message=error_resp)
            
            serializer.save()
            response_data = self.transform_single(serializer.instance)
            return ApiResponse.response_created(self, data=response_data, message=self.singular_name + " created successfully.")

        except Exception as e:
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

        
    def transform_single(self, instance):
        resp_dict = dict()
        resp_dict["id"] = instance.id
        resp_dict["name"] = instance.name
        resp_dict["email"] = instance.email
        resp_dict["mobile"] = instance.mobile
        return resp_dict

    def transform_list(self, data):
        return map(self.transform_single, data)
