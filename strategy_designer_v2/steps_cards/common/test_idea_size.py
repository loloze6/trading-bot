"""idea_size.py on a record whose answer is known by construction."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from idea_size import size  # noqa: E402
import pandas as pd


def write_window(path, close, fc, alloc, value=None):
    """One window of hourly bars. Without a value series, the book's value follows the book without costs."""
    close = np.asarray(close, float); alloc = np.asarray(alloc, float)
    if value is None:
        r = np.append(close[1:] / close[:-1] - 1, 0.0)
        value = 1000 * np.cumprod(np.concatenate([[1.0], 1 + alloc[:-1] * r[:-1]]))
    n = len(close)
    df = pd.DataFrame({"timestamp": pd.date_range("2024-01-01", periods=n, freq="h", tz="UTC").strftime("%Y-%m-%d %H:%M:%S+00:00"),
                       "close": close, "forecast": fc, "previous_allocation": np.concatenate([[0.0], alloc[:-1]]),
                       "postRebalance_current_allocation": alloc, "postRebalance_total_value": value})
    path.mkdir(parents=True, exist_ok=True)
    df.to_csv(path / "bars.csv.gz", index=False)


def test_a_known_idea_size(tmp_path):
    # the coin alternates +1 % and -1 % each bar (usual move over 2 bars: known); after each signal it rises 2 % more
    n, H = 400, 2
    steps = np.array([1.01 if i % 2 else 0.99 for i in range(n)]); fc = np.zeros(n)
    for t in range(20, n - 10, 20):
        fc[t] = 5; steps[t + 1] *= 1.02
    close = 100 * np.cumprod(steps)
    write_window(tmp_path / "rec" / "BTCUSD" / "w1", close, fc, np.zeros(n))
    s = size(tmp_path / "rec", H)
    assert s["cases"] == len(range(20, n - 10, 20))
    assert s["unusual_move"] > 0.015                     # about 2 % above the coin's normal 2-bar move
    assert s["total_move"] == pytest.approx(s["unusual_move"] + s["normal_drift"], abs=1e-12)
    assert s["strength"] > 0


def test_no_signal_no_case(tmp_path):
    n = 100; write_window(tmp_path / "rec" / "BTCUSD" / "w1", np.linspace(100, 110, n), np.zeros(n), np.zeros(n))
    assert size(tmp_path / "rec", 5)["cases"] == 0
