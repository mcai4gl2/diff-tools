from mock import patch, sentinel

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


def test_diff_checks_col_differences(base_file_name):
    with patch('diff.tools.models.col_diff') as col_diff:
        col_diff.return_value = [sentinel.col_diff]
        task = models.DiffTask(base_file_name, base_file_name, [], [])
        results = task.compute()
        col_diff.assert_called_once()
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
