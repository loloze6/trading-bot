"""E-068 slice 1 (CUL-386): calibration gate for tools/claim_tests.py.

Pre-registered in engineering/roadmap/E-068/regrade_specs/AMENDMENT_3.md,
section 5, before it was run. The claim tool must not find an edge where there
is none. On simulated prices with NO edge, using the real signal, the share of
one-sided p < 0.05 must be about 0.05 in each direction.

  Signal   DonchianBreakoutComponent(period=20), daily, via claim_tests.SIGNALS
           (vectorized copy, proven equal to update() by a test); clip +-20.
  Layout   6 contiguous windows x 120 daily bars (as run_065's windows abut),
           + 30 warm-up bars from the same simulated path.
  Prices   zero mean, no edge: `iid` normal (sd 0.035); `switching` two-state
           volatility (calm sd 0.02, wild sd 0.06, switch prob 0.01 per bar,
           ~100-bar spells). Intrabar high/low scale with the bar's own sd.
  Cells    model x side (forecast >= 12, forecast <= -12) x direction
           (claimed, opposite), horizons 1-5; both directions come from the
           same simulations (p_value and p_value_opposite).
  Methods  a851a_episode_v1 (existing A8.5.1a, its own 2000 resamples) and
           block_permutation_v1 (N = 199 fakes per simulation).
  Pass     per row: undefined p in <= 5% of simulations, AND among defined p
           the share below 0.05 within [0.025, 0.075] at every horizon. A
           method passes if all 8 rows pass. Undefined p are counted and
           reported, never hidden as "no rejection".

Each (method, model, side) cell runs as its own job and writes its own file:
    python tools/claim_tests_calibration.py cell --method M --model X --side S --out F
    python tools/claim_tests_calibration.py summarize --method M --out F CELL_FILES...
Synthetic data only; no market data is read.
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
MAX_UNDEFINED = 0.05
ALPHA = 0.05
N_SIMS = 400
N_NULL = 199
T0 = 1577836800            # 2020-01-01 UTC, synthetic timestamps only
DONCHIAN = {"class": "DonchianBreakoutComponent", "params": {"period": 20, "scaling_factor": 20.0}}
DAILY = {"n": 120, "warmup": ct.WARMUP_BARS["daily"], "step": 86400, "windows": 6}
MODELS = ("iid", "switching")
SIDES = {"upper": (">=", 12), "lower": ("<=", -12)}
METHODS = (ct.A851A_METHOD, ct.SIGNIFICANCE_METHOD)
HORIZONS = [1, 2, 3, 4, 5]


def simulate_sd(rng, n: int, model: str) -> np.ndarray:
    """Per-bar volatility: constant (iid) or a persistent two-state switch."""
    if model == "iid":
        return np.full(n, 0.035)
    wild = rng.random() < 0.5
    sd = np.empty(n)
    for t in range(n):
        if rng.random() < 0.01:
            wild = not wild
        sd[t] = 0.06 if wild else 0.02
    return sd


def simulate_windows(rng, model: str, signal: dict = DONCHIAN, cfg: dict = DAILY) -> list:
    out = []
    n, wu = cfg["n"], cfg["warmup"]
    m = n + wu
    for wi in range(cfg["windows"]):
        sd = simulate_sd(rng, m, model)
        close = 100.0 * np.exp(np.cumsum(rng.normal(0.0, 1.0, m) * sd))
        opn = np.r_[100.0, close[:-1]]
        wick = np.abs(rng.normal(0.0, 1.0, (2, m))) * sd * 0.5
        high = np.maximum(opn, close) * np.exp(wick[0])
        low = np.minimum(opn, close) * np.exp(-wick[1])
        fc = ct.compute_signal(signal, high, low, close)
        ts = (T0 + (wi * n + np.arange(-wu, n)) * cfg["step"]).astype(np.int64)
        warm = {"ts": ts[:wu], "high": high[:wu], "low": low[:wu], "close": close[:wu]}
        out.append(ct.Window("SIM", f"w{wi}", ts[wu:], close[wu:], fc[wu:],
                             np.array(["unknown"] * n, dtype=object), cfg["step"],
                             high=high[wu:], low=low[wu:], warm=warm, signal=signal))
    return out


def cell_spec(method: str, side: str, seed: int) -> ct.TestSpec:
    op, value = SIDES[side]
    sig = ({"method": method} if method == ct.A851A_METHOD
           else {"method": method, "n_resamples": N_NULL, "seed": seed})
    return ct.TestSpec(selector={"kind": "event", "field": "forecast", "op": op, "value": value},
                       outcome={"kind": "fwd_return", "horizons": HORIZONS},
                       baseline={"kind": "complement"}, statistic="mean_diff",
                       direction="greater" if side == "upper" else "less",
                       floor={"min_events": 1}, significance=sig)


def run_cell(method: str, model: str, side: str, n_sims: int = N_SIMS) -> dict:
    """One (method, model, side) cell; both directions from the same sims."""
    idx = METHODS.index(method) * 100 + MODELS.index(model) * 10 + list(SIDES).index(side)
    rng = np.random.default_rng([SEED, idx])
    rej = {d: {h: 0 for h in HORIZONS} for d in ("claimed", "opposite")}
    undefined = {h: 0 for h in HORIZONS}
    for k in range(n_sims):
        res = ct.run_test(simulate_windows(rng, model), cell_spec(method, side, k), calibrated=True)
        for h in HORIZONS:
            hr = res["horizons"][h]
            src = hr.get("a851a", hr)
            if src["p_value"] is None or src["p_value_opposite"] is None:
                undefined[h] += 1
                continue
            rej["claimed"][h] += src["p_value"] < ALPHA
            rej["opposite"][h] += src["p_value_opposite"] < ALPHA
    rows = []
    for d in ("claimed", "opposite"):
        share = {h: (rej[d][h] / (n_sims - undefined[h]) if n_sims > undefined[h] else None)
                 for h in HORIZONS}
        und = {h: undefined[h] / n_sims for h in HORIZONS}
        ok = all(und[h] <= MAX_UNDEFINED and share[h] is not None
                 and GATE[0] <= share[h] <= GATE[1] for h in HORIZONS)
        rows.append({"row": f"{model}_{side}_{d}", "n_sims": n_sims,
                     "share_p_below_0_05_of_defined": share, "share_undefined": und,
                     "pass": ok})
    return {"method": method, "model": model, "side": side, "rows": rows}


def summarize(method: str, cell_docs: list) -> dict:
    rows = [r for c in cell_docs if c["method"] == method for r in c["rows"]]
    expected = len(MODELS) * len(SIDES) * 2
    return {"method": method, "gate": {"alpha": ALPHA, "pass_range": list(GATE),
                                       "max_share_undefined": MAX_UNDEFINED},
            "seed": SEED, "rows": rows,
            "all_pass": len(rows) == expected and all(r["pass"] for r in rows)}


def main(argv=None) -> int:
    import yaml
    ap = argparse.ArgumentParser(description="claim_tests calibration gate")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("cell")
    c.add_argument("--method", choices=METHODS, required=True)
    c.add_argument("--model", choices=MODELS, required=True)
    c.add_argument("--side", choices=list(SIDES), required=True)
    c.add_argument("--n-sims", type=int, default=N_SIMS)
    c.add_argument("--out", type=Path, required=True)
    s = sub.add_parser("summarize")
    s.add_argument("--method", choices=METHODS, required=True)
    s.add_argument("--out", type=Path, required=True)
    s.add_argument("cells", nargs="+", type=Path)
    a = ap.parse_args(argv)
    if a.cmd == "cell":
        res = run_cell(a.method, a.model, a.side, a.n_sims)
    else:
        res = summarize(a.method, [yaml.safe_load(p.read_text(encoding="utf-8")) for p in a.cells])
    a.out.parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        yaml.safe_dump(res, f, sort_keys=False)
    for r in res["rows"]:
        print(f"{'PASS' if r['pass'] else 'FAIL'}  {res['method']}  {r['row']}  "
              + " ".join(f"h{h}={v:.3f}" if v is not None else f"h{h}=n/a"
                         for h, v in r["share_p_below_0_05_of_defined"].items())
              + f"  undefined_max={max(r['share_undefined'].values()):.2f}", flush=True)
    if a.cmd == "summarize":
        print("ALL PASS" if res["all_pass"] else "GATE FAILED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
