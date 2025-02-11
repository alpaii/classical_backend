# tests/conftest.py
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """테스트용 APIClient를 반환하는 pytest fixture"""
    return APIClient()
