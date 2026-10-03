"""E-068 slice 1 (CUL-386): calibration gate for tools/claim_tests.py.

Pre-registered in engineering/roadmap/E-068/regrade_specs/AMENDMENT_3.md,
section 5, before it was run. The claim tool must not find an edge where there
is none. On simulated prices with NO edge, using the real signal, the share of
one-sided p < 0.05 must be about 0.05 in each direction.

  Signal   DonchianBreakoutComponent(period=20), daily, via claim_tests.SIGNALS
           (vectorized copy, proven equal to update() by a test); clip +-20.
  Layout   6 windows x 120 daily bars whose TIMESTAMPS abut (as run_065's
           do); each window is its own independent price path with its own
           30 warm-up bars. No eras are passed (all dates fall in one era, as
           run_065's do).
  Note     rejection is counted as p < 0.05 with N = 199 fakes, so a valid
           method's expected share is at most 9/200 = 0.045 (at the grade's
           N = 1000 it is 0.04995): this gate is slightly stricter than the
           grade (final review, 2026-10-03).
  Prices   zero mean, no edge: `iid` normal (sd 0.035); `switching` two-state
           volatility (calm sd 0.02, wild sd 0.06, switch prob 0.01 per bar,
           ~100-bar spells). Intrabar high/low scale with the bar's own sd.
  Cells    model x side (forecast >= 12, forecast <= -12) x direction
           (claimed, opposite), horizons 1-5; both directions come from the
           same simulations (p_value and p_value_opposite).
  Methods  a851a_episode_v1 (existing A8.5.1a, its own 2000 resamples) and
           block_permutation_v1 (N = 199 fakes per simulation).
  Pass     per row: undefined p in <= 5% of simulations, AND among defined p
           the share below 0.05 at most 0.075 (the ceiling) at every horizon.
           ONE-SIDED since amendment 5: a share below 0.025 (the floor) is a
           pass with a "conservative" warning, listed per row. A method passes
           if all 8 rows pass. Undefined p are counted and reported, never
           hidden as "no rejection". (Amendment 3's two-sided band failed the
           floor too.)

Each (method, model, side) cell runs as its own job and writes its own file:
    python tools/claim_tests_calibration.py cell --method M --model X --side S --out F
    python tools/claim_tests_calibration.py summarize --method M --out F CELL_FILES...
Cells written before per-cell code hashes (amendment 3's, commit bc4e67f4) are
re-judged under the current rule, without re-running, by
    python tools/claim_tests_calibration.py reevaluate --method M --code-ref REF --out F CELLS...
which records the hash of the producing code read from git at REF.
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
ALPHA = ct.CALIBRATION_GATE["alpha"]
N_SIMS = 400
N_NULL = 199
T0 = 1577836800            # 2020-01-01 UTC, synthetic timestamps only
DONCHIAN = {"class": "DonchianBreakoutComponent", "params": {"period": 20, "scaling_factor": 20.0}}
DAILY = {"n": 120, "warmup": ct.WARMUP_BARS["daily"], "step": 86400, "windows": 6}
MODELS = ("iid", "switching")
SIDES = {"upper": (">=", 12), "lower": ("<=", -12)}
METHODS = (ct.A851A_METHOD, ct.SIGNIFICANCE_METHOD, ct.A851A_TIMEGAP_METHOD)
PERIODS = (20, 14)          # run_065's two signals; the identical gate runs once per signal


def donchian(period: int) -> dict:
    return {"class": "DonchianBreakoutComponent",
            "params": {"period": period, "scaling_factor": 20.0}}
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
    sig = ({"method": method} if method in ct.A851A_METHODS
           else {"method": method, "n_resamples": N_NULL, "seed": seed})
    return ct.TestSpec(selector={"kind": "event", "field": "forecast", "op": op, "value": value},
                       outcome={"kind": "fwd_return", "horizons": HORIZONS},
                       baseline={"kind": "complement"}, statistic="mean_diff",
                       direction="greater" if side == "upper" else "less",
                       floor={"min_events": 1}, significance=sig)


def run_cell(method: str, model: str, side: str, n_sims: int = N_SIMS, period: int = 20) -> dict:
    """One (method, model, side) cell; both directions from the same sims.
    For the two older methods, period-20 seeds equal the earlier gate runs';
    a new method gets new seed indices."""
    idx = (METHODS.index(method) * 100 + MODELS.index(model) * 10 + list(SIDES).index(side)
           + (0 if period == 20 else 1000 * period))
    signal = donchian(period)
    rng = np.random.default_rng([SEED, idx])
    rej = {d: {h: 0 for h in HORIZONS} for d in ("claimed", "opposite")}
    undefined = {h: 0 for h in HORIZONS}
    for k in range(n_sims):
        res = ct.run_test(simulate_windows(rng, model, signal), cell_spec(method, side, k),
                          calibrated=True)
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
        rows.append(_rejudged({"row": f"{model}_{side}_{d}", "n_sims": n_sims,
                               "share_p_below_0_05_of_defined": share,
                               "share_undefined": und}))
    return {"method": method, "model": model, "side": side, "signal": signal, "rows": rows,
            "code_sha256": code_sha256()}


def code_sha256() -> str:
    """Hash of the two files that produce a calibration result."""
    import hashlib
    h = hashlib.sha256()
    for f in (ct.__file__, __file__):
        h.update(Path(f).read_bytes())
    return h.hexdigest()


def _rejudged(row: dict) -> dict:
    """A gate row judged under the CURRENT rule (amendment 5, one-sided),
    whatever rule wrote its `pass` flag."""
    keep = {k: row[k] for k in ("row", "n_sims", "share_p_below_0_05_of_defined",
                                "share_undefined")}
    ok, cons = ct.judge_calibration_row(keep)
    return dict(keep, conservative_horizons=cons, **{"pass": ok})


def summarize(method: str, cell_docs: list) -> dict:
    cells = [c for c in cell_docs if c["method"] == method]
    rows = [_rejudged(r) for c in cells for r in c["rows"]]
    full = (len({r["row"] for r in rows}) == ct.CALIBRATION_ROWS
            and all(r.get("n_sims") == N_SIMS for r in rows))
    signals = [c.get("signal", DONCHIAN) for c in cells]
    signal = signals[0] if signals and all(x == signals[0] for x in signals) else None
    hashes = {c.get("code_sha256") for c in cells}
    code = hashes.pop() if len(hashes) == 1 else None      # all cells from one code version
    # E-068 slice 3: the scope names exactly what the cells simulated -- the
    # selector of each side (cell_spec) and the fakes the method really draws
    # (A8.5.1a its own resamples, not N_NULL) -- so the lock can match them.
    sides = sorted({c["side"] for c in cells if c.get("side") in SIDES})
    selectors = [cell_spec(method, s, 0).selector for s in sides]
    n_null = ct.A851A_SETTINGS["n_resamples"] if method in ct.A851A_METHODS else N_NULL
    return {"method": method, "gate": dict(ct.CALIBRATION_GATE), "seed": SEED,
            "scope": {"signal": signal, "cadence": "daily", "statistic": "mean_diff",
                      "selector": selectors, "outcome": "fwd_return",
                      "n_null": n_null, "n_sims": N_SIMS},
            "code_sha256": code, "rows": rows,
            "conservative": {r["row"]: r["conservative_horizons"] for r in rows
                             if r["conservative_horizons"]},
            "all_pass": (len(rows) == ct.CALIBRATION_ROWS and code is not None
                         and signal is not None and full
                         and all(r["pass"] for r in rows))}


CODE_FILES = ("strategy-research/tools/claim_tests.py",
              "strategy-research/tools/claim_tests_calibration.py")


REPO_ROOT = Path(__file__).resolve().parents[2]


def git_blob(ref: str, repo_path: str) -> bytes:
    """A file's bytes as git stores them at REF (LF; independent of the
    checkout's line endings, so a hash of them is reproducible anywhere)."""
    import subprocess
    return subprocess.run(["git", "-C", str(REPO_ROOT), "show", f"{ref}:{repo_path}"],
                          check=True, capture_output=True).stdout


