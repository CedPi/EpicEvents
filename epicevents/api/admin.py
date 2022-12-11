from django.contrib import admin
from api.models import Client, Contract, ContractStatus, Event


admin.site.register((Client, Contract, ContractStatus, Event))
