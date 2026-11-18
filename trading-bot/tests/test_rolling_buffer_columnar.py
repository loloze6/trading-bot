"""The history table built from columns (2026-11-18, `strategies/strategy_base.RollingBuffer`): every frame equals
the one `pd.DataFrame(list of bar dicts)` gives, exactly; any bar outside the columnar kinds switches the buffer back
to that construction. Measured gain: `strategy_designer_v2/steps_cards/orchestration/duration/`."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from strategies.strategy_base import RollingBuffer  # noqa: E402

T0 = pd.Timestamp("2024-01-01")


def bar(i, **over):
    d = {"timestamp": T0 + pd.Timedelta(hours=i), "close": float(i), "volume": np.float64(i / 2), "n": i,
         "flag": i % 2 == 0}
    d.update(over)
    return d


def same(buf):
    pd.testing.assert_frame_equal(buf.get_df(), pd.DataFrame(list(buf.bars)), check_exact=True)


def test_every_frame_equals_the_list_of_dicts_frame_across_many_slides():
    b = RollingBuffer(max_size=5)
    for i in range(43):
        b.add_data(bar(i))
        same(b)
    assert b._columnar and len(b.get_df()) == 5 and b.get_df()["close"].tolist() == [38.0, 39.0, 40.0, 41.0, 42.0]


def test_the_frame_does_not_share_memory_with_the_arrays():
    b = RollingBuffer(max_size=3)
    for i in range(3):
        b.add_data(bar(i))
    df = b.get_df()
    b.add_data(bar(3))
    assert df["close"].tolist() == [0.0, 1.0, 2.0]


def test_other_values_fall_back_to_the_list_of_dicts_construction():
    for odd in ({"close": None}, {"close": "x"}, {"timestamp": pd.Timestamp("2024-01-01", tz="UTC")}):
        b = RollingBuffer(max_size=4)
        b.add_data(bar(0))
        b.add_data(bar(1, **odd))
        b.add_data(bar(2))
        assert not b._columnar
        same(b)
    b = RollingBuffer(max_size=4)                     # a column changing kind, and keys in another order
    b.add_data(bar(0))
    b.add_data(bar(1, n=1.5))
    assert not b._columnar
    same(b)
    b = RollingBuffer(max_size=4)
    b.add_data(bar(0))
    b.add_data(dict(reversed(list(bar(1).items()))))
    assert not b._columnar
    same(b)


def test_clear_starts_columnar_again():
    b = RollingBuffer(max_size=4)
    b.add_data(bar(0, close=None))
    assert not b._columnar
    b.clear()
    for i in range(6):
        b.add_data(bar(i))
    assert b._columnar
    same(b)
