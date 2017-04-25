from enum import Enum

import pandas as pd


class DifferenceType(Enum):
    file_not_found = 1
    column_not_found = 2


class DiffTask(object):
    def __init__(self, base_file_name, reg_file_name, key_list, column_list):
        self.base_file = base_file_name
        self.reg_file = reg_file_name
        self.keys = key_list
        self.columns = column_list
        self.differences = list()

    def compute(self):
        self.differences = list()
        try:
            base_df = pd.read_csv(self.base_file)
        except Exception as ex:
            self.differences.append(MissingDifference(DifferenceType.file_not_found, ex, True))
            return self.differences
        try:
            reg_df = pd.read_csv(self.reg_file)
        except Exception as ex:
            self.differences.append(MissingDifference(DifferenceType.file_not_found, ex, False))
            return self.differences
        self.differences.extend(col_diff(base_df, reg_df))
        return self.differences


def col_diff(base_df, reg_df):
    results = list()
    for col in base_df.columns:
        if col not in reg_df:
            results.append(MissingDifference(DifferenceType.column_not_found, col, False))
    for col in reg_df.columns:
        if col not in base_df:
            results.append(MissingDifference(DifferenceType.column_not_found, col, True))
    return results


class MissingDifference(object):
    def __init__(self, type, data, base_is_missing):
        self.type = type
        self.data = data
        self.base_is_missing = base_is_missing


class DataDifference(object):
    def __init__(self, keys, at, column, type, base_value, reg_value):
        self.keys = keys
        self.at = at
        self.column = column
        self.type = type
        self.base_value = base_value
        self.reg_value = reg_value
