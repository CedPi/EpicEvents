from rest_framework import permissions, filters, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from datetime import datetime
import pytz
from api import utils
from api.models import Client, Contract, ContractStatus, Event
from api.serializer import (
    ClientSerializer,
    ContractSerializer,
    EventSerializer,
    SimpleEventSerializer,
    SimpleContractSerializer
)
from api.permissions import (
    IsSales,
    IsSupport,
    IsClientOwner,
    IsContractOwner,
    HasEventPermissions,
    IsEventOwner
)


utc = pytz.utc


class ClientView(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    search_fields = ['last_name', 'email', 'date_created']
    filter_backends = (filters.SearchFilter,)
    permission_classes = [permissions.IsAuthenticated & (IsSales & IsClientOwner)]

    def create(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data['sales_contact'] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data['sales_contact'] = request.user
        data['date_updated'] = datetime.now().replace(tzinfo=utc)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def perform_update(self, serializer):
        instance = self.get_object()
        serializer.update(instance, serializer.validated_data)


class ContractView(ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    search_fields = ['client__last_name', 'client__email', 'date_created', 'amount']
    filter_backends = (filters.SearchFilter,)
    permission_classes = [permissions.IsAuthenticated & (IsSales & IsContractOwner)]

    def check_inputs(self, serializer, request, errors, instance=None):
        if not utils.client_is_acquired(serializer):
            errors['ERREUR_CLIENT'] = "Le client n'est pas acquis"
        if not utils.date_is_ok(serializer):
            errors['ERREUR_DATE'] = "La date de paiement est passée"
        if not utils.event_is_available(serializer, request, instance):
            errors['ERREUR_EVENEMENT'] = "L'évènement n'est pas disponible"
        if not utils.amount_is_positive(serializer):
            errors['ERREUR_MONTANT'] = "Le montant doit être positif"
        if not utils.contract_is_signed(instance) and serializer.validated_data['event'] is not None:
            errors['ERREUR_CONTRAT'] = "Impossible de rattacher un évènement à un contrat non signé"
        if len(errors) == 0:
            return True
        return False

    def create(self, request, *args, **kwargs):
        errors = {}
        serializer = SimpleContractSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data['sales_contact'] = request.user
        data['status'] = ContractStatus.objects.get(id=1)
        headers = self.get_success_headers(serializer.validated_data)
        if self.check_inputs(serializer, request, errors):
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        errors = {}
        serializer = SimpleContractSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data['sales_contact'] = request.user
        data['date_updated'] = datetime.now().replace(tzinfo=utc)
        headers = self.get_success_headers(serializer.validated_data)
        if self.check_inputs(serializer, request, errors, self.get_object()):
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST, headers=headers)

    def perform_update(self, serializer):
        instance = self.get_object()
        serializer.update(instance, serializer.validated_data)


class EventView(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    search_fields = ['event_date', 'contract__client__last_name', 'contract__client__email']
    filter_backends = (filters.SearchFilter,)
    permission_classes = [permissions.IsAuthenticated & ((IsSales & IsEventOwner) | (IsSupport & HasEventPermissions))]

    def check_inputs(self, serializer, request, errors, instance=None):
        if not utils.event_date_is_ok(serializer):
            errors['ERREUR_DATE'] = "La date de l'évènement est passée"
        if not utils.attendees_is_positive(serializer):
            errors['ERREUR_INVITES'] = "Le nombre d'invités doit être positif"
        if not utils.contact_is_support(serializer):
            errors['ERREUR_CONTACT'] = "Le contact doit être de l'équipe Support"
        if not utils.change_contact_allowed(serializer, request, instance):
            errors['ERREUR_TYPE_CONTACT'] = "Seul un membre de l'équipe Sales peut changer le contact"
        if len(errors) == 0:
            return True
        return False

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.serializer_class(instance).data
        if instance.event_date < datetime.now().replace(tzinfo=utc):
            self.permission_classes = [permissions.IsAuthenticated & (IsSales & IsEventOwner)]
            data['INFO_EVENEMENT_PASSE'] = "Impossible de modifier un évènement passé"
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        errors = {}
        serializer = SimpleEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data['created_by'] = request.user
        headers = self.get_success_headers(serializer.validated_data)
        if self.check_inputs(serializer, request, errors):
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        errors = {}
        serializer = SimpleEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data['date_updated'] = datetime.now().replace(tzinfo=utc)
        headers = self.get_success_headers(serializer.validated_data)
        if self.check_inputs(serializer, request, errors, instance=self.get_object()):
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST, headers=headers)

    def perform_update(self, serializer):
        instance = self.get_object()
        serializer.update(instance, serializer.validated_data)
