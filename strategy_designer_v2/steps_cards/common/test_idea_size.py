"""idea_size.py on a record whose answer is known by construction."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from idea_size import size  # noqa: E402
from test_book_diagnosis import write_window  # noqa: E402


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
