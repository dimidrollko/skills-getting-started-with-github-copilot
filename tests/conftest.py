import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as activities_data


@pytest.fixture
def client():
    original_activities = copy.deepcopy(activities_data)

    with TestClient(app) as client:
        yield client

    activities_data.clear()
    activities_data.update(original_activities)
