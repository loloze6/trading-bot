"""
CUL-250: a backtest that fetches OHLCV at a finer resolution than it trades on
must be distinguishable from one that doesn't, by its run identity.

Same fold and the same fail-loud collision guard model_funding (#54) and the
risk gate (PR #59) use -- transcribed from backtester.py _end_of_backtest.
"""
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from reporting.run_artifact import new_run_dir  # noqa: E402

_BASE = {"strategy": "x", "params": {"a": 1}}


def _fold(strategy_config, *, fetch_interval_seconds, interval_seconds):
    """The provenance fold, transcribed from backtester.py _end_of_backtest."""
    cfg = strategy_config
    if fetch_interval_seconds != interval_seconds:
        if "fetch_interval_seconds" in cfg:
            raise ValueError("collision")
        cfg = {**cfg, "fetch_interval_seconds": fetch_interval_seconds}
    return cfg


def test_default_is_the_same_object_so_identity_cannot_move():
    """fetch_interval_seconds == interval_seconds (the default, DataManager
    resolves None to interval_seconds) must leave the config object itself
    untouched -- nothing downstream can hash differently."""
    out = _fold(_BASE, fetch_interval_seconds=14400, interval_seconds=14400)
    assert out is _BASE


def test_diverging_changes_the_provenance_config():
    out = _fold(_BASE, fetch_interval_seconds=3600, interval_seconds=14400)
    assert out is not _BASE
    assert out["fetch_interval_seconds"] == 3600
    assert _BASE == {"strategy": "x", "params": {"a": 1}}, "input must not be mutated"


def test_diverging_and_default_do_not_share_a_run_dir_hash(tmp_path):
    """The actual CUL-250-class symptom: two runs that differ only by the
    fetch resolution must not land on the same config hash."""
    default_dir = new_run_dir(
        str(tmp_path / "default"), _fold(_BASE, fetch_interval_seconds=14400, interval_seconds=14400)
    )
    finer_dir = new_run_dir(
        str(tmp_path / "finer"), _fold(_BASE, fetch_interval_seconds=3600, interval_seconds=14400)
    )
    default_hash = Path(default_dir).name.split("_")[-1]
    finer_hash = Path(finer_dir).name.split("_")[-1]
    assert default_hash != finer_hash, (
        f"fetch_interval_seconds diverging vs matching share config hash {default_hash} -- "
        "the manifest cannot distinguish the two runs"
    )


def test_collision_fails_loud_rather_than_overwriting():
    """A silent {**cfg, 'fetch_interval_seconds': X} would mask a real
    difference in run identity if the strategy config ever carried that key."""
    with pytest.raises(ValueError, match="collision"):
        _fold(
            {**_BASE, "fetch_interval_seconds": 900},
            fetch_interval_seconds=3600,
            interval_seconds=14400,
        )
