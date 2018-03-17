from django.test import TestCase
from django.http import HttpRequest

from .views import HomeListView


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        pass
