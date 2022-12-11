from rest_framework import serializers
from api.models import Client, Contract, Event


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name', 'acquired']


class SimpleContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('id', 'amount', 'payment_due', 'client', 'event', 'status')


class ContractSerializer(SimpleContractSerializer):
    event_details = serializers.SerializerMethodField(read_only=True)
    client_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Contract
        fields = ('id', 'amount', 'payment_due', 'client', 'client_details', 'event', 'event_details', 'status')

    def get_event_details(self, obj):
        event = Event.objects.filter(id=obj.event_id)
        if event:
            serializer = SimpleEventSerializer(event, many=True)
            return serializer.data[0]
        return "Aucun évènement rattaché pour l'instant"

    def get_client_details(self, obj):
        client = Client.objects.filter(id=obj.client_id)
        if client:
            serializer = ClientSerializer(client, many=True)
            return serializer.data[0]
        return "Aucun client rattaché pour l'instant"


class SimpleEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'attendees', 'event_date', 'notes', 'support_contact')


class EventSerializer(SimpleEventSerializer):
    client = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'attendees', 'event_date', 'notes', 'client', 'support_contact')

    def get_client(self, obj):
        contract = Contract.objects.filter(event_id=obj.id).first()
        if contract is not None:
            client = Client.objects.filter(id=contract.client_id)
            serializer = ClientSerializer(client, many=True)
            return serializer.data[0]
        return "Cet évènement n'est pas encore rattaché à un contrat"