def code_sha256_at(ref: str) -> str:
    """code_sha256() of the two producing files as committed at git REF (same
    order; git's stored bytes -- the amendment-4 hashes match this form)."""
    import hashlib
    h = hashlib.sha256()
    for f in CODE_FILES:
        h.update(git_blob(ref, f))
    return h.hexdigest()


def committed_cells(paths: list, ref: str) -> tuple[list, dict]:
    """(cell docs, {repo path: sha256 of git's stored bytes}) for cell files
    committed at REF. Refused if a working file differs from its blob at REF
    (line endings aside): the cells re-evaluated must be the cells produced."""
    import hashlib
    import yaml
    docs, shas = [], {}
    for p in paths:
        rel = Path(p).resolve().relative_to(REPO_ROOT).as_posix()
        blob = git_blob(ref, rel)
        if Path(p).read_bytes().replace(b"\r\n", b"\n") != blob.replace(b"\r\n", b"\n"):
            raise ValueError(f"{rel} differs from its committed version at {ref}")
        docs.append(yaml.safe_load(blob.decode("utf-8")))
        shas[rel] = hashlib.sha256(blob).hexdigest()
    return docs, shas


def reevaluate(method: str, cell_docs: list, cell_sha256: dict, code_ref: str,
               code_hash: str) -> dict:
    """Amendment 5 section 4: existing cells re-judged under the current rule,
    NOT re-run. Only for cells that predate per-cell code hashes and the
    per-cell signal field (so they ran the then-only signal, Donchian(20));
    the hash of their producing code (read from git at `code_ref`) is
    recorded with it."""
    if any(c.get("code_sha256") for c in cell_docs):
        raise ValueError("these cells carry their own code hash; use `summarize`")
    if any(c.get("signal", DONCHIAN) != DONCHIAN for c in cell_docs):
        raise ValueError("pre-hash cells can only be the Donchian(20) gate")
    res = summarize(method, [dict(c, code_sha256=code_hash) for c in cell_docs])
    res["reevaluated"] = {"rule": "amendment 5 (one-sided)", "rerun": False,
                          "code_ref": code_ref,
                          "code_sha256_source": f"git blobs of {list(CODE_FILES)} at {code_ref}",
                          "cell_files_sha256_source": f"git blobs at {code_ref}",
                          "cell_files_sha256": dict(cell_sha256)}
    return res


