"""FOLD-FLOORS-2026-10-19: null simulator for fold_confirm's noise rule (measurement only).

Synthetic prices only: no market data, no run folder, nothing written except --out.
Uses the UNCHANGED blocks of tools/claim_tests.py (selectors, fwd_return, complement,
statistics) and tools/fold_confirm.grade_test (the noise rule). The plain cell is
cross-checked against the full chain claim_measure.measure_test -> fold_confirm.grade_test
(--check N sims per plain cell; any difference raises).

Layout: K windows (default 6) x N daily bars (default 120), each its own iid Gaussian
log-return random walk (sd 0.035 per bar, zero drift: no edge anywhere), as
tools/claim_tests_calibration.simulate_windows lays them out (no warm-up rows are
needed: no signal is recomputed).

Controlled variants (one change each, see CELLS):
  outcome   arith (fwd_return, the tool's) | log (log(close[t+h]/close[t])) |
            shadow (fwd_return of an INDEPENDENT second path: selection and outcome
            share nothing)
  stride    None | s: only bars t with t % s == 0 are candidates (selected or complement)
  baseline  complement (the tool's) | zero_sel (selected mean minus the exact expected
            outcome) | zero_comp (exact expected outcome minus the complement mean)
  statistic mean_diff | hit_rate

Run (from the repo root, the venv's interpreter):
  python strategy-research/engineering/FOLD-FLOORS-2026-10-19/fold_floor_sim.py \
      --sims 1000 --out <scratch>/sim.yaml [--only CELL ...] [--check 50]
"""
from __future__ import annotations

import argparse
import math
import sys
import time
from pathlib import Path

import numpy as np
import yaml

TOOLS = Path(__file__).resolve().parents[2] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import claim_measure as cmeas  # noqa: E402
import claim_tests as ct  # noqa: E402
import fold_confirm as fcf  # noqa: E402

SEED = 20261019
SD = 0.035
STEP = 86400
T0 = 1577836800
FLOOR = {"min_events": 100, "min_windows": 4}     # the three recorded claims' floor


def _path(rng, n):
    return 100.0 * np.exp(np.cumsum(rng.normal(0.0, SD, n)))


def make_windows(rng, k, n, shadow=False, empty=0):
    """`empty`: the last `empty` windows hold 4 bars only (a coin or period with almost no
    data): no selector with bars >= 4 has a value there."""
    sel, out = [], []
    for i in range(k):
        ni = 4 if i >= k - empty else n
        ts = (T0 + i * n * STEP + np.arange(ni) * STEP).astype(np.int64)
        reg = np.array(["unknown"] * ni, dtype=object)
        w = ct.Window("SIM", f"w{i}", ts, _path(rng, ni), np.full(ni, np.nan), reg, STEP)
        sel.append(w)
        if shadow:
            out.append(ct.Window("SIM", f"w{i}", ts, _path(rng, ni), np.full(ni, np.nan), reg, STEP))
    return sel, (out if shadow else sel)


def outcome(w, h, kind):
    if kind == "log":
        y = ct.out_fwd_return(w, h)
        return np.log1p(y)
    return ct.out_fwd_return(w, h)


def expected(h, kind, stat, direction):
    """The exact per-bar expectation of the outcome (or the hit share) under the null."""
    if stat == "hit_rate":
        return 0.5 if kind == "log" else (
            # P(fwd arith > 0) == P(log > 0) == 0.5 for a zero-drift Gaussian log walk
            0.5)
    return 0.0 if kind == "log" else math.exp(h * SD * SD / 2.0) - 1.0


def stat_value(y, mask, wref, direction, stat, baseline, mu0):
    sign = 1.0 if direction == "greater" else -1.0
    if baseline == "complement":
        return ct.STATISTICS[stat](y, mask, wref, np.full(len(y), np.nan), direction)[1]
    if stat == "hit_rate":
        hit = (y > 0) if direction == "greater" else (y < 0)
        z = np.where(np.isfinite(y), hit.astype(float), np.nan)
        side = mask if baseline == "zero_sel" else (wref > 0)
        ok = side & np.isfinite(z)
        if not ok.any():
            return float("nan")
        m = float(z[ok].mean())
        return m - mu0 if baseline == "zero_sel" else mu0 - m
    side = mask if baseline == "zero_sel" else (wref > 0)
    ok = side & np.isfinite(y)
    if not ok.any():
        return float("nan")
    m = float(y[ok].mean())
    return sign * (m - mu0 if baseline == "zero_sel" else mu0 - m)


def one_sim(rng, c, check=False):
    k, n = c.get("k", 6), c.get("n", 120)
    sw, ow = make_windows(rng, k, n, c.get("outcome") == "shadow", c.get("empty", 0))
    hs = c["h"]
    kind = "log" if c.get("outcome") == "log" else "arith"
    stat, base, d = c.get("statistic", "mean_diff"), c.get("baseline", "complement"), c["direction"]
    per = []
    for w, wo in zip(sw, ow):
        mask, valid = ct.SELECTORS[c["selector"]["kind"]](w, c["selector"])
        mask = mask & valid
        if c.get("stride"):
            keep = (np.arange(len(w.ts)) % c["stride"]) == 0
            mask, valid = mask & keep, valid & keep
        wref = (valid & ~mask).astype(float)
        ys = {h: outcome(wo, h, kind) for h in hs}
        if c.get("edge"):           # a REAL effect of the claimed sign on the selected bars (power)
            for h in hs:
                ys[h] = ys[h] + np.where(mask, (1.0 if d == "greater" else -1.0) * c["edge"], 0.0)
        per.append({"label": w.label, "mask": mask, "wref": wref, "ys": ys})
    horizons = {}
    for h in hs:
        mu0 = expected(h, kind, stat, d)
        pw, nev, nref = {}, {}, {}
        for p in per:
            y = p["ys"][h]
            o = stat_value(y, p["mask"], p["wref"], d, stat, base, mu0)
            pw[p["label"]] = {"oriented": None if not np.isfinite(o) else float(o)}
            nev[p["label"]] = int((p["mask"] & np.isfinite(y)).sum())
            nref[p["label"]] = int(((p["wref"] > 0) & np.isfinite(y)).sum())
        y = np.concatenate([p["ys"][h] for p in per])
        m = np.concatenate([p["mask"] for p in per])
        wr = np.concatenate([p["wref"] for p in per])
        o = stat_value(y, m, wr, d, stat, base, mu0)
        horizons[h] = {"value": None, "oriented": None if not np.isfinite(o) else float(o),
                       "n_events": int(sum(nev.values())),
                       "n_windows_with_events": int(sum(1 for v in nev.values() if v > 0)),
                       "per_window": pw, "_nev": nev, "_nref": nref}
    status = cmeas.NO_EVENTS if all(x["n_events"] == 0 for x in horizons.values()) else cmeas.MEASURED
    result = {"status": status, "horizons": horizons}
    if check:
        test = {"name": "t", "selector": c["selector"], "outcome": {"kind": "fwd_return", "horizons": hs},
                "baseline": {"kind": "complement"}, "statistic": stat, "direction": d,
                "floor": dict(FLOOR)}
        real = cmeas.measure_test(sw, test, None)
        g_real, g_mine = fcf.grade_test(real), fcf.grade_test(result)
        assert g_real["status"] == g_mine["status"], (g_real, g_mine)
        for h in hs:
            a, b = real["horizons"][h], horizons[h]
            assert a["n_events"] == b["n_events"]
            for lab, cell in a["per_window"].items():
                x, z = cell["oriented"], b["per_window"][lab]["oriented"]
                assert (x is None and z is None) or abs(x - z) < 1e-12, (lab, x, z)
            assert (a["oriented"] is None and b["oriented"] is None) or abs(a["oriented"] - b["oriented"]) < 1e-12
    return result


# ---------------------------------------------------------------------------
# Rules (iii): R0 is fold_confirm.grade_test unchanged; the others are candidates
# ---------------------------------------------------------------------------

def _k_n(h):
    vals = [c["oriented"] for c in h["per_window"].values() if c["oriented"] is not None]
    return sum(1 for v in vals if v > 0), len(vals)


def rule_r0(res):
    return fcf.grade_test(res)["status"] == fcf.CONFIRMED


