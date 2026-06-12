from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

import pytest

from app.db.repositories import InvoiceRepository


@pytest.fixture
def mock_db():
    return AsyncMock()


@pytest.fixture
def repo(mock_db):
    return InvoiceRepository(db=mock_db)



@pytest.mark.asyncio
async def test_get_all_with_date_filters(repo, mock_db):
    mock_db.scalar.return_value = 0
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_db.execute.return_value = mock_result

    start = datetime(2024, 1, 1)
    end = datetime(2024, 12, 31)
    total, items = await repo.get_all(start_date=start, end_date=end, offset=0, limit=10)

    assert total == 0
    assert items == []


@pytest.mark.asyncio
async def test_get_all_respects_pagination(repo, mock_db):
    all_invoices = [MagicMock(id=i, total=i * 10.0) for i in range(0, 15)]

    mock_db.scalar.return_value = 15
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = all_invoices[:5]
    mock_db.execute.return_value = mock_result

    total, items = await repo.get_all(start_date=None, end_date=None, offset=0, limit=5)

    assert total == 15
    assert len(items) == 5
    assert items[0].id == 0
    assert items[4].id == 4

    mock_result2 = MagicMock()
    mock_result2.scalars.return_value.all.return_value = all_invoices[5:10]
    mock_db.execute.return_value = mock_result2

    total2, items2 = await repo.get_all(start_date=None, end_date=None, offset=5, limit=5)

    assert total2 == 15
    assert len(items2) == 5
    assert items2[0].id == 5
    assert items2[4].id == 9
