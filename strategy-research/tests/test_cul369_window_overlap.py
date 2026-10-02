"""
CUL-369 (D-058): protocol windows must not share a day.

`test.end` is the LAST INCLUDED DAY -- the engine loads every bar of a
date-only end (trading-bot base_fetcher._inclusive_end). Protocols used to write
`end` as the next window's start, so that day was backtested in two windows:
pooled records double-counted it and the grid's time-ordered fit refused it
(run_064's RecordOrderError). One convention now, the engine's:
  * the monthly generator ends each tile on the month's last day;
  * run_protocol refuses, before any backtest, windows that share a day;
  * the hand-made protocols were migrated (end = next start - 1 day);
  * the data gate measures each window through its end day's last bar.
"""
import json
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import pytest

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import data_availability_gate as dag  # noqa: E402
import run_phase1_research as rpr  # noqa: E402
import run_protocol as rp  # noqa: E402

_FAR_SEAL = ("2030-01-01", "2030-06-30")  # an injected seal out of the way


def _w(label, start, end):
    return {"label": label, "test": {"start": start, "end": end}}


# ---------------------------------------------------------------------------
# 1. The generator
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("start,end", [("2018-01-01", "2025-12-31"), ("2019-09-10", "2020-03-15"),
                                       ("2023-11-01", "2024-03-31"), ("2024-02-01", "2024-02-29")])
def test_generated_windows_are_disjoint_and_contiguous(start, end):
    ws = rpr._generate_monthly_windows(start, end, holdout_range=_FAR_SEAL)
    assert rp.windows_overlap(ws) is None
    for a, b in zip(ws, ws[1:]):
        assert (date.fromisoformat(a["test"]["end"]) + timedelta(days=1)
                == date.fromisoformat(b["test"]["start"]))
    assert ws[-1]["test"]["end"] == end


def test_each_tile_ends_on_its_months_last_day():
    ws = rpr._generate_monthly_windows("2023-12-01", "2024-03-31", holdout_range=_FAR_SEAL)
    assert [w["test"]["end"] for w in ws] == ["2023-12-31", "2024-01-31", "2024-02-29",
                                              "2024-03-31"]


# ---------------------------------------------------------------------------
# 2. The run_protocol pre-flight
# ---------------------------------------------------------------------------

def test_the_old_shared_day_form_is_refused():
    msg = rp.windows_overlap([_w("a", "2024-01-01", "2024-02-01"), _w("b", "2024-02-01", "2024-03-01")])
    assert msg and "2024-02-01" in msg and "LAST INCLUDED DAY" in msg


def test_overlap_is_found_whatever_the_listed_order():
    assert rp.windows_overlap([_w("b", "2024-02-01", "2024-02-29"),
                               _w("a", "2024-01-01", "2024-02-10")])


@pytest.mark.parametrize("windows", [
    [_w("a", "2024-01-01", "2024-01-31"), _w("b", "2024-02-01", "2024-02-29")],   # adjacent
    [_w("a", "2024-01-01", "2024-01-31"), _w("b", "2024-03-01", "2024-03-31")],   # a real gap
    [_w("a", "2024-01-01", "2024-01-31")],
    [],
])
def test_disjoint_windows_pass(windows):
    assert rp.windows_overlap(windows) is None


def test_run_protocol_refuses_an_overlapping_protocol_before_any_backtest(monkeypatch, tmp_path):
    calls = []
    monkeypatch.setattr(rp, "run_backtest", lambda *a, **kw: calls.append(a))
    monkeypatch.setattr(rp, "_RESULTS_ROOT", str(tmp_path / "results"))
    policy = tmp_path / "policy.yaml"
    policy.write_text('holdout_range: ["2030-01-01", "2030-06-30"]\nholdout_consumed_by: []\n',
                      encoding="utf-8")
    monkeypatch.setattr(rp, "_DATA_POLICY_PATH", policy)
    protocol = {"symbols": ["BTCUSDT"], "promotion": {
        "median_sharpe_gt": -999, "max_abs_drawdown_pct_lt": 999, "min_trade_count_gte": 0,
        "kill_median_sharpe_lt": -999999},
        "windows": [_w("a", "2022-01-01", "2022-02-01"), _w("b", "2022-02-01", "2022-03-01")]}
    (tmp_path / "protocol.json").write_text(json.dumps(protocol))
    (tmp_path / "config.json").write_text(json.dumps({"dummy": True}))
    monkeypatch.setattr(sys, "argv", ["run_protocol.py", str(tmp_path / "config.json"),
                                      str(tmp_path / "protocol.json"),
                                      "--out-dir", str(tmp_path / "out")])
    with pytest.raises(SystemExit) as exc:
        rp.main()
    assert exc.value.code == rp.EXIT_NO_DATA_TOUCHED
    assert calls == []


