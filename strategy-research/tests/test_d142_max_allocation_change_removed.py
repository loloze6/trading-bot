"""D-142: the max_allocation_change risk control (|delta| > 4.0 refused) is removed.

It also refused reductions and flips back toward the target: run_096's
asset_XRPUSDT variant, window 2018-09, held -15.69x its equity on 2018-09-20 and
the move back to the -2.0 target (+13.69) was refused; equity was -591 the next
day. The control never fired in lane 1.

Fast: the RiskManager on the committed controls approves that +13.69 move.
Slow (needs the kraken daily caches and fear_greed_daily.csv, never in CI): two
recorded windows replayed through tools/run_protocol.py, exactly as
protocol_execution calls it:
  - run_084 BTCUSD 2018-05 (lane 1): every field of portfolio_states.csv is
    identical to the record, except the removed control's debug column;
  - run_096 asset_XRPUSDT 2018-09: the 2018-09-20 reduction now executes and the
    equity stays positive over the window.

Fixtures (tests/fixtures/d142/): each run's config snapshot, its protocol cut to
the one symbol and window (holdout block dropped: run_protocol then takes the
data policy's start), and the recorded portfolio_states.csv.
"""
import csv
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest
from _cache_guard import requires_cache

ROOT = Path(__file__).resolve().parent.parent
TBOT_ROOT = ROOT.parent / "trading-bot"
FIXTURES = ROOT / "tests" / "fixtures" / "d142"
LOCAL = TBOT_ROOT / "local_data"
GONE = "debug_approve_allocation_change.controls.max_allocation_change.passed"

if str(TBOT_ROOT) not in sys.path:
    sys.path.insert(0, str(TBOT_ROOT))


def test_committed_controls_approve_a_large_reduction():
    from risk.risk_manager import RiskManager

    controls = json.loads((TBOT_ROOT / "config.json").read_text())["risk_management"]["controls"]
    assert "max_allocation_change" not in controls
    assert not hasattr(RiskManager, "_ctrl_max_allocation_change")
    data = pd.DataFrame({"timestamp": [pd.Timestamp("2018-09-20")]})
    approved, debug = RiskManager(controls).approve_allocation_change("XRPUSD", 13.688841, data)
    assert approved is True
    assert set(debug["controls"]) == {"min_allocation_change"}


def _replay(case: str, tmp_path: Path) -> list[dict]:
    src = FIXTURES / case
    out = tmp_path / "run"
    cmd = [sys.executable, str(ROOT / "tools" / "run_protocol.py"),
           str(src / "strategy_config.json"), str(src / "protocol.json"),
           "--legacy-verdict-retired", "--out-dir", str(out)]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-2000:]
    (run_dir,) = list((out / "results").iterdir())
    return _rows(run_dir / "portfolio_states.csv")


def _rows(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


@pytest.mark.slow
@requires_cache(LOCAL / "kraken_BTCUSD_1d.csv", LOCAL / "fear_greed_daily.csv")
def test_lane1_window_replays_identically_but_for_the_removed_column(tmp_path):
    recorded = _rows(FIXTURES / "run_084_BTCUSD_2018-05" / "portfolio_states_recorded.csv")
    new = _replay("run_084_BTCUSD_2018-05", tmp_path)
    # The gate never fired in this window ...
    assert {r[GONE] for r in recorded} <= {"True", ""}
    # ... so removing it changes nothing but its own debug column.
    assert GONE not in new[0]
    assert [{k: v for k, v in r.items() if k != GONE} for r in recorded] == new


@pytest.mark.slow
@requires_cache(LOCAL / "kraken_XRPUSD_1d.csv", LOCAL / "fear_greed_daily.csv")
def test_run_096_xrp_reduction_on_2018_09_20_executes(tmp_path):
    recorded = _rows(FIXTURES / "run_096_asset_XRPUSDT_2018-09" / "portfolio_states_recorded.csv")
    new = _replay("run_096_asset_XRPUSDT_2018-09", tmp_path)
    old_day = next(r for r in recorded if r["timestamp"].startswith("2018-09-20"))
    new_day = next(r for r in new if r["timestamp"].startswith("2018-09-20"))
    # Recorded: the move back to target was refused by the max control alone.
    assert old_day[GONE] == "False" and old_day["approved_rebalance"] == "False"
    assert min(float(r["total_portfolio_value"]) for r in recorded) < 0
    # Now: the same bar asks for the same move and it executes.
    assert float(new_day["previous_allocation"]) == pytest.approx(-15.688841, abs=1e-5)
    assert float(new_day["allocation_change"]) == pytest.approx(13.688841, abs=1e-5)
    assert new_day["approved_rebalance"] == "True"
    assert new_day["succcess_execute_portfolio_rebalance"] == "True"
    assert float(new_day["postRebalance_current_allocation"]) == pytest.approx(-2.0, abs=0.05)
    assert min(float(r["total_portfolio_value"]) for r in new) > 0
