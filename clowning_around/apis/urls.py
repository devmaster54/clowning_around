from django.urls import path
from clowning_around.apis.views import (
    AppointmentApi,
    RequestContactApi,
    ReportIssueApi,
    RateEmojiApi,
)


app_name = "apis"

urlpatterns = [
    path("appointment/", AppointmentApi.as_view(), name="appointment"),
    path("request-contact/", RequestContactApi.as_view(), name="request_contact"),
    path("report-issue/", ReportIssueApi.as_view(), name="report_issue"),
    path("rate-emoji/", RateEmojiApi.as_view(), name="rate_emoji"),
]
