import pandas as pd
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from execution.portfolio_info import flatten_dict_columns


def test_flatten_no_repeated_prefix():
    df = pd.DataFrame([{"a": {"controls": {"x": {"passed": True, "v": 1.0}}}}])
    result = flatten_dict_columns(df)
    cols = set(result.columns)
    assert cols == {"a.controls.x.passed", "a.controls.x.v"}, f"Unexpected columns: {cols}"
    for col in cols:
        parts = col.split(".")
        for i in range(1, len(parts)):
            prefix = ".".join(parts[:i])
            remainder = ".".join(parts[i:])
            assert not remainder.startswith(prefix), f"Repeated prefix in column {col!r}"
