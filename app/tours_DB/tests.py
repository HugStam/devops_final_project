from django.test import TestCase
from django.urls import reverse
import pytest
from tours_DB.models import Customers
# Create your tests here.
def test_homepage_access():
    url = reverse('home')
    assert url == "/"

   