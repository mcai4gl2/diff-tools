import os


TEST_DATA_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_DATA_DIR = os.path.join(TEST_DATA_DIR, 'data')


def for_all(list, func):
    return all([func(i) for i in list])
