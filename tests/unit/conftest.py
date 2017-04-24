import os

import pytest

from . import TEST_DATA_DIR


@pytest.fixture
def base_file_name():
    return os.path.join(TEST_DATA_DIR, 'base.csv')