# ---------------------------------------------------------------------------
# 3. The committed protocols
# ---------------------------------------------------------------------------

def _tracked_protocols():
    out = subprocess.check_output(["git", "ls-files", "protocols/*.json"], cwd=_SR, text=True)
    return [f for f in out.split() if f]


_HAND_MADE = [f for f in _tracked_protocols() if "_generated" not in f]


def test_the_hand_made_protocols_were_all_found():
    assert len(_HAND_MADE) == 10


@pytest.mark.parametrize("path", _HAND_MADE)
def test_every_hand_made_protocol_passes_the_preflight(path):
    """Migrated by CUL-369: end = next start - 1 day. The tracked
    run_0xx_generated.json files are records of past runs and keep their old
    (shared-day) windows -- the pre-flight refuses re-running them as-is."""
    windows = json.loads((_SR / path).read_text(encoding="utf-8"))["windows"]
    assert rp.windows_overlap(windows) is None


# ---------------------------------------------------------------------------
# 4. The data gate measures through the end day
# ---------------------------------------------------------------------------

def _hourly(first: str, last: str) -> pd.DataFrame:
    return pd.DataFrame({"timestamp": pd.date_range(first, last, freq="h")})


def test_a_date_only_end_is_measured_to_the_next_midnight():
    assert dag._measure_end("2024-01-31") == datetime(2024, 2, 1)
    assert dag._measure_end("2024-01-31 12:00:00") == datetime(2024, 1, 31, 12)


def test_a_full_end_day_is_fully_available():
    df = _hourly("2024-01-01 00:00", "2024-01-31 23:00")
    frac = dag._missing_fraction(df, datetime(2024, 1, 1), dag._measure_end("2024-01-31"), 3600)
    assert frac == 0.0


def test_a_missing_end_day_is_now_seen():
    """Before CUL-369 the gate stopped at the end day's midnight, so a whole
    missing last day read as fully available."""
    df = _hourly("2024-01-01 00:00", "2024-01-30 23:00")
    frac = dag._missing_fraction(df, datetime(2024, 1, 1), dag._measure_end("2024-01-31"), 3600)
    assert frac == pytest.approx(24 / (31 * 24))  # the 24 hourly bars of the end day
    old = dag._missing_fraction(df, datetime(2024, 1, 1), datetime(2024, 1, 31), 3600)
    assert old == 0.0


def test_disjoint_windows_listed_out_of_order_pass():
    """Compared in start order: a protocol listing windows newest-first is not
    falsely refused."""
    assert rp.windows_overlap([_w("b", "2024-02-01", "2024-02-29"),
                               _w("a", "2024-01-01", "2024-01-31")]) is None


class _FakeDM:
    """Stands in for DataManager: returns a fixed hourly frame, touches no data."""
    df = None

    def __init__(self, *a, **kw):
        self.fetch_interval_seconds = 3600

    def fetch_historical_data(self, *a, **kw):
        return self.df


def test_the_price_check_looks_at_the_end_day(monkeypatch):
    _FakeDM.df = _hourly("2024-01-01 00:00", "2024-01-30 23:00")  # 2024-01-31 missing
    monkeypatch.setattr(dag, "DataManager", _FakeDM)
    res = dag.check_price_window("BTCUSDT", "binance", "1h", "2024-01-01", "2024-01-31",
                                 fetch_interval_seconds=None)
    assert res["missing_fraction"] == pytest.approx(1 / 31)
    _FakeDM.df = _hourly("2024-01-01 00:00", "2024-01-31 23:00")
    res = dag.check_price_window("BTCUSDT", "binance", "1h", "2024-01-01", "2024-01-31",
                                 fetch_interval_seconds=None)
    assert res["outcome"] == "validate"


def test_the_venue_less_aux_check_looks_at_the_end_day(monkeypatch):
    feed = sorted(dag._VENUE_LESS_FEED_NAMES)[0]

    class _Fetcher:
        interval_seconds = 86400

        def get_data(self):  # daily rows, the end day 2024-01-31 missing
            return pd.DataFrame({"timestamp": pd.date_range("2024-01-01", "2024-01-30", freq="D")})

    monkeypatch.setitem(dag.FEED_REGISTRY, feed, lambda *a, **kw: _Fetcher())
    res = dag.check_aux_feed_window(feed, "binance", [], "2024-01-01", "2024-01-31")
    assert res["missing_fraction"] == pytest.approx(1 / 31)


# ---------------------------------------------------------------------------
# 5. Review fixes
# ---------------------------------------------------------------------------

import run_campaign as camp  # noqa: E402

