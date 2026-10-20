"""FOLD-FLOORS-2 (c), synthetic part: false-confirm and power of R5, R5 + remedy 1, R5 +
remedy 2 on cell A of FOLD-FLOORS-2026-10-19 (#495), iid paths (measurement only).

Synthetic prices only: no market data, nothing written except --out.
"Pass" = fold_confirm.grade_test(result, fold_windows=the fold's 6 labels) == confirmed
under R5: run with --tools <worktree of PR #496 (claims/fold-confirm-r5)>/strategy-research/tools.
The claim_tests blocks (selector, fwd_return, mean_diff) come unchanged from that path.
The remedies are defined in ff2_common.py's docstring.

Layout (as #495's fold_floor_sim.make_windows): 6 windows x 120 daily bars, each its own
iid Gaussian log-return walk, sd 0.035 per bar, zero drift. Cells (both directions on the
same paths, every cell of one sim on the same paths):
  null          the tool's outcome, no edge (cell A's null)
  edge 1% / 2%  the tool's outcome plus delta in the claimed direction on the selected bars
                (#495 planted delta on a SHADOW outcome; the tool-outcome cells keep the
                coupling of (i) in the test, which is what the remedies are for)
  shadow null / shadow edge 1% / 2%: the outcome read from an independent second path, as
                #495's P_A_edge cells (comparable to #495's power table)
Remedy 2's reference null: the same layout with an independent seed (--ref-sims draws);
the tool-outcome cells use the tool-outcome null, the shadow cells the shadow null.

Run (Git Bash, from the repo root, the venv's interpreter, under the shared test lock):
  python strategy-research/engineering/FOLD-FLOORS-2/remedy_power.py \
      --tools <r5 worktree>/strategy-research/tools --sims 2000 --ref-sims 2000 --check 50 \
      --out <dir>/remedy_power_synthetic.yaml
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ff2_common as fc  # noqa: E402

SEED = 20261020
SD, STEP, T0 = 0.035, 86400, 1577836800
K, N = 6, 120
EDGES = (0.0, 0.01, 0.02)
DIRS = ("less", "greater")


def make_windows(ct, rng, shadow):
    sel, out = [], []
    for i in range(K):
        ts = (T0 + i * N * STEP + np.arange(N) * STEP).astype(np.int64)
        reg = np.array(["unknown"] * N, dtype=object)
        close = 100.0 * np.exp(np.cumsum(rng.normal(0.0, SD, N)))
        sel.append(ct.Window("SIM", f"w{i}", ts, close, np.full(N, np.nan), reg, STEP))
        if shadow:
            c2 = 100.0 * np.exp(np.cumsum(rng.normal(0.0, SD, N)))
            out.append(ct.Window("SIM", f"w{i}", ts, c2, np.full(N, np.nan), reg, STEP))
    return sel, (out if shadow else None)


def run(ct, cmeas, fcf, sims, seed, refs=None, check=0, edges=EDGES):
    labels = [f"w{i}" for i in range(K)]
    rng = np.random.default_rng(seed)
    cells = {}
    for kind in ("tool", "shadow"):
        for e in edges:
            for d in DIRS:
                ref = None if refs is None else refs[f"{kind}|null|{d}"]
                cells[f"{kind}|{'null' if e == 0 else f'edge{e}'}|{d}"] = fc.Tally(K, ref)
    for s in range(sims):
        sw, ow = make_windows(ct, rng, shadow=True)
        for kind, o in (("tool", None), ("shadow", ow)):
            for e in edges:
                for d in DIRS:
                    r = fc.cell_a_fold(ct, cmeas, fcf, sw, d, labels, edge=e, outcome_windows=o,
                                       check=(s < check and kind == "tool" and e == 0))
                    cells[f"{kind}|{'null' if e == 0 else f'edge{e}'}|{d}"].add(r)
    return cells


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--tools", type=Path, required=True)
    ap.add_argument("--sims", type=int, default=2000)
    ap.add_argument("--ref-sims", type=int, default=2000)
    ap.add_argument("--check", type=int, default=0)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    ct, cmeas, fcf = fc.load_tools(a.tools)
    t0 = time.time()
    ref_cells = run(ct, cmeas, fcf, a.ref_sims, [SEED, 1], edges=(0.0,))
    refs = {k: v.reference() for k, v in ref_cells.items()}
    t1 = time.time()
    print(f"reference ({a.ref_sims} sims) {t1 - t0:.0f}s", flush=True)
    for k, v in refs.items():
        print(f"  ref {k:22s} pooled_q95 {v['pooled_q95']:+.5f}  share_q95 {v['share_q95']:.3f}", flush=True)
    cells = run(ct, cmeas, fcf, a.sims, [SEED, 2], refs=refs, check=a.check)
    t2 = time.time()
    out = {"script": "remedy_power.py", "tools": str(a.tools.resolve()), "seed_reference": [SEED, 1],
           "seed_test": [SEED, 2], "layout": {"windows": K, "bars": N, "sd": SD},
           "cell": "A: past_return(5) >= +0.05, fwd_return h=3, mean_diff vs complement",
           "floor": fc.FLOOR, "spacing_remedy1": fc.SPACING, "check_sims_full_chain": a.check,
           "reference": {k: dict(v, cell=k) for k, v in refs.items()},
           "cells": {k: v.summary() for k, v in cells.items()},
           "seconds": {"reference": round(t1 - t0, 1), "test": round(t2 - t1, 1)}}
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(yaml.safe_dump(out, sort_keys=False), encoding="utf-8")
    for k, v in out["cells"].items():
        c = v["confirm"]
        print(f"{k:26s} win+ {v['per_window_claimed_sign']['rate']:.3f}  R5 {c['R5']['rate']:.3f}"
              f"  rem1a {c['rem1a']['rate']:.3f}  rem1b {c['rem1b']['rate']:.3f}"
              f"  rem2p {c['rem2_pooled']['rate']:.3f}  rem2s {c['rem2_share']['rate']:.3f}"
              f"  ev {v['selected_events_per_fold']} thin {v['selected_thinned_per_fold']}", flush=True)
    print(f"total {t2 - t0:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
