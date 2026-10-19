"""PR-B (analyst tools, 2026-10-19): the dollar-basis reconciliation of window_economics.

Operator decision 2026-10-19: gross, fees and net are dollar sums over the window divided by the
account equity at the window's first bar (V0 = `total_portfolio_value` of the first row of
bars.csv by timestamp); and two identities must hold in every window:

  (a) gross_pct - fees_pct == net_pct                       (abs tol SUM_TOL = 2e-6 pp: the tool
                                                              rounds each of the three to 8
                                                              significant digits, up to 5e-7 pp
                                                              each below 100, so the identity holds
                                                              on the rounded numbers to 1.5e-6)
  (b) net_pct == 100 * (E_end - V0) / V0, V0 = `total_portfolio_value` of the first row (the
      account before the window's first action), E_end = `postRebalance_total_value` of the
      last row (the account after the window's last action)   (tol RECON_TOL below)
      Why two columns: `total_portfolio_value` is the bar's account BEFORE its rebalance, so the
      last row's value misses the last bar's closing rebalance and fee; `postRebalance_total_value`
      is the account AFTER it. Using the last row's `total_portfolio_value` misses by up to
      0.15 percentage points on run_097; the post-action column reconciles to rounding.

Two tests of the same two assertions:
  - synthetic twin: always runs (a hand-made window whose bars.csv equity is consistent with its
    trades);
  - run copy: reads the base variant of a saved run (env WINDOW_ECONOMICS_RUN_COPY, default the
    analyst smoke copy of run_097 on this machine); skipped when the folder is absent (runs/ is
    not in git, CI has no copy). Reads only bars.csv and trades.json of each window (the window
    folders are resolved as the stored-object code does: portfolio_daily.find_window_equity_file
    over the graded results of the variant's protocol_result.yaml, then the parent folder).

Why this cannot leak: post-run accounting over a finished run's own files; nothing here feeds a
decision. Window labels and dates of a real run are never written in this file or in its
messages: windows are reported by index.
"""
import json
import os
import sys
from pathlib import Path

import pandas as pd
import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import window_economics as we  # noqa: E402
import portfolio_daily as _pd  # noqa: E402
from test_window_economics import lot  # noqa: E402

DEFAULT_RUN_COPY = r"C:\Users\alauz\AppData\Local\Temp\analyst_smoke\run_097"
ENV_RUN_COPY = "WINDOW_ECONOMICS_RUN_COPY"

SUM_TOL = 2e-6
RECON_TOL = 1e-5   # percentage points of V0: the tool rounds each *_pct to 8 significant digits
#                    (about 5e-7 pp at 43%); the measured max difference is below it.


def equity_change_pct(bars_csv) -> float:
    """100 * (E_end - V0) / V0 over the rows of bars.csv sorted by timestamp: V0 = the first
    row's total_portfolio_value (pre-action: the account at the window's start, the value
    window_economics divides by), E_end = the last row's postRebalance_total_value (post-action:
    the account after the window's last action). Every row counts, NOT_READY ones included."""
    df = pd.read_csv(bars_csv, usecols=["timestamp", "total_portfolio_value",
                                        "postRebalance_total_value"])
    df = df.assign(_t=pd.to_datetime(df["timestamp"], utc=True)).sort_values("_t")
    v0 = float(df["total_portfolio_value"].iloc[0])
    end = float(df["postRebalance_total_value"].iloc[-1])
    return 100.0 * (end - v0) / v0


