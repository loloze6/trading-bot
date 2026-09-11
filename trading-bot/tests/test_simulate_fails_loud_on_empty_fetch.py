"""`simulate` must exit non-zero when the data fetch returns nothing.

Before this guard a total fetch failure produced a *successful-looking* run:
the loop iterated over an empty series, metrics came out all-zero, the run
artifact recorded the hash of nothing, and the process exited 0. That is the
worst shape a failure can take here -- it is indistinguishable from a real
backtest of a strategy that simply never traded, so it can be read as evidence.

Drives the real Launcher.simulate() with a stubbed engine, so the assertion is
about the CLI path's own behaviour rather than a helper's.
"""
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import core.launcher as launcher_mod  # noqa: E402


class _StubEngine:
    """Stands in for BacktestEngine: records whether the sim was ever run."""

    simulated = False

    def __init__(self, *_, **kwargs):
        self._symbols = kwargs.get("symbols") or ["BTCUSDT"]
        self.historical_data = {}

    def load_data(self, **_):
        # The failure under test: fetch "succeeds" but yields nothing.
        self.historical_data[self._symbols[0]] = []

    def simulate_on_loaded_data(self):
        type(self).simulated = True
        return {}


class _StubStrategy:
    """Minimal stand-in for AdvancedStrategy -- just enough shape for
    Launcher.simulate() to read before it ever reaches load_data(). E-055 added
    a min_allocation_change_override read at this point (real AdvancedStrategy
    always has the attribute, None or not); a bare `None` strategy object
    doesn't, so it must be stubbed here too."""

    min_allocation_change_override = None


@pytest.fixture
def _stubbed(monkeypatch):
    _StubEngine.simulated = False
    monkeypatch.setattr(launcher_mod, "BacktestEngine", _StubEngine)
    monkeypatch.setattr(launcher_mod, "AdvancedStrategy", lambda *a, **k: _StubStrategy())
    return _StubEngine


def test_empty_fetch_exits_nonzero(_stubbed):
    with pytest.raises(SystemExit) as exc:
        launcher_mod.Launcher().simulate()
    assert exc.value.code != 0, "an empty fetch must not report success"


def test_empty_fetch_does_not_run_the_simulation(_stubbed):
    """Fail before simulating, not after.

    Running the loop first and erroring afterwards would still write the
    zero-metric artifact this guard exists to prevent.
    """
    with pytest.raises(SystemExit):
        launcher_mod.Launcher().simulate()
    assert not _stubbed.simulated, (
        "the simulation ran despite there being no data -- the guard is placed "
        "after simulate_on_loaded_data() instead of before it")
