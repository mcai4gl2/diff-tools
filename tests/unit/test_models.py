from StringIO import StringIO

from mock import patch, sentinel, MagicMock
import pandas as pd

import diff.tools.models as models

from . import for_all


def test_can_handle_non_exist_base_file():
    task = models.DiffTask("non_exist_base_file", "non_exist_reg_file", [], [])
    results = task.compute()
    assert len(results) == 1
    diff = results[0]
    assert type(diff) == models.MissingDifference
    assert diff.type == models.DifferenceType.file_not_found
    assert diff.base_is_missing


def test_can_handle_non_exist_reg_file(base_file_name):
    task = models.DiffTask(base_file_name, "non_exist_reg_file", [], [])
    results = task.compute()
    assert len(results) == 1
    diff = results[0]
    assert type(diff) == models.MissingDifference
    assert diff.type == models.DifferenceType.file_not_found
    assert not diff.base_is_missing


def test_compute(base_file_name):
    with patch('diff.tools.models.col_diff') as col_diff, \
         patch('diff.tools.models.duplicate_keys') as duplicate_keys:
        col_diff.return_value = [sentinel.col_diff]
        duplicate_keys.return_value = [MagicMock()]
        task = models.DiffTask(base_file_name, base_file_name, [], [])
        results = task.compute()
        col_diff.assert_called_once()
        duplicate_keys.assert_called()
        assert duplicate_keys.call_count == 2
        assert sentinel.col_diff in results


def test_col_diff_handles_matching_base_reg_columns(some_df):
    results = models.col_diff(some_df, some_df)
    assert len(results) == 0


def test_col_diff_handles_base_having_more_cols(some_df, empty_df):
    results = models.col_diff(some_df, empty_df)
    assert len(results) == len(some_df.columns)
    assert for_all(results, lambda r: not r.base_is_missing)
    assert for_all(results, lambda r: r.type == models.DifferenceType.column_not_found)


def test_col_diff_handles_reg_having_more_cols(some_df, empty_df):
    results = models.col_diff(empty_df, some_df)
    assert len(results) == len(some_df.columns)
    assert for_all(results, lambda r: r.base_is_missing)
    assert for_all(results, lambda r: r.type == models.DifferenceType.column_not_found)


def test_find_duplicate_keys_when_there_is_no_duplicate_keys():
    input_data = StringIO("""col1,col2,col3
1,2,3
4,5,6
7,8,9
""")
    df = pd.read_csv(input_data, sep=",")
    results = models.duplicate_keys(df, ["col1"])
    assert len(results) == 0


def test_find_duplicate_keys_handles_single_key_difference():
    input_data = StringIO("""col1,col2,col3
c1,2,3
c1,5,6
c1,8,9
""")
    df = pd.read_csv(input_data, sep=",")
    results = models.duplicate_keys(df, ["col1"])
    assert len(results) == 2
    result = results[0]
    assert type(result) == models.DuplicationDifference
    assert result.type == models.DifferenceType.duplicated_keys
    assert result.keys == ['c1']
    assert result.is_base is None
    assert result.line_number == 2
    result = results[1]
    assert type(result) == models.DuplicationDifference
    assert result.type == models.DifferenceType.duplicated_keys
    assert result.keys == ['c1']
    assert result.is_base is None
    assert result.line_number == 3


def test_find_duplicate_keys_handles_multi_keys_difference():
    input_data = StringIO("""col1,col2,col3
1,2,3
1,2,6
7,2,9
""")
    df = pd.read_csv(input_data, sep=",")
    results = models.duplicate_keys(df, ["col1", "col2"])
    assert len(results) == 1
    result = results[0]
    assert type(result) == models.DuplicationDifference
    assert result.type == models.DifferenceType.duplicated_keys
    assert result.keys == [1, 2]
    assert result.is_base is None