"""flatten_dict_columns (2026-11-18): the frame the row-by-row expansion gives (each row one dtype, as pd.Series(x)
has), built with one construction per column. The reference below is the former code, kept here as the test."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from execution.portfolio_info import flatten_dict_columns  # noqa: E402


def reference(df):
    changed = True
    while changed:
        changed = False
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, dict) and len(x) > 0).any():
                df = df.drop(columns=[col]).join(
                    df[col].apply(lambda x: pd.Series(x) if isinstance(x, dict) else pd.Series(dtype=object))
                    .add_prefix(f"{col}."))
                changed = True
    return df


def test_the_same_frame_as_the_row_by_row_expansion():
    rows = [
        {"t": 1, "bal": {"USDT": {"free": 10.5, "locked": 0}, "BTC": {"free": 1, "locked": 0}}, "dbg": {"a": True}},
        {"t": 2, "bal": {"USDT": {"free": 9, "locked": 1}, "BTC": {"free": np.float64(0.5), "locked": None}},
         "dbg": {"a": False, "b": "x"}},
        {"t": 3, "bal": {}, "dbg": None},
        {"t": 4, "bal": {"USDT": {"free": 1, "locked": 2}}, "dbg": {"a": 1, "c": pd.Timestamp("2024-01-01")}},
    ]
    df = pd.DataFrame(rows)
    pd.testing.assert_frame_equal(flatten_dict_columns(df.copy()), reference(df.copy()), check_exact=True)


def test_a_frame_without_dicts_is_unchanged():
    df = pd.DataFrame({"a": [1, 2], "b": [0.5, None]})
    pd.testing.assert_frame_equal(flatten_dict_columns(df.copy()), df)