from test_e061_c1_4_5_pauses_preflight import RUN, _NON_GENERIC, _root, _scaffold  # noqa: E402

_OLD_FORM = [_w("2022-01", "2022-01-01", "2022-02-01"), _w("2022-02", "2022-02-01", "2022-03-01")]


def test_an_end_on_the_first_of_a_month_is_refused():
    """Finding 1: it would be a one-day last window (ungradable by the chain)."""
    with pytest.raises(ValueError, match="LAST INCLUDED DAY"):
        rpr._generate_monthly_windows("2022-01-01", "2022-03-01", holdout_range=_FAR_SEAL)


def test_a_sweep_to_the_seals_first_day_still_reports_the_breach_first():
    with pytest.raises(rpr.HoldoutBoundaryBreach):
        rpr._generate_monthly_windows("2022-01-01", "2022-03-01",
                                      holdout_range=("2022-03-01", "2022-06-30"))


def test_a_midnight_timestamp_end_is_a_whole_day_like_the_engine():
    assert dag._measure_end(pd.Timestamp("2024-01-31")) == datetime(2024, 2, 1)
    assert dag._measure_end("2024-01-31T00:00:00") == datetime(2024, 2, 1)


def _constraints():
    return {"protocol": {"symbols": ["BTCUSDT"], "timeframe": "1h", "start": "2022-01-01",
                         "end": "2022-02-28", "promotion": _NON_GENERIC}}


def _old_generated_file():
    path = _root() / "protocols" / f"{RUN}_generated.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps({"symbols": ["BTCUSDT"], "timeframe": "1h", "windows": _OLD_FORM,
                                "promotion": _NON_GENERIC}), encoding="utf-8")
    return path


def test_preflight_names_the_right_remedy_before_any_spend():
    """Finding 2 (run_063's case): pre_registration did not change, the
    generator did -- delete the file, it regenerates."""
    run_dir = _scaffold(constraints=_constraints())
    _old_generated_file()
    refusal, regen = camp._generated_protocol_plan(run_dir, RUN, _constraints()["protocol"], {},
                                                   promotion_retired=False)
    assert regen is None and "D-058" in refusal and "Delete" in refusal
    assert "Restore pre_registration.yaml" not in refusal


def test_preflight_refuses_resuming_a_spent_run_on_an_old_protocol():
    """Finding 2 (run_061's case): data spent, never regenerated, cannot resume."""
    run_dir = _scaffold(constraints=_constraints())
    _old_generated_file()
    state = {"stage_attempts": {"protocol_execution": 1}}
    refusal, regen = camp._generated_protocol_plan(run_dir, RUN, _constraints()["protocol"], state,
                                                   promotion_retired=False)
    assert regen is None and "cannot resume" in refusal and "new run id" in refusal


def test_preflight_refuses_a_pinned_old_form_protocol():
    """Finding 3: refused at launch, not at 5a after 1a/1b/2 spent."""
    (_root() / "protocols").mkdir(exist_ok=True)
    (_root() / "protocols" / "old_pin.json").write_text(json.dumps(
        {"symbols": ["BTCUSDT"], "timeframe": "1h", "windows": _OLD_FORM,
         "promotion": _NON_GENERIC}), encoding="utf-8")
    run_dir = _scaffold(constraints={"protocol_ref": "protocols/old_pin.json"})
    refusal = camp._protocol_preflight_refusal(run_dir, RUN, promotion_retired=False)
    assert refusal and "CUL-369" in refusal and "old_pin.json" in refusal


def test_preflight_passes_a_new_form_generated_protocol():
    run_dir = _scaffold(constraints=_constraints())
    rpr._ensure_protocol_from_constraints(run_dir, RUN, _constraints())
    assert camp._generated_protocol_plan(run_dir, RUN, _constraints()["protocol"], {},
                                         promotion_retired=False) == (None, None)


def test_preflight_refuses_an_old_form_protocol_named_by_run_context():
    """Finding 3, third branch: a forced_diagnostic run_context naming a
    shared-day protocol is refused at launch too."""
    (_root() / "protocols").mkdir(exist_ok=True)
    (_root() / "protocols" / "old_diag.json").write_text(json.dumps(
        {"symbols": ["BTCUSDT"], "timeframe": "1h", "windows": _OLD_FORM,
         "promotion": _NON_GENERIC}), encoding="utf-8")
    run_dir = _scaffold(constraints={})
    rpr.save_yaml(run_dir / "artifacts" / "run_context.yaml",
                  {"run_type": "forced_diagnostic", "protocol": "old_diag.json"})
    refusal = camp._protocol_preflight_refusal(run_dir, RUN, promotion_retired=False)
    assert refusal and "CUL-369" in refusal and "old_diag.json" in refusal
