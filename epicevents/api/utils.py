import pytz
from datetime import datetime
from .models import User, Client, Contract


utc = pytz.utc


def contact_is_support(serializer):
    contact = User.objects.get(id=serializer.validated_data.get('support_contact').id)
    if "Support" in contact.groups.values_list('name')[0]:
        return True
    return False


def change_contact_allowed(serializer, request, instance=None):
    if request.method == 'POST':
        return True
    data = serializer.validated_data
    if instance.support_contact == data['support_contact'] or request.user.groups.filter(name='Sales'):
        return True
    return False


def event_date_is_ok(serializer):
    event_date_data = serializer.validated_data.get('event_date').replace(tzinfo=utc)
    if event_date_data >= datetime.now().replace(tzinfo=utc):
        return True
    return False


def event_is_past(request, instance):
    if instance.event_date.replace(tzinfo=utc) < datetime.now().replace(tzinfo=utc):
        return False


def client_is_acquired(serializer):
    client = Client.objects.get(id=serializer.validated_data.get('client').id)
    return client.acquired


def date_is_ok(serializer):
    payment_data = serializer.validated_data.get('payment_due').replace(tzinfo=utc)
    if payment_data >= datetime.now().replace(tzinfo=utc):
        return True
    return False


def contract_is_signed(instance):
    return instance.status.id == 2


def amount_is_positive(serializer):
    amount_data = serializer.validated_data.get('amount')
    if amount_data > 0:
        return True
    return False


def attendees_is_positive(serializer):
    attendees_data = serializer.validated_data.get('attendees')
    if attendees_data > 0:
        return True
    return False


def event_is_available(serializer, request, instance=None):
    event_data = serializer.validated_data.get('event')
    linked_contracts = None
    if event_data is None:
        return True
    if request.method == 'POST':
        linked_contracts = Contract.objects.filter(event=event_data)
    if request.method == 'PUT':
        linked_contracts = Contract.objects.filter(event=event_data).exclude(id=instance.id)
    if len(linked_contracts) == 0:
        return True
    return False
