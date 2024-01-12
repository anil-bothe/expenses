from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
import datetime
from django.utils.timezone import make_aware
from django.conf import settings
from decimal import Decimal
from app.models import Balance, User
import decimal
import json 


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super().default(o)


""" mixins to handle request url """
class CreateRetrieveUpdateViewSet(GenericViewSet,
                                  mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.CreateModelMixin,
                                  mixins.UpdateModelMixin):
    pass


class MultipleFieldPKModelMixin(object):
    """
    Class to override the default behaviour for .get_object for models which have retrieval on fields
    other  than primary keys.
    """
    lookup_field = []
    lookup_url_kwarg = []

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        get_args = {field: self.kwargs[field] for field in
                    self.lookup_field if field in self.kwargs}

        get_args.update({'pk': self.kwargs[field] for field in
                         self.lookup_url_kwarg if field in self.kwargs})
        return get_object_or_404(queryset, **get_args)


""" handle serializer error """
def get_serielizer_error(serializer):
    msg_list = []
    try:
        mydict = serializer.errors
        for key in sorted(mydict.keys()):
            msg = key + " : " + str(mydict.get(key)[0])
            msg_list.append(msg)
    except:
        msg_list = ["Invalid format"]
    return msg_list


""" pagination response """
def get_pagination_resp(data, request):
    page_response = {"total_count": None, "total_pages": None,
                     "current_page": None, "limit": None}
    if request.query_params.get('type') == 'all':
        # response_data = {"data": data}
        return {"data": data, "paginator": page_response}
    page = request.query_params.get('page') if request.query_params.get('page') else 1
    limit = request.query_params.get('limit') if request.query_params.get('limit') else settings.PAGE_SIZE
    paginator = Paginator(data, limit)
    category_data = paginator.get_page(page).object_list
    page_response = {"total_count": paginator.count, "total_pages": paginator.num_pages,
                     "current_page": page, "limit": limit}
    current_page = paginator.num_pages
    paginator = {"paginator": page_response}
    if int(current_page) < int(page):
        return {"data": [], "paginator": paginator.get('paginator')}
        # return {"data": [], **paginator}
    response_data = {"data": category_data, "paginator": paginator.get('paginator')}
    return response_data


""" string to date """
def string_to_date(string_time):
    try:
        naive_datetime = datetime.datetime.strptime(string_time, "%Y-%m-%d")
        aware_datetime = make_aware(naive_datetime)
        return aware_datetime.date()
    except:
        return None
    
    
""" timestamp to date """
def convert_timestamp_to_date(timestamp):
    try:
        naive_datetime = datetime.datetime.fromtimestamp(timestamp)
        aware_datetime = make_aware(naive_datetime)
        return aware_datetime.date()
    except:
        return None


def calculate_splits(expense):
    amount = Decimal(expense.amount)
    participants = expense.participants.all()
    num_participants = len(participants)

    if expense.split_type == 'EQUAL':
        individual_amounts = [{'user_id': participant.id, 'amount': round(amount / num_participants, 2)} for participant in participants]
    elif expense.split_type == 'EXACT':
        individual_amounts = [{'user_id': participant.id, 'amount': Decimal(expense.shares[str(participant.id)])} for participant in participants]
    elif expense.split_type == 'PERCENT':
        # total_percentage = sum(Decimal(split) for split in expense.shares.values())
        individual_amounts = [{'user_id': participant.id, 'amount': (amount * Decimal(expense.shares[str(participant.id)]) / 100)} for participant in participants]
    else:
        raise ValueError("Invalid expense split type")

    return individual_amounts

def update_balances(expense, splits):
    expense.shares = json.dumps(splits, cls=DecimalEncoder)
    expense.save()

    for split in splits:
        user = User.objects.get(id=split['user_id'])
        amount = split['amount']

        # Create or update Balance object
        balance, created = Balance.objects.get_or_create(
            user1=expense.payer, user2=user
        )
        
        if balance.amount is None:
            balance.amount = 0

        balance.amount += amount
        balance.save()
