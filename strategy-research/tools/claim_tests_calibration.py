"""E-068 slice 1 (CUL-386): calibration gate for tools/claim_tests.py.

Pre-registered in engineering/roadmap/E-068/regrade_specs/AMENDMENT_1.md
(section B) and AMENDMENT_2.md (section B3) before it was run. The claim tool
must not find an edge where there is none: on simulated prices with NO edge,
using the real signals, the share of one-sided p < 0.05 must be about 0.05 in
each direction. Pass = within [0.025, 0.075] for every cell and every horizon,
400 simulations per cell. Both directions are read from the same simulations
(p_value and p_value_opposite).

Signals: DonchianBreakoutComponent(period=20) on daily bars and
KeltnerBreakoutComponent(20, 20, 2.0) on hourly bars, through claim_tests.SIGNALS
(the vectorized copies, proven equal to update() by a test). Engine clip +-20.

Price models (zero mean, no edge): iid normal log returns; GARCH(1,1)
volatility clustering (alpha 0.08, beta 0.90). Warm-up comes from the same
simulated history.

Synthetic data only; no market data is read.
    python tools/claim_tests_calibration.py --n-sims 400 --out <file.yaml>
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import claim_tests as ct  # noqa: E402

SEED = 20261003
GATE = (0.025, 0.075)
ALPHA = 0.05
N_NULL = 199               # fake worlds per simulation (amendment 2, B3)
T0 = 1577836800            # 2020-01-01 UTC, synthetic timestamps only
DONCHIAN = {"class": "DonchianBreakoutComponent", "params": {"period": 20, "scaling_factor": 20.0}}
KELTNER = {"class": "KeltnerBreakoutComponent",
           "params": {"ema_period": 20, "atr_period": 20, "atr_multiplier": 2.0,
                      "scaling_factor": 20.0}}
DAILY = {"n": 120, "warmup": ct.WARMUP_BARS["daily"], "step": 86400, "sd": 0.035, "windows": 6}
HOURLY = {"n": 2900, "warmup": ct.WARMUP_BARS["hourly"], "step": 3600, "sd": 0.007, "windows": 6}


def simulate_returns(rng, n: int, sd: float, model: str) -> np.ndarray:
    if model == "iid":
        return rng.normal(0.0, sd, n)
    a, b = 0.08, 0.90
    omega = sd * sd * (1 - a - b)
    r = np.empty(n)
    s2 = sd * sd
    for t in range(n):
        r[t] = rng.normal(0.0, np.sqrt(s2))
        s2 = omega + a * r[t] ** 2 + b * s2
    return r


def simulate_windows(rng, cfg: dict, model: str, signal: dict) -> list:
    out = []
    for wi in range(cfg["windows"]):
        n, wu = cfg["n"], cfg["warmup"]
        m = n + wu
        close = 100.0 * np.exp(np.cumsum(simulate_returns(rng, m, cfg["sd"], model)))
        opn = np.r_[100.0, close[:-1]]
        wick = np.abs(rng.normal(0.0, cfg["sd"] * 0.5, (2, m)))
        high = np.maximum(opn, close) * np.exp(wick[0])
        low = np.minimum(opn, close) * np.exp(-wick[1])
        fc = ct.compute_signal(signal, high, low, close)
        ts_all = (T0 + (wi * (m + 10) + np.arange(m)) * cfg["step"]).astype(np.int64)
        warm = {"ts": ts_all[:wu], "high": high[:wu], "low": low[:wu], "close": close[:wu]}
        out.append(ct.Window("SIM", f"w{wi}", ts_all[wu:], close[wu:], fc[wu:],
                             np.array(["unknown"] * n, dtype=object), cfg["step"],
                             high=high[wu:], low=low[wu:], warm=warm, signal=signal))
    return out


def cells() -> list[dict]:
    """Each cell yields two rows: its direction and the opposite one."""
    sig = {"method": ct.SIGNIFICANCE_METHOD, "n_resamples": N_NULL, "seed": 1}
    out = []
    for model in ("iid", "garch"):
        for op, value in ((">=", 12), ("<=", -12)):
            out.append({"name": f"daily_donchian_{model}_fc{op}{value}",
                        "cfg": DAILY, "model": model, "signal": DONCHIAN,
                        "spec": ct.TestSpec(
                            selector={"kind": "event", "field": "forecast", "op": op,
                                      "value": value},
                            outcome={"kind": "fwd_return", "horizons": [1, 2, 3, 4, 5]},
                            baseline={"kind": "complement"}, statistic="mean_diff",
                            direction="greater", floor={"min_events": 1},
                            significance=dict(sig))})
        out.append({"name": f"hourly_keltner_{model}_rank_ic",
                    "cfg": HOURLY, "model": model, "signal": KELTNER,
                    "spec": ct.TestSpec(
                        selector={"kind": "all"},
                        outcome={"kind": "fwd_return", "horizons": [72, 168, 336]},
                        baseline=None, statistic="rank_ic", direction="greater",
                        floor={"min_events": 1}, significance=dict(sig))})
    return out


def run_calibration(n_sims: int, seed: int = SEED, only: str | None = None) -> dict:
    rows = []
    for i, cell in enumerate(cells()):
        if only and only not in cell["name"]:
            continue
        rng = np.random.default_rng([seed, i])
        hs = cell["spec"].outcome["horizons"]
        rej = {d: {h: 0 for h in hs} for d in ("greater", "less")}
        undefined = {h: 0 for h in hs}
        for k in range(n_sims):
            spec = ct.TestSpec(**{**cell["spec"].__dict__,
                                  "significance": {**cell["spec"].significance, "seed": k}})
            res = ct.run_test(simulate_windows(rng, cell["cfg"], cell["model"], cell["signal"]),
                              spec)
            for h in hs:
                hr = res["horizons"][h]
                if hr["p_value"] is None:
                    undefined[h] += 1
                    continue
                rej["greater"][h] += hr["p_value"] < ALPHA
                rej["less"][h] += hr["p_value_opposite"] < ALPHA
        for d in ("greater", "less"):
            share = {h: rej[d][h] / n_sims for h in hs}
            rows.append({"cell": f"{cell['name']}_{d}", "n_sims": n_sims, "n_null": N_NULL,
                         "share_p_below_0_05": share, "undefined": undefined,
                         "pass": all(GATE[0] <= v <= GATE[1] for v in share.values())})
    return {"gate": {"alpha": ALPHA, "pass_range": list(GATE)},
            "method": ct.SIGNIFICANCE_METHOD, "seed": seed, "cells": rows,
            "all_pass": all(r["pass"] for r in rows)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="claim_tests calibration gate")
    ap.add_argument("--n-sims", type=int, default=400)
    ap.add_argument("--only", default=None)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    import yaml
    res = run_calibration(a.n_sims, only=a.only)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        yaml.safe_dump(res, f, sort_keys=False)
    for r in res["cells"]:
        print(f"{'PASS' if r['pass'] else 'FAIL'}  {r['cell']}  "
              + " ".join(f"h{h}={v:.3f}" for h, v in r["share_p_below_0_05"].items()), flush=True)
    print("ALL PASS" if res["all_pass"] else "GATE FAILED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
