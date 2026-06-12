from unittest.mock import AsyncMock
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.db.database import get_db
from app.db.repositories import InvoiceRepository


@pytest.fixture
def mock_repo():
    return AsyncMock(spec=InvoiceRepository)


@pytest.fixture
def client(mock_repo):
    app.dependency_overrides[get_db] = lambda: AsyncMock()

    # Patch get_repo in the router to return mock_repo directly
    from app.api import invoices as inv_module
    app.dependency_overrides[inv_module.get_repo] = lambda: mock_repo

    yield AsyncClient(transport=ASGITransport(app=app), base_url="http://test")

    app.dependency_overrides.clear()