def rule_pooled_floor(res, floor=FLOOR):
    """R1: R0, and the claim's own floor (claim_measure's reading: pooled per horizon)
    must be met at every horizon, else not measurable."""
    if not rule_r0(res):
        return False
    for h in res["horizons"].values():
        if h["n_events"] < floor["min_events"] or h["n_windows_with_events"] < floor["min_windows"]:
            return False
    return True


def rule_window_floor(res, m, n_fold, against=True, min_windows=4, floor=FLOOR):
    """R2 (against=True): a window below the per-window floor m (selected events AND
    baseline events) counts AGAINST; confirmed when the pooled sign holds and at most one
    of the fold's n_fold windows is against (wrong sign, no value, or below the floor),
    plus R1's pooled floor. R3 (against=False): a below-floor window is dropped and the
    all-but-one rule runs on the rest (needs min_windows), plus R1's pooled floor."""
    if res["status"] != cmeas.MEASURED:
        return False
    for h in res["horizons"].values():
        if h["oriented"] is None or h["oriented"] <= 0:
            return False
        if h["n_events"] < floor["min_events"] or h["n_windows_with_events"] < floor["min_windows"]:
            return False
        good = bad = 0
        for lab, c in h["per_window"].items():
            ok_floor = h["_nev"][lab] >= m and h["_nref"][lab] >= m
            if not ok_floor:
                if against:
                    bad += 1
                continue
            if c["oriented"] is not None and c["oriented"] > 0:
                good += 1
            else:
                bad += 1
        if against:
            bad += n_fold - len(h["per_window"])
            if bad > 1:
                return False
        else:
            if good + bad < min_windows or bad > 1:
                return False
    return True


def rule_all_windows(res, min_windows=4):
    """R4: every window with a value has the claimed sign (none against)."""
    if res["status"] != cmeas.MEASURED:
        return False
    for h in res["horizons"].values():
        k, n = _k_n(h)
        if h["oriented"] is None or h["oriented"] <= 0 or n < min_windows or k < n:
            return False
    return True


def rules(res, n_fold):
    return {"R0_current": rule_r0(res),
            "R1_pooled_floor": rule_pooled_floor(res),
            "R5_pooled_floor_fold_denominator": rule_window_floor(res, 1, n_fold, True),
            "R2_window_floor_against_m10": rule_window_floor(res, 10, n_fold, True),
            "R2_window_floor_against_m17": rule_window_floor(res, 17, n_fold, True),
            "R3_window_floor_dropped_m17": rule_window_floor(res, 17, n_fold, False),
            "R4_all_windows": rule_all_windows(res)}


# ---------------------------------------------------------------------------
# Cells
# ---------------------------------------------------------------------------

def pr_ge(bars, v):
    return {"kind": "event", "field": "past_return", "bars": bars, "op": ">=", "value": v}


def pr_le(bars, v):
    return {"kind": "event", "field": "past_return", "bars": bars, "op": "<=", "value": v}


def pr_q(bars, side="top", q=0.2, lookback=20):
    return {"kind": "quantile", "field": "past_return", "bars": bars, "lookback": lookback,
            "q": q, "side": side}


def tv_ge(bars, v):
    return {"kind": "event", "field": "trailing_vol", "bars": bars, "op": ">=", "value": v}


def _pair(name, base, **kw):
    """Both directions of one selector, same seeds (paired paths)."""
    return [(f"{name}|less", dict(base, direction="less", **kw)),
            (f"{name}|greater", dict(base, direction="greater", **kw))]


