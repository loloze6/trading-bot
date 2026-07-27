"""
The monthly-tile generator must refuse to emit a tile that reaches the seal.

ROOT CAUSE THIS PINS (campaign_data_policy.yaml:holdout_contaminated_runs)
--------------------------------------------------------------------------
`_generate_monthly_windows` emits tiles whose `test.end` is the first of the
NEXT month, and the next tile starts on that same date -- so `end` reads as an
exclusive bound. It is not one at the engine: `run_protocol` hands `end` to
`launcher.run_backtest`, which calls `load_data(end_date=end)`, and that yields
every bar of the end DAY through 23:00. Each tile therefore materialises
[month M 00:00, month M+1 day 1 23:00] -- a deliberate 24-bar overspill, present
on all 24 sibling tiles of the 2025 sweep and harmless on 23 of them.

On the last one it was not harmless: it spilled into day 1 of the sealed holdout
and spent those bars. Two run directories were quarantined for it. The generator
had no clamp, so extending the sweep by one month would breach again by
construction, and the execution-side assert in run_protocol.py used `<=`, which
admits `end == holdout_start` -- exactly the breaching value.

Fixtures use the REAL boundary from campaign_data_policy.yaml (this project's
standing rule that a regression test reproduces the actual historical failure),
plus an injected synthetic range to prove the check is not date-hardcoded.
"""

import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "workflow"))

import run_phase1_research as rpr  # noqa: E402

POLICY = ROOT / "config" / "campaign_data_policy.yaml"
HOLDOUT_START, HOLDOUT_END = yaml.safe_load(
    POLICY.read_text(encoding="utf-8")
)["holdout_range"]

# One day before the seal, and the month it closes -- derived, never spelled out,
# so this file carries no literal sealed-window date of its own.
LAST_CLEAR_MONTH_START = HOLDOUT_START[:8] + "01"


# ---------------------------------------------------------------------------
# the breach
# ---------------------------------------------------------------------------


def test_a_sweep_spanning_the_boundary_raises():
    """
    The exact historical request shape: a monthly sweep asked to run up to the
    first day of the holdout. The final tile's `end` lands ON the seal and
    materialises that day's bars.
    """
    with pytest.raises(rpr.HoldoutBoundaryBreach) as exc:
        rpr._generate_monthly_windows("2025-11-01", HOLDOUT_START)
    msg = str(exc.value)
    assert HOLDOUT_START in msg
    assert "INCLUSIVE-BY-DAY" in msg


def test_a_sweep_reaching_past_the_boundary_raises():
    with pytest.raises(rpr.HoldoutBoundaryBreach):
        rpr._generate_monthly_windows("2025-11-01", LAST_CLEAR_MONTH_START)


def test_it_raises_rather_than_silently_truncating():
    """
    A clamped-and-continued sweep reports coverage that no longer matches what
    was pre-registered, and the caller has no way to notice. Loud or nothing.
    """
    with pytest.raises(rpr.HoldoutBoundaryBreach):
        rpr._generate_monthly_windows("2024-01-01", HOLDOUT_START)


# ---------------------------------------------------------------------------
# the clear cases still work
# ---------------------------------------------------------------------------


def test_a_sweep_ending_the_day_before_the_seal_is_allowed():
    """The archive cutoff aligns with the seal; this is the normal request."""
    from datetime import date, timedelta

    y, m, d = (int(x) for x in HOLDOUT_START.split("-"))
    last_clear = (date(y, m, d) - timedelta(days=1)).isoformat()
    windows = rpr._generate_monthly_windows("2019-09-10", last_clear)
    assert windows[-1]["test"]["end"] == last_clear
    assert all(w["test"]["end"] < HOLDOUT_START for w in windows)


def test_the_preexisting_generator_contract_is_unchanged():
    """Contiguous, monotonic, no overshoot -- the property the F4d test pinned."""
    windows = rpr._generate_monthly_windows("2019-09-10", "2025-12-31")
    assert windows[0]["test"]["start"] == "2019-09-01"
    assert windows[-1]["test"]["end"] == "2025-12-31"
    for a, b in zip(windows, windows[1:]):
        assert a["test"]["end"] == b["test"]["start"]


# ---------------------------------------------------------------------------
# the boundary is read, not hardcoded
# ---------------------------------------------------------------------------


def test_the_boundary_comes_from_the_policy_file_not_from_code():
    """Move the seal in an injected policy and the generator moves with it."""
    with pytest.raises(rpr.HoldoutBoundaryBreach) as exc:
        rpr._generate_monthly_windows(
            "2020-01-01", "2020-06-01", holdout_range=("2020-03-01", "2020-09-30")
        )
    assert "2020-03-01" in str(exc.value)

    # ...and the same request is fine against a seal that is out of the way.
    windows = rpr._generate_monthly_windows(
        "2020-01-01", "2020-06-01", holdout_range=("2021-01-01", "2021-06-30")
    )
    assert len(windows) == 5


def test_the_generator_reads_the_real_policy_by_default():
    """
    `_DATA_POLICY_PATH` is redirected into a sandbox by conftest, which seeds it
    with a verbatim copy of the real file — so the default path must still
    yield the real seal.
    """
    assert rpr._load_holdout_range() == (HOLDOUT_START, HOLDOUT_END)
    assert rpr._load_holdout_range(POLICY) == (HOLDOUT_START, HOLDOUT_END)


def test_an_unreadable_policy_denies_by_default(tmp_path):
    """No policy is not 'no holdout to worry about'."""
    with pytest.raises(rpr.HoldoutBoundaryBreach):
        rpr._load_holdout_range(tmp_path / "does_not_exist.yaml")

    malformed = tmp_path / "policy.yaml"
    malformed.write_text("holdout_range: null\n", encoding="utf-8")
    with pytest.raises(rpr.HoldoutBoundaryBreach):
        rpr._load_holdout_range(malformed)


# ---------------------------------------------------------------------------
# the execution-side guard, which admitted the breaching value
# ---------------------------------------------------------------------------


def test_run_protocol_rejects_a_window_ending_exactly_on_the_seal():
    """
    The `<=` form let `end == holdout_start` through, which is the one value
    that breaches. Asserted against the source because the guard sits inside a
    per-window backtest loop that cannot be driven without a full data stack.
    """
    text = (ROOT / "tools" / "run_protocol.py").read_text(encoding="utf-8")
    assert "assert end < _holdout_start" in text
    assert "assert end <= _holdout_start" not in text