def main(argv=None) -> int:
    import yaml
    ap = argparse.ArgumentParser(description="claim_tests calibration gate")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("cell")
    c.add_argument("--method", choices=METHODS, required=True)
    c.add_argument("--model", choices=MODELS, required=True)
    c.add_argument("--side", choices=list(SIDES), required=True)
    c.add_argument("--n-sims", type=int, default=N_SIMS)
    c.add_argument("--period", type=int, choices=PERIODS, default=20)
    c.add_argument("--out", type=Path, required=True)
    s = sub.add_parser("summarize")
    s.add_argument("--method", choices=METHODS, required=True)
    s.add_argument("--out", type=Path, required=True)
    s.add_argument("cells", nargs="+", type=Path)
    r = sub.add_parser("reevaluate")
    r.add_argument("--method", choices=METHODS, required=True)
    r.add_argument("--code-ref", required=True, help="git commit that produced the cells")
    r.add_argument("--out", type=Path, required=True)
    r.add_argument("cells", nargs="+", type=Path)
    a = ap.parse_args(argv)
    if a.cmd == "cell":
        res = run_cell(a.method, a.model, a.side, a.n_sims, a.period)
    elif a.cmd == "summarize":
        res = summarize(a.method, [yaml.safe_load(p.read_text(encoding="utf-8")) for p in a.cells])
    else:
        docs, shas = committed_cells(a.cells, a.code_ref)
        res = reevaluate(a.method, docs, shas, a.code_ref, code_sha256_at(a.code_ref))
    a.out.parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        yaml.safe_dump(res, f, sort_keys=False)
    for r in res["rows"]:
        print(f"{'PASS' if r['pass'] else 'FAIL'}  {res['method']}  {r['row']}  "
              + " ".join(f"h{h}={v:.3f}" if v is not None else f"h{h}=n/a"
                         for h, v in r["share_p_below_0_05_of_defined"].items())
              + f"  undefined_max={max(r['share_undefined'].values()):.2f}", flush=True)
    if a.cmd != "cell":
        for row, hs in res["conservative"].items():
            print(f"CONSERVATIVE  {row}  horizons {hs}")
        print("ALL PASS" if res["all_pass"] else "GATE FAILED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