def cells():
    A = {"selector": pr_ge(5, 0.05), "h": [3]}
    out = []
    # (i) reproduction
    out += _pair("A_abs_rise", A)
    out += _pair("A_quant_top", {"selector": pr_q(5), "h": [3]})
    out += _pair("A_abs_fall", {"selector": pr_le(5, -0.05), "h": [3]})
    out += _pair("A_trailing_vol", {"selector": tv_ge(10, 0.035), "h": [3]})
    # (i) one change at a time, on A
    out += _pair("V_shadow_outcome", A, outcome="shadow")
    out += _pair("V_log_outcome", A, outcome="log")
    out += _pair("V_stride_8", A, stride=8)
    out += _pair("V_stride_8_n960", A, stride=8, n=960)
    out += _pair("V_stride_4", A, stride=4)
    out += _pair("V_zero_sel", A, baseline="zero_sel")
    out += _pair("V_zero_comp", A, baseline="zero_comp")
    out += _pair("V_hit_rate", A, statistic="hit_rate")
    out += _pair("V_h1", {"selector": pr_ge(5, 0.05), "h": [1]})
    out += _pair("V_h6", {"selector": pr_ge(5, 0.05), "h": [6]})
    out += _pair("V_bars1", {"selector": pr_ge(1, 0.03), "h": [3]})
    out += _pair("V_k4", A, k=4)
    out += _pair("V_k8", A, k=8)
    out += _pair("V_n480", A, n=480)
    out += _pair("V_sparse", {"selector": pr_ge(5, 0.12), "h": [3]})
    out += _pair("V_three_h", {"selector": pr_ge(5, 0.05), "h": [1, 3, 6]})
    # (iii) a selector thin enough for the floors to bite (~19 events per window, ~115
    # per fold), with the tool's outcome and with the coupling removed (a symmetric null)
    out += _pair("F_mid", {"selector": pr_ge(5, 0.075), "h": [3]})
    out += _pair("F_mid_shadow", {"selector": pr_ge(5, 0.075), "h": [3]}, outcome="shadow")
    out += _pair("F_mid_tv", {"selector": tv_ge(10, 0.042), "h": [3]})
    # (iii) power: a real effect of the claimed sign added to the selected bars' outcome
    # (shadow outcome, so the coupling of (i) is absent and only the edge differs)
    for e in (0.01, 0.02):
        out += _pair(f"P_A_edge{e}", A, outcome="shadow", edge=e)
        out += _pair(f"P_mid_edge{e}", {"selector": pr_ge(5, 0.075), "h": [3]}, outcome="shadow", edge=e)
    # (iii) a fold where 2 of its 6 windows have no value (a coin or period with almost no
    # data): the current rule grades the other 4 (3 of 4 suffices)
    out += _pair("F_two_empty", A, empty=2)
    out += _pair("F_two_empty_shadow", A, outcome="shadow", empty=2)
    out += _pair("F_one_empty_shadow", A, outcome="shadow", empty=1)
    return out


def mechanism(sims, out_path):
    """The decisive measurement of (i): per window, S = the sum of the selected bars'
    log forward returns, N = their count. E[S] is 0 by construction (each bar's outcome
    is independent of its OWN selection); the mean S/N is what the rule reads. Also: how
    many of the next n+h bars are selected after a selected bar whose own outcome rose
    vs fell (the cluster-length coupling). Selector A (past_return 5 bars >= +5%), h=3."""
    res = {}
    for label, stride in (("stride_1_tool", None), ("stride_8_no_overlap", 8)):
        rng = np.random.default_rng([SEED, 999])
        S, N, M, after_up, after_dn = [], [], [], [], []
        sel = pr_ge(5, 0.05)
        h = 3
        for _ in range(sims):
            ws, _o = make_windows(rng, 6, 120)
            for w in ws:
                mask, valid = ct.SELECTORS["event"](w, sel)
                mask &= valid
                if stride:
                    mask &= (np.arange(len(w.ts)) % stride) == 0
                y = np.log1p(ct.out_fwd_return(w, h))
                ev = mask & np.isfinite(y)
                if not ev.any():
                    continue
                S.append(float(y[ev].sum()))
                N.append(int(ev.sum()))
                M.append(float(y[ev].mean()))
                for t in np.nonzero(ev)[0]:
                    nxt = mask[t + 1:t + 1 + 5 + h].sum()
                    (after_up if y[t] > 0 else after_dn).append(int(nxt))
        S, N, M = np.array(S), np.array(N), np.array(M)

        def ms(x):
            return {"mean": float(x.mean()), "se": float(x.std(ddof=1) / math.sqrt(len(x)))}
        res[label] = {"windows": int(len(S)), "sum_S": ms(S), "mean_S_over_N": ms(M),
                      "share_mean_below_0": _rate(int((M < 0).sum()), len(M)),
                      "corr_S_N": float(np.corrcoef(S, N)[0, 1]),
                      "selected_in_next_8_bars_after_up_outcome": ms(np.array(after_up, float)),
                      "selected_in_next_8_bars_after_down_outcome": ms(np.array(after_dn, float))}
        print(label, yaml.safe_dump(res[label], sort_keys=False), flush=True)
    out_path.write_text(yaml.safe_dump({"seed": [SEED, 999], "sims": sims, "mechanism": res},
                                       sort_keys=False), encoding="utf-8")
    return 0


