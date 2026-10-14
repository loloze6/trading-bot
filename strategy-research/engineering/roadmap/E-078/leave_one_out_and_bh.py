"""E-078 one-time read-only numbers (ruling 2 item (2)): per run, the whole-test Sharpe,
each leave-one-block-out whole-test Sharpe, and the basket buy-and-hold Sharpe.

Fragility condition (stated before running, README.md): any leave-one-block-out Sharpe <= 0.

Read-only: reads runs/<run>/artifacts/ and config/profitability_bars.yaml; writes nothing.
Run from strategy-research/: python engineering/roadmap/E-078/leave_one_out_and_bh.py run_084 ...
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

SR = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(SR / "tools"), str(SR / "workflow")]
import run_phase1_research as rpr  # noqa: E402

ROOT = Path.cwd()  # the checkout whose runs are read (cwd = strategy-research/)
rpr.ROOT = ROOT
pwt = rpr._portfolio_whole_test_module()


def _bars() -> dict:
    doc = yaml.safe_load((ROOT / "config" / "profitability_bars.yaml").read_text(encoding="utf-8"))
    return doc.get("bars", doc)


def numbers(run_id: str) -> dict:
    rd = ROOT / "runs" / run_id
    pr = yaml.safe_load((rd / "artifacts" / "protocol_result.yaml").read_text(encoding="utf-8"))
    chain, _coins = rpr._whole_test_chain(rd, pr)
    returns = chain["daily_returns"]
    # D-127: the one definition the branch-3 bar uses (a block = a 4-month calendar slice,
    # which on the folds' windows is the window itself)
    loo = pwt.leave_one_block_out_sharpes(returns)
    bh = rpr._whole_test_profit_metrics(rd, pr, _bars())["buy_and_hold_sharpe_excess_min"]["detail"]
    return {"sharpe": pwt.whole_test_sharpe(returns), "loo": loo,
            "bh_sharpe": bh["buy_and_hold_sharpe"],
            "fragile": any(s <= 0 for s in loo.values())}


def main(run_ids: list) -> None:
    print("| Run | Whole-test Sharpe | Leave-one-block-out Sharpe (window left out) | Min | "
          "Fragile (any <= 0) | Basket buy-and-hold Sharpe |")
    print("|---|---|---|---|---|---|")
    for run_id in run_ids:
        n = numbers(run_id)
        loo = ", ".join(f"{w}: {s:.2f}" for w, s in n["loo"].items())
        print(f"| {run_id} | {n['sharpe']:.2f} | {loo} | {min(n['loo'].values()):.2f} | "
              f"{'yes' if n['fragile'] else 'no'} | {n['bh_sharpe']:.2f} |")


if __name__ == "__main__":
    main(sys.argv[1:])
