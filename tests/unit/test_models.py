import diff.tools.models as models


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
