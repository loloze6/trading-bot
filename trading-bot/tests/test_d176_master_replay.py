"""
D-176 byte-identity against a recording made on MASTER's code (no D-176).

strategy-research/tests/fixtures/d176/master_recorded_run_{099,084}.csv are the bars.csv files
master produced for run_099's and run_084's real configs (no strategies.sizing block) over the
seeded synthetic daily series next to them (README.md there: master sha, seed, command). This
test replays the same series through THIS checkout's code with the same real entry point
(core.launcher.run_backtest; only the data fetch is replaced by a CSV read) and compares the
whole file -- header and every row string -- after normalising CRLF (recorded on Windows).
No column is excluded. No stub strategy; nothing here imports from a master checkout.
"""
import importlib.util
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = PROJECT_ROOT.parent
FX = REPO_ROOT / "strategy-research" / "tests" / "fixtures" / "d176"
CONFIGS = {
    "run_099": (FX / "run_099_strategy_config.json", FX / "master_recorded_run_099.csv"),
    "run_084": (REPO_ROOT / "strategy-research" / "tests" / "fixtures" / "d142"
                / "run_084_BTCUSD_2018-05" / "strategy_config.json",
                FX / "master_recorded_run_084.csv"),
}


def _harness():
    spec = importlib.util.spec_from_file_location("d176_replay_harness", FX / "replay_harness.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _lines(path):
    return Path(path).read_bytes().replace(b"\r\n", b"\n").decode("utf-8").split("\n")


@pytest.mark.parametrize("name", sorted(CONFIGS))
def test_branch_replay_equals_the_master_recording_byte_for_byte(name, tmp_path):
    config, recorded = CONFIGS[name]
    assert "sizing" not in config.read_text()
    bars = _harness().replay(PROJECT_ROOT, config, FX / "synthetic_daily_ohlcv.csv", tmp_path)
    got, want = _lines(bars), _lines(recorded)
    assert got[0] == want[0]                                     # same header, same column order
    assert len(got) == len(want) > 600
    for i, (g, w) in enumerate(zip(got, want)):
        assert g == w, f"row {i} differs"
    # the recording is not a flat book: the comparison covers real orders
    assert _harness().assert_traded(recorded) >= 5               # never passes on an all-flat recording
    assert _harness().assert_traded(bars) >= 5


def test_the_recorded_series_is_the_seeded_one(tmp_path):
    """The CSV the recordings were made over is reproducible from its seed (numpy default_rng)."""
    import pandas as pd

    h = _harness()
    h.make_series(tmp_path / "again.csv")
    again = pd.read_csv(tmp_path / "again.csv")
    kept = pd.read_csv(FX / "synthetic_daily_ohlcv.csv")
    # the recordings were made over the committed CSV (the replay reads it, never regenerates it);
    # numpy's exp/cumsum can differ in the last ulp across platforms, so compare to 1e-12
    assert list(again.columns) == list(kept.columns) and (again["timestamp"] == kept["timestamp"]).all()
    pd.testing.assert_frame_equal(again, kept, rtol=1e-12, atol=0)