def _rate(x, n):
    p = x / n if n else None
    return {"rate": None if p is None else round(p, 4), "count": int(x), "n": int(n),
            "se": None if p is None else round(math.sqrt(p * (1 - p) / n), 4)}


def run_cell(idx, name, c, sims, check):
    rng = np.random.default_rng([SEED, idx // 2])         # the pair shares its paths
    n_fold = c.get("k", 6)
    pos = tot = 0
    pooled = []
    corr_num = []
    conf = {}
    for s in range(sims):
        res = one_sim(rng, c, check=check > s and c.get("outcome", "arith") == "arith" and c["selector"].get("field") == "past_return"
                      and not c.get("stride") and c.get("baseline", "complement") == "complement")
        for h in res["horizons"].values():
            for cell in h["per_window"].values():
                if cell["oriented"] is not None:
                    tot += 1
                    pos += cell["oriented"] > 0
            if h["oriented"] is not None:
                pooled.append(h["oriented"])
        for r, ok in rules(res, n_fold).items():
            conf[r] = conf.get(r, 0) + int(ok)
        ev = [sum(h["_nev"].values()) / n_fold for h in res["horizons"].values()]
        corr_num.append(float(np.mean(ev)))
    pooled = np.array(pooled)
    return {"cell": name, "config": {k: v for k, v in c.items()}, "sims": sims,
            "per_window_claimed_sign": _rate(pos, tot),
            "pooled_oriented_mean": float(pooled.mean()) if len(pooled) else None,
            "pooled_oriented_se": float(pooled.std(ddof=1) / math.sqrt(len(pooled))) if len(pooled) > 1 else None,
            "pooled_claimed_sign": _rate(int((pooled > 0).sum()), len(pooled)),
            "mean_events_per_window": round(float(np.mean(corr_num)), 2),
            "confirm": {r: _rate(v, sims) for r, v in conf.items()}}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--sims", type=int, default=1000)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--check", type=int, default=0, help="cross-check the first N sims of plain cells")
    ap.add_argument("--mechanism", action="store_true", help="run only the (i) mechanism measurement")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    if a.mechanism:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        return mechanism(a.sims, a.out)
    out = []
    t0 = time.time()
    for i, (name, c) in enumerate(cells()):
        if a.only and not any(name.startswith(o) for o in a.only):
            continue
        t = time.time()
        r = run_cell(i, name, c, a.sims, a.check)
        r["seconds"] = round(time.time() - t, 1)
        out.append(r)
        cf = r["confirm"]
        print(f"{name:32s} win+ {r['per_window_claimed_sign']['rate']:.3f}"
              f"±{r['per_window_claimed_sign']['se']:.3f}  R0 {cf['R0_current']['rate']:.3f}"
              f"±{cf['R0_current']['se']:.3f}  R1 {cf['R1_pooled_floor']['rate']:.3f}"
              f"  R5 {cf['R5_pooled_floor_fold_denominator']['rate']:.3f}"
              f"  R2m10 {cf['R2_window_floor_against_m10']['rate']:.3f}"
              f"  R2m17 {cf['R2_window_floor_against_m17']['rate']:.3f}"
              f"  R3m17 {cf['R3_window_floor_dropped_m17']['rate']:.3f}"
              f"  R4 {cf['R4_all_windows']['rate']:.3f}  ev/w {r['mean_events_per_window']}"
              f"  ({r['seconds']}s)", flush=True)
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(yaml.safe_dump({"seed": SEED, "sd": SD, "floor": FLOOR, "cells": out},
                                        sort_keys=False), encoding="utf-8")
    print(f"total {time.time() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
