from collections.abc import Iterable

import pytest

from fasty.items.service import fetch_all_items
from fasty.items.sql_models import Item


@pytest.mark.batch_num(5)
def test_fetch_all_items(_item_batch: Iterable[Item]):
    result = fetch_all_items()
    assert len(result) == 5