def write_reconciled_window(folder: Path, rows, trades):
    """Like test_window_economics.write_window, plus a postRebalance_total_value column.
    rows: (regime, total_portfolio_value, postRebalance_total_value, previous_allocation,
    postRebalance_current_allocation), one per hourly bar from 2020-01-01 00:00."""
    folder.mkdir(parents=True, exist_ok=True)
    lines = ["timestamp,regime,total_portfolio_value,postRebalance_total_value,"
             "previous_allocation,postRebalance_current_allocation"]
    for i, (regime, tpv, post, prev, alloc) in enumerate(rows):
        lines.append(f"2020-01-01 {i:02d}:00:00,{regime},{tpv},{post},{prev},{alloc}")
    (folder / "bars.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (folder / "trades.json").write_text(json.dumps(trades), encoding="utf-8")


def check_cells(windows, tol_recon):
    """Per window (symbol, label, folder): (index, gross, fees, net, equity change). Asserts (a)
    and (b); messages name the window by index only."""
    out = we.window_economics(windows)["windows"]
    assert len(windows) >= 1
    rows = []
    for i, (sym, win, folder) in enumerate(windows):
        c = out[f"{sym}/{win}"]
        gross, fees, net = c["gross_pct"], c["fees_pct"], c["net_pct"]
        eq = equity_change_pct(Path(folder) / "bars.csv")
        assert abs((gross - fees) - net) <= SUM_TOL, (
            f"window #{i}: gross {gross} - fees {fees} != net {net}")
        assert abs(net - eq) <= tol_recon, (
            f"window #{i}: net_pct {net} vs equity change {eq} (diff {net - eq})")
        rows.append((i, gross, fees, net, eq))
    return rows


# ---------------------------------------------------------------------------
# synthetic twin (always runs)
# ---------------------------------------------------------------------------

def test_synthetic_gross_minus_fees_is_net_and_net_is_the_equity_change(tmp_path):
    # V0 = 1000 (a NOT_READY first row); the account ends at 1037 = 1000 + the lots' net 37
    # (gross 40, fees 3): lots 30/-10/20 gross, 1/.5/1.5 fees. The last bar's pre-action value
    # (1030) is deliberately NOT the end: its closing rebalance adds 7, post-action 1037.
    # A second window on a 2000 account with a loss: lots -50/20 gross, 2/1 fees -> net -33
    # -> ends at 1967 (last bar pre-action 1975).
    write_reconciled_window(
        tmp_path / "a",
        [("NOT_READY", 1000, 1000, 0, 0), ("trend", 1000, 1000, 0.0, 0.5),
         ("trend", 1010, 1010, 0.5, 0.5), ("trend", 1020, 1020, 0.5, 0.0),
         ("trend", 1020, 1020, 0.0, -0.4), ("trend", 1030, 1037, -0.4, 0.0)],
        [lot(30.0, 1.0, 29.0, 120.0), lot(-10.0, 0.5, -10.5, 60.0), lot(20.0, 1.5, 18.5, 300.0)])
    write_reconciled_window(
        tmp_path / "b",
        [("trend", 2000, 2000, 0.0, 0.3), ("trend", 1990, 1990, 0.3, 0.3),
         ("trend", 1975, 1967, 0.3, 0.0)],
        [lot(-50.0, 2.0, -52.0, 60.0), lot(20.0, 1.0, 19.0, 120.0)])
    wins = [("AAA", "w0", tmp_path / "a"), ("BBB", "w1", tmp_path / "b")]
    rows = check_cells(wins, RECON_TOL)
    (_, g0, f0, n0, e0), (_, g1, f1, n1, e1) = rows
    assert (g0, f0, n0, e0) == pytest.approx((4.0, 0.3, 3.7, 3.7), abs=1e-9)
    assert (g1, f1, n1, e1) == pytest.approx((-1.5, 0.15, -1.65, -1.65), abs=1e-9)


def test_synthetic_twin_catches_an_account_that_does_not_reconcile(tmp_path):
    # a last-bar post-action equity that is not V0 + net (1030 against 1009): the check must fail
    write_reconciled_window(
        tmp_path / "x",
        [("trend", 1000, 1000, 0.0, 0.5), ("trend", 1010, 1010, 0.5, 0.0),
         ("trend", 1030, 1030, 0.0, 0.0)],
        [lot(10.0, 1.0, 9.0, 60.0)])
    with pytest.raises(AssertionError, match="window #0: net_pct"):
        check_cells([("X", "w", tmp_path / "x")], RECON_TOL)


# ---------------------------------------------------------------------------
# the run copy (skipped without it)
# ---------------------------------------------------------------------------

def _run_copy_windows():
    root = Path(os.environ.get(ENV_RUN_COPY) or DEFAULT_RUN_COPY)
    if not root.is_dir():
        pytest.skip(f"no run copy at {root} (set {ENV_RUN_COPY}; runs/ is not in git, "
                    "CI has no copy)")
    pr_path = root / "artifacts" / "variants" / "base" / "protocol_result.yaml"
    if not pr_path.is_file():
        pytest.skip(f"run copy at {root} has no base variant protocol_result.yaml")
    pr = yaml.safe_load(pr_path.read_text(encoding="utf-8")) or {}
    wins = []
    for r in pr.get("results") or []:
        equity = _pd.find_window_equity_file(root, r["run_id"])
        assert equity is not None, "a graded window of the copy has no folder"
        wins.append((str(r["symbol"]), str(r["window"]), Path(equity).parent))
    return wins


def test_run_copy_gross_minus_fees_is_net_and_net_is_the_equity_change(capsys):
    """net_pct (dollar basis, rounded by the tool to 8 significant digits) against the equity
    change from bars.csv (first-row total_portfolio_value to last-row postRebalance_total_value).
    RECON_TOL = 1e-5 percentage points covers that rounding; it was not widened to pass a
    window (measured max difference on run_097 is ~1e-6 pp)."""
    wins = _run_copy_windows()
    assert len(wins) >= 1
    rows = check_cells(wins, RECON_TOL)
    with capsys.disabled():
        print("\nidx  gross_pct  fees_pct  net_pct  equity_change_pct  diff")
        for i, g, f, n, e in rows:
            print(f"{i:>3}  {g:.8g}  {f:.8g}  {n:.8g}  {e:.8g}  {n - e:.3e}")
        print(f"max |net - equity change| over {len(rows)} windows: "
              f"{max(abs(n - e) for _, _, _, n, e in rows):.3e}")
