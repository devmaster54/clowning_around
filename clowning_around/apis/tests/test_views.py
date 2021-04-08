import pytest
from django.conf import settings
from django.test import RequestFactory
from rest_framework.test import APIRequestFactory, force_authenticate
from clowning_around.apis.views import AppointmentApi
from clowning_around.users.models import User


pytestmark = pytest.mark.django_db

