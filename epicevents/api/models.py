from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    company_name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    acquired = models.BooleanField(default=False)
    sales_contact = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Event(models.Model):
    # client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, related_name='client_id')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    support_contact = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    attendees = models.IntegerField()
    event_date = models.DateTimeField(auto_now_add=False)
    notes = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='created_by')

    def __str__(self):
        return f"{self.notes} - {self.event_date}"


class ContractStatus(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "contract status"


class Contract(models.Model):
    sales_contact = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(ContractStatus, on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    payment_due = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return f"{self.client} - {self.event}"
