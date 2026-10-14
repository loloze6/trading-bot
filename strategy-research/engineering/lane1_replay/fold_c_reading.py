"""Lane 1's fold-C reading (D-126): every figure of the D-row, recomputed read-only.

Run from the operator checkout's strategy-research/ (the runs live there):
    ../venv/Scripts/python.exe <this file>
Reads runs/<run>/artifacts/ and the trial ledger; writes nothing.

Prints, per run (run_090 SMA 50, run_092 SMA 100 base, run_093 SMA 200, all fold C; and
run_091 SMA 50 fold D): the stored branch-3 rows (profit_bars_evaluation.yaml), the deflated
Sharpe recomputed on the current ledger (D-124), the chained drawdown's peak and trough and
each window's worst drop inside the window; then D-108's two inputs: whole-test Sharpe > 0
on at least 2 of the 3 fold-C runs, and the base run's curve-based gross/cost >= 2
(tools/curve_cost_ratio.py on run_092).
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

SR = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(SR / "tools"), str(SR / "workflow")]
import curve_cost_ratio as ccr  # noqa: E402
import run_phase1_research as rpr  # noqa: E402

ROOT = Path.cwd()
rpr.ROOT = ROOT
rpr.CAMPAIGN_STATE_PATH = ROOT / "campaign_record" / "campaign_state.yaml"
rpr.TRIAL_SHARPE_BASIS_OVERLAY_PATH = ROOT / "trial_sharpe_basis_recompute.yaml"
pwt = rpr._portfolio_whole_test_module()
RUNS = (("run_090", "SMA 50", "C"), ("run_092", "SMA 100 (base)", "C"),
        ("run_093", "SMA 200", "C"), ("run_091", "SMA 50", "D"))


def _window_drops(run_dir: Path, pr: dict) -> dict:
    chain, _coins = rpr._whole_test_chain(run_dir, pr)
    levels = dict(chain["daily_levels"])
    bounds = rpr._v2_protocol_window_bounds(pr, rpr._pd.load_windows(run_dir, pr)[0])
    out = {}
    for w in sorted(bounds):
        a, b = (str(x)[:10] for x in bounds[w])
        seg = [v for d, v in sorted(levels.items()) if a <= d.isoformat() <= b]
        peak, worst = seg[0], 0.0
        for v in seg:
            peak = max(peak, v)
            worst = min(worst, v / peak - 1.0)
        out[w] = round(100.0 * worst, 1)
    return out


def main() -> None:
    wctx = rpr._whole_test_dsr_context()
    sharpes = {}
    for run, signal, fold in RUNS:
        rd = ROOT / "runs" / run
        pr = yaml.safe_load((rd / "artifacts" / "protocol_result.yaml").read_text(encoding="utf-8"))
        ev = yaml.safe_load((rd / "artifacts" / "profit_bars_evaluation.yaml").read_text(encoding="utf-8"))
        print(f"\n{run} ({signal}, fold {fold}) stored evaluation generated_at {ev['generated_at']}")
        for row in ev["variants"][run]["bars"]:
            print(f"  {row['name']}: threshold {row['threshold']}, actual {row['actual']}, {row['result']}")
            if row["name"] == "sharpe_min":
                sharpes[run] = row["actual"]
            if row["name"] == "max_drawdown_pct_max":
                print(f"    peak {row['detail']['peak_ts']} -> trough {row['detail']['trough_ts']}")
        dsr = rpr._whole_test_dsr_candidate(wctx, rd, pr, run, 10)
        print(f"  deflated Sharpe on the current ledger: {dsr.get('dsr')} (status {dsr.get('status')}, "
              f"K {dsr.get('K')}, N {dsr.get('N')})")
        print(f"  worst drop inside each window (%): {_window_drops(rd, pr)}")
    fold_c = [r for r, _s, f in RUNS if f == "C"]
    n_pos = sum(1 for r in fold_c if sharpes[r] > 0)
    cost = ccr.curve_gross_to_cost(list(ccr.load_run_accounts(ROOT / "runs" / "run_092").values()))
    print(f"\nD-108 on fold C: whole-test Sharpe > 0 on {n_pos} of 3 runs (rule: at least 2); "
          f"run_092 curve-based gross/cost {cost['ratio']:.2f} (gross {cost['gross_points']:.2f}, "
          f"costs {cost['cost_points']:.2f} points, {cost['n_accounts']} accounts; rule: >= 2)")
    print("D-108 outcome:", "CONTINUE" if n_pos >= 2 and cost["ratio"] >= 2 else "FAIL")


if __name__ == "__main__":
    main()
