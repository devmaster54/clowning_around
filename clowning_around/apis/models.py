from django.db import models
from clowning_around.users.models import Clown, Client


class AppointmentModel(models.Model):
    APPOINTMENT_STATUS = (
        (1, "upcoming"),
        (2, "incipient"),
        (3, "completed"),
        (4, "cancelled"),
    )
    clown = models.ForeignKey(Clown, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.IntegerField(default=1, choices=APPOINTMENT_STATUS)
    created_at = models.DateTimeField(auto_now=True)


class IssueModel(models.Model):
    appointment = models.ForeignKey(
        AppointmentModel, on_delete=models.SET_NULL, null=True, blank=True
    )
    issue = models.CharField(default="", max_length=255)


class RequestModel(models.Model):
    appointment = models.ForeignKey(
        AppointmentModel, on_delete=models.SET_NULL, null=True, blank=True
    )
    reason = models.CharField(default="", max_length=255)


class RateEmojiModel(models.Model):
    appointment = models.ForeignKey(
        AppointmentModel, on_delete=models.SET_NULL, null=True, blank=True
    )
    emoji = models.CharField(default="", max_length=255)
