"""
`visualize_data`'s window must not reach the sealed holdout — FORK-ONLY.

Found 2026-07-28 by the write tripwire, not by inspection. `launcher.py`
hardcoded `end_date = '2026-04-23'`, inside holdout_range (2026-01-01 ..
2026-06-30), with `localStorage=True` and a 60-second candle interval. A single
`python main.py visualize_data` therefore fetched roughly half a million 1m bars
straight across the seal and wrote them to local_data/BTCUSDT_1m.csv.

It then died on `fetcher.validate_quality_data_continuity(...)`, a method that
does not exist on any fetcher (BaseFetcher defines `validate_data_continuity`).
The AttributeError was swallowed by the broad `except Exception` and reported as
"Data visualization failed", so the mode announced failure AFTER the damage —
the cache write at `get_data()` happens first. That ordering is why no operator
would have connected the failure to a contaminated cache.

No BTCUSDT_1m.csv exists in this fork, so the mode was never actually run here.

The bound is now a literal one day before the seal rather than a policy read:
`tests/test_no_sealed_date_literals.py` scans production code for any date
inside holdout_range, so a seal that moves over this constant fails on the same
commit that moves it.

These tests drive the real method with a stub fetcher — no network, no disk.
"""

import sys
from pathlib import Path
from typing import ClassVar

import pandas as pd
import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core import launcher as launcher_mod  # noqa: E402

_POLICY = PROJECT_ROOT.parent / "strategy-research" / "config" / "campaign_data_policy.yaml"
with open(_POLICY, encoding="utf-8") as fh:
    HOLDOUT_START = pd.Timestamp(yaml.safe_load(fh)["holdout_range"][0])


class _RecordingFetcher:
    """Captures the window it was constructed with; serves one in-sample bar."""

    calls: ClassVar[list] = []

    def __init__(self, start_date, end_date, symbols, **kwargs):
        type(self).calls.append(
            {
                "start": pd.Timestamp(start_date),
                "end": pd.Timestamp(end_date),
                "symbols": symbols,
                "kwargs": kwargs,
            }
        )
        self.symbols = symbols

    def get_data(self):
        return {s: pd.DataFrame({"timestamp": [pd.Timestamp("2025-06-01")]}) for s in self.symbols}

    def validate_data_continuity(self, symbol):
        return True, []


@pytest.fixture
def run_visualize(monkeypatch):
    _RecordingFetcher.calls = []
    monkeypatch.setattr(launcher_mod, "HistoricalDataFetcher", _RecordingFetcher)

    def _run():
        lau = launcher_mod.Launcher.__new__(launcher_mod.Launcher)
        lau.logger = launcher_mod.logging.getLogger("trading_bot")
        lau.visualize_data()
        return _RecordingFetcher.calls

    return _run


def test_the_window_never_reaches_the_sealed_holdout(run_visualize):
    calls = run_visualize()

    assert len(calls) == 1
    assert calls[0]["end"] < HOLDOUT_START, (
        f"visualize_data would fetch through {calls[0]['end']}, at or past the "
        f"sealed holdout start {HOLDOUT_START.date()}"
    )


def test_the_window_is_not_inverted(run_visualize):
    calls = run_visualize()
    assert calls[0]["start"] < calls[0]["end"]


def test_it_completes_instead_of_dying_on_a_missing_method(run_visualize):
    """
    `validate_quality_data_continuity` does not exist. The call sat AFTER
    get_data(), so the mode wrote its cache and then raised, and the broad
    `except Exception` turned that into a plain "failed" message.

    A stub exposing only the real method name means this test fails with
    AttributeError while the typo is present -- and `sys.exit(1)` from the
    handler surfaces as SystemExit, so a regression cannot pass quietly.
    """
    run_visualize()  # must not raise, must not SystemExit
