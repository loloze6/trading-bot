"""FOLD-FLOORS-2 (a): trade-level null of the three recorded confirmations (measurement only).

Synthetic prices only: no market data, no run folder, nothing written except --out.
"Pass" = fold_confirm.grade_test(claim_measure.measure_test(windows, test, None,
trade_tests=True), fold_windows=<the fold's 6 labels>) == confirmed, under R5: run with
--tools <worktree of PR #496 (claims/fold-confirm-r5)>/strategy-research/tools. The full
chain is used for every sim (claim_measure.measure_test with the trade family on, then
grade_test), the claim_tests / claim_measure blocks unchanged from that tools path.

The three tests are copied exactly from the child runs' hypothesis cards (run_096, run_079,
run_078, artifacts/hypothesis_card.yaml) and each is run in both directions on the same
paths; the claimed direction's spec_hash is asserted equal to the hash recorded in
campaign_record/confirmations.yaml:
  T1 forecast_power-run_095-1 (run_096): side == short, trade_net_return, mean_diff vs
     other_trades, claimed `less`
  T2 trade_efficiency-run_066-2 (run_079): exit_cause == flip, post_exit_return h 1, 6, 24,
     hit_rate vs other_trades, claimed `greater`
  T3 trade_efficiency-run_071-4 (run_078): entry_forecast >= 10, trade_net_return,
     mean_diff vs other_trades, claimed `greater`
  floor min_events 100, min_windows 4 (all three).

HOST "d155" -- the run_097-like host of the PR-C safety reviews (D-155's rates), copied
from their prc_sim.py (host_forecast, host_trade_windows) without change:
  - 6 windows x 240 daily bars, each its own iid Gaussian log-return walk (sd 0.035 per bar,
    zero drift: no edge anywhere), with 60 warm-up bars before each window;
  - forecast f_t = -clip(10 * r_t / std_60(r)_t, -20, 20), r = the 1-bar log return, std the
    60-bar trailing sample std (ddof 1) including bar t, min 30 bars (pandas rolling);
  - one lot per run of the same forecast sign: opened at the close of the first bar of the
    run, closed at the close of the bar where the sign changes (exit_cause "flip"), the last
    open lot closed at the window's last bar ("end_of_window"); full size, no rebalance
    band, no partial closes, so there are no "reduction" lots;
  - gross = side * (close[exit] / close[entry] - 1), cost a constant 0.002 per lot,
    net = gross - cost (basis all_costs); entry_forecast = f at the entry bar.
  On this host T2's baseline (`other_trades`, the non-flip lots) holds only the one
  end_of_window lot per window, whose post_exit_return is undefined (no bar after the
  window's last bar): T2 has no baseline and no per-window value by construction.

HOST "lifo" -- added for T2 only (also run for T1 and T3): the same paths and forecast, with
lots as the bot keeps them -- target allocation a_t = f_t / 10 (forecast_manager:
forecast / FORECAST_FOR_100_INVESTMENT), a rebalance when |a_t - held| >= 0.2 (risk
control min_allocation_change, threshold 0.20), the held allocation taken as the last
target traded to (no drift of the market-value allocation between bars); an increase on
the same side opens a new lot of the increase; a decrease on the same side closes lots
LIFO, a lot partly closed giving one record for the closed part (its entry bar kept) and
staying open for the rest; a sign change closes every lot then opens one of |a_t|. Every
record costs a constant 0.002; exit_cause comes from claim_tests.classify_exit (exit
forecast against side, then the post-rebalance allocation), so flip / reduction /
end_of_window all occur.

Mechanism numbers (per window, per test selector, on the claimed direction's outcome): the
selected lots' count N and sum S of the outcome, mean S/N, the baseline mean, the
correlation of S and N, and, for each selected lot, the selected lots opened from its
entry to 8 bars after its exit, split by the sign of its own outcome. For the two
trade_net_return tests also: the same mean difference with each lot's result taken as the
side-signed LOG price move minus the cost (symmetric between long and short).

DRIFT control (--drift): "log0" (the D-155 host, a zero-drift log walk) or "arith0" (log
returns with mean -sd^2/2, an arithmetic martingale: E[close[t+1] / close[t]] = 1). Same
seeds, so the two are the same draws shifted by a constant: a one-change control.

Run (Git Bash, from the repo root, the venv's interpreter, under the shared test lock;
chunk the sims with --chunk, each chunk its own seed, then --merge):
  python strategy-research/engineering/FOLD-FLOORS-2/trade_null_sim.py \
      --tools <r5 worktree>/strategy-research/tools --host d155 --drift log0 --sims 500 \
      --chunk 0 --out <dir>/trade_d155_log0_c0.pkl
  python .../trade_null_sim.py --merge <dir>/trade_d155_log0_c*.pkl --out results/trade_null_d155_log0.yaml
"""
from __future__ import annotations

import argparse
import math
import sys
import time
from pathlib import Path

import numpy as np
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ff2_common as fc  # noqa: E402

SEED = 20261020
SD, STEP, T0, WARM = 0.035, 86400, 1577836800, 60
COST = 0.002
K, N = 6, 240
BAND = 0.2
FORECAST_FOR_100 = 10.0
FLOOR = {"min_events": 100, "min_windows": 4}
#: per-bar mean of the log return: 0 ("log0", the D-155 host: a zero-drift LOG walk, whose
#: price rises by sd^2/2 per bar in arithmetic terms) or -sd^2/2 ("arith0": an arithmetic
#: martingale, E[close[t+1] / close[t]] = 1; the one-change control of the drift)
DRIFTS = {"log0": 0.0, "arith0": -SD * SD / 2.0}
MU = 0.0

RECORDED_HASH = {
    "T1_short_net": "05508ac0c6df321b1ff06d30f20ad42e37e052a8924a700e79fa77f8931c2951",
    "T2_flip_post_exit": "c609a010c712c29acad11eeee063bf8d0a5b5c05a0b801ce83df3f52acb4aeb7",
    "T3_strong_long_net": "70837262630bcfce9f4373dd633c9ab654e12dc62b69ed280f137805a7d6be5e",
}
CLAIMED = {"T1_short_net": "less", "T2_flip_post_exit": "greater", "T3_strong_long_net": "greater"}


def spec(key, direction):
    if key == "T1_short_net":
        return {"name": "shorts_earn_less_than_other_lots",
                "selector": {"kind": "trade", "where": [{"field": "side", "op": "==", "value": "short"}]},
                "outcome": {"kind": "trade_net_return"}, "baseline": {"kind": "other_trades"},
                "statistic": "mean_diff", "direction": direction, "floor": dict(FLOOR)}
    if key == "T2_flip_post_exit":
        return {"name": "flip_closed_lots_continue",
                "selector": {"kind": "trade", "where": [{"field": "exit_cause", "op": "==", "value": "flip"}]},
                "outcome": {"kind": "post_exit_return", "horizons": [1, 6, 24]},
                "baseline": {"kind": "other_trades"}, "statistic": "hit_rate",
                "direction": direction, "floor": dict(FLOOR)}
    if key == "T3_strong_long_net":
        return {"name": "strong_long_entries_earn_more",
                "selector": {"kind": "trade", "where": [{"field": "entry_forecast", "op": ">=", "value": 10}]},
                "outcome": {"kind": "trade_net_return"}, "baseline": {"kind": "other_trades"},
                "statistic": "mean_diff", "direction": direction, "floor": dict(FLOOR)}
    raise KeyError(key)


# ----------------------------- the d155 host (copied from prc_sim.py) -------------------

def host_forecast(r):
    """Vectorised host forecast (pandas rolling std, ddof=1, incl. bar t)."""
    import pandas as pd
    s = pd.Series(r).rolling(60, min_periods=30).std(ddof=1).to_numpy()
    return -np.clip(10.0 * r / s, -20, 20)


def host_path(ct, rng, i, n=N):
    r = rng.normal(MU, SD, n + WARM)
    close_all = 100.0 * np.exp(np.cumsum(r))
    f_all = host_forecast(r)
    close, f = close_all[WARM:], f_all[WARM:]
    ts = (T0 + i * (n + 10) * STEP + np.arange(n) * STEP).astype(np.int64)
    bars = ct.Window("SIM", f"w{i}", ts, close, f, np.array(["unknown"] * n, dtype=object), STEP)
    return bars, close, f, ts


def _tw(ct, bars, ts, ent, ext, side, cause, efc, gross):
    ent, ext = np.asarray(ent, dtype=np.int64), np.asarray(ext, dtype=np.int64)
    cost = np.full(len(ent), COST)
    return ct.TradeWindow(bars=bars, entry_ts=ts[ent], exit_ts=ts[ext], side=np.array(side, dtype=object),
                          exit_cause=np.array(cause, dtype=object),
                          regime_at_entry=np.array(["unknown"] * len(ent), dtype=object),
                          entry_forecast=np.array(efc, dtype=float), entry_idx=ent, exit_idx=ext,
                          net_return=np.asarray(gross, dtype=float) - cost, basis="all_costs")
    # (prc_sim also passed gross_return / cost, fields of the PR-C branch's TradeWindow that
    # R5's claim_tests does not have; none of the three tests reads them)


def d155_window(ct, rng, i, n=N):
    """prc_sim.host_trade_windows, one window, unchanged."""
    bars, close, f, ts = host_path(ct, rng, i, n)
    sg = np.sign(f)
    ent, ext, side, cause, efc = [], [], [], [], []
    t0 = 0
    for t in range(1, n):
        if sg[t] != sg[t0]:
            if sg[t0] != 0:
                ent.append(t0); ext.append(t); side.append("long" if sg[t0] > 0 else "short")
                cause.append("flip"); efc.append(f[t0])
            t0 = t
    if sg[t0] != 0 and t0 < n - 1:
        ent.append(t0); ext.append(n - 1); side.append("long" if sg[t0] > 0 else "short")
        cause.append("end_of_window"); efc.append(f[t0])
    ent_a, ext_a = np.array(ent, dtype=np.int64), np.array(ext, dtype=np.int64)
    sgn = np.where(np.array(side) == "long", 1.0, -1.0)
    gross = sgn * (close[ext_a] / close[ent_a] - 1.0)
    return _tw(ct, bars, ts, ent, ext, side, cause, efc, gross)


def lifo_window(ct, rng, i, n=N):
    """The 'lifo' host (module docstring)."""
    bars, close, f, ts = host_path(ct, rng, i, n)
    held = 0.0
    lots = []                                  # stack of [entry_idx, side_sign, size]
    recs = []                                  # (entry, exit, side_sign, cause)

    def close_size(t, amount, post):
        while amount > 1e-12 and lots:
            e, sgn, size = lots[-1]
            take = min(size, amount)
            recs.append((e, t, sgn, post))
            amount -= take
            if take >= size - 1e-12:
                lots.pop()
            else:
                lots[-1][2] = size - take

    for t in range(n):
        if not np.isfinite(f[t]):
            continue
        a = f[t] / FORECAST_FOR_100
        if t == n - 1:
            break
        if abs(a - held) < BAND:
            continue
        if held != 0 and (a == 0 or np.sign(a) != np.sign(held)):
            close_size(t, abs(held), a)
            held = 0.0
        if held == 0 or np.sign(a) == np.sign(held):
            if abs(a) > abs(held):
                lots.append([t, 1 if a > 0 else -1, abs(a) - abs(held)])
            elif abs(a) < abs(held):
                close_size(t, abs(held) - abs(a), a)
        held = a
    for e, sgn, _size in lots[::-1]:
        recs.append((e, n - 1, sgn, held))
    recs.sort(key=lambda r: (r[1], r[0]))
    ent, ext, side, cause, efc, gross = [], [], [], [], [], []
    for e, x, sgn, post in recs:
        if x <= e:
            continue
        ent.append(e); ext.append(x); side.append("long" if sgn > 0 else "short")
        cause.append(ct.classify_exit(sgn, f[x], post, True, x == n - 1))
        efc.append(f[e])
        gross.append(sgn * (close[x] / close[e] - 1.0))
    return _tw(ct, bars, ts, ent, ext, side, cause, efc, gross)


HOSTS = {"d155": d155_window, "lifo": lifo_window}


# ----------------------------- mechanism -------------------------------------------------

def mechanism_window(ct, tw, test, h):
    """(N, S, mean_sel, mean_base, after_pos, after_neg) of one window, claimed-direction
    orientation is NOT applied (raw outcome). For post_exit_return the selected / baseline
    lots are de-duplicated per exit bar and side as claim_tests does."""
    sp = test
    mask, valid = ct.sel_trade(tw, sp["selector"])
    mask = mask & valid
    wref = (valid & ~mask).astype(float)
    kind = sp["outcome"]["kind"]
    if kind != "trade_net_return":
        mask, wref = ct._one_event_per_exit(tw, mask, wref)
    y = ct.trade_outcome(tw, kind, h)
    ev = mask & np.isfinite(y)
    base = (wref > 0) & np.isfinite(y)
    n, s = int(ev.sum()), float(y[ev].sum()) if ev.any() else 0.0
    after_pos, after_neg = [], []
    ent, ext = tw.entry_idx, tw.exit_idx
    for i in np.nonzero(ev)[0]:
        nxt = int(((ent > ent[i]) & (ent <= ext[i] + 8) & ev).sum())
        (after_pos if y[i] > 0 else after_neg).append(nxt)
    # the side-signed LOG price move of the lot minus the cost: the same comparison with each
    # lot's result symmetric between long and short (a short's arithmetic return 1 - e^R is not
    # the mirror of a long's e^R - 1)
    sgn = np.where(np.asarray(tw.side) == "long", 1.0, -1.0)
    ly = (sgn * np.log(tw.bars.close[tw.exit_idx] / tw.bars.close[tw.entry_idx]) - COST
          if kind == "trade_net_return" else np.full(len(y), np.nan))
    ldiff = (float(ly[ev].mean() - ly[base].mean()) if (ev.any() and base.any()
             and kind == "trade_net_return") else np.nan)
    return (n, s, float(y[ev].mean()) if n else np.nan,
            float(y[base].mean()) if base.any() else np.nan, int(base.sum()), after_pos, after_neg,
            ldiff)


# ----------------------------- the run ----------------------------------------------------

def run(ct, cmeas, fcf, host, sims, chunk):
    labels = [f"w{i}" for i in range(K)]
    rng = np.random.default_rng([SEED, 100 + list(HOSTS).index(host), chunk])
    tests = {}
    for key in RECORDED_HASH:
        for d in ("less", "greater"):
            t = spec(key, d)
            _s, hsh = cmeas.test_spec(t, True)
            if d == CLAIMED[key]:
                assert hsh == RECORDED_HASH[key], (key, hsh)
            tests[f"{key}|{d}"] = t
    acc = {name: {"confirmed": 0, "status": {}, "win_pos": {}, "win_tot": {}, "lots": [],
                  "floor_not_met": 0, "pooled": {}} for name in tests}
    mech = {key: {"N": [], "S": [], "mean_sel": [], "mean_base": [], "n_base": [], "ldiff": [],
                  "after_pos": [], "after_neg": []} for key in RECORDED_HASH}
    hist = {"lots_per_window": [], "causes": {}}
    for s in range(sims):
        tws = [HOSTS[host](ct, rng, i) for i in range(K)]
        for tw in tws:
            hist["lots_per_window"].append(tw.n)
            for c in tw.exit_cause:
                hist["causes"][str(c)] = hist["causes"].get(str(c), 0) + 1
        for name, test in tests.items():
            res = cmeas.measure_test(tws, test, None, trade_tests=True)
            g = fcf.grade_test(res, fold_windows=labels)
            a = acc[name]
            a["confirmed"] += int(g["status"] == fcf.CONFIRMED)
            a["status"][g["status"]] = a["status"].get(g["status"], 0) + 1
            a["floor_not_met"] += int(bool(res.get("floor_not_met")))
            for h, r in (res.get("horizons") or {}).items():
                hk = str(h)
                a["win_pos"].setdefault(hk, 0)
                a["win_tot"].setdefault(hk, 0)
                a["pooled"].setdefault(hk, [])
                for c in r["per_window"].values():
                    if c["oriented"] is not None:
                        a["win_tot"][hk] += 1
                        a["win_pos"][hk] += int(c["oriented"] > 0)
                a["pooled"][hk].append(r["oriented"] if r["oriented"] is not None else np.nan)
                if hk == str(min(res["horizons"])):
                    a["lots"].append(r["n_events"])
        for key in RECORDED_HASH:
            t = tests[f"{key}|{CLAIMED[key]}"]
            hs = t["outcome"].get("horizons") or [0]
            for tw in tws:
                for h in hs:
                    n, sm, msel, mbase, nb, ap, an, ld = mechanism_window(ct, tw, t, h)
                    m = mech[key]
                    m.setdefault("h", [])
                    m["h"].append(h)
                    m["N"].append(n); m["S"].append(sm); m["mean_sel"].append(msel)
                    m["mean_base"].append(mbase); m["n_base"].append(nb); m["ldiff"].append(ld)
                    m["after_pos"].append(ap); m["after_neg"].append(an)
    return {"acc": acc, "mech": mech, "hist": hist, "sims": sims}


def _share_below(x):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    return fc.rate(int((x < 0).sum()), len(x)) if len(x) else None


def summarise(parts):
    sims = sum(p["sims"] for p in parts)
    out = {"sims": sims, "tests": {}, "mechanism": {}}
    names = list(parts[0]["acc"])
    for name in names:
        conf = sum(p["acc"][name]["confirmed"] for p in parts)
        status, wp, wt, pooled = {}, {}, {}, {}
        for p in parts:
            a = p["acc"][name]
            for k, v in a["status"].items():
                status[k] = status.get(k, 0) + v
            for hk in a["win_tot"]:
                wp[hk] = wp.get(hk, 0) + a["win_pos"][hk]
                wt[hk] = wt.get(hk, 0) + a["win_tot"][hk]
                pooled.setdefault(hk, []).extend(a["pooled"][hk])
        lots = [x for p in parts for x in p["acc"][name]["lots"]]
        fnm = sum(p["acc"][name]["floor_not_met"] for p in parts)
        out["tests"][name] = {
            "confirm_R5": fc.rate(conf, sims),
            "status": dict(sorted(status.items())),
            "floor_not_met_share": fc.rate(fnm, sims),
            "per_window_claimed_sign": {hk: fc.rate(wp[hk], wt[hk]) for hk in sorted(wt, key=float)},
            "windows_with_value_per_fold": {hk: round(wt[hk] / sims, 2) for hk in sorted(wt, key=float)},
            "pooled_oriented": {hk: fc.ms(pooled[hk]) for hk in sorted(pooled, key=float)},
            "selected_lots_per_fold": round(float(np.mean(lots)), 1) if lots else None}
    for key in parts[0]["mech"]:
        m = {k: [x for p in parts for x in p["mech"][key].get(k, [])] for k in
             ("h", "N", "S", "mean_sel", "mean_base", "n_base", "after_pos", "after_neg", "ldiff")}
        res = {}
        for h in sorted(set(m["h"])):
            idx = [i for i, x in enumerate(m["h"]) if x == h]
            N_ = np.array([m["N"][i] for i in idx], float)
            S_ = np.array([m["S"][i] for i in idx], float)
            Ms = np.array([m["mean_sel"][i] for i in idx], float)
            Mb = np.array([m["mean_base"][i] for i in idx], float)
            ok = N_ > 0
            ap = [x for i in idx for x in m["after_pos"][i]]
            an = [x for i in idx for x in m["after_neg"][i]]
            res[str(h)] = {
                "windows": int(len(idx)),
                "selected_lots_per_window": fc.ms(N_),
                "baseline_lots_per_window": fc.ms([m["n_base"][i] for i in idx]),
                "sum_S": fc.ms(S_[ok]),
                "ratio_sumS_over_sumN": round(float(S_[ok].sum() / N_[ok].sum()), 6) if ok.any() else None,
                "mean_of_S_over_N": fc.ms(Ms),
                "mean_of_baseline_mean": fc.ms(Mb),
                "mean_diff_sel_minus_base": fc.ms(Ms - Mb),
                "mean_diff_signed_log_move_sel_minus_base": fc.ms([m["ldiff"][i] for i in idx]),
                "share_windows_diff_below_0": _share_below([Ms[j] - Mb[j] for j in range(len(idx))]),
                "share_windows_signed_log_move_diff_below_0": _share_below([m["ldiff"][i] for i in idx]),
                "corr_S_N": (round(float(np.corrcoef(S_[ok], N_[ok])[0, 1]), 4)
                             if ok.sum() > 2 and np.std(N_[ok]) > 0 else None),
                "selected_lots_opened_entry_to_exit_plus_8_after_own_outcome_up": fc.ms(ap),
                "selected_lots_opened_entry_to_exit_plus_8_after_own_outcome_down": fc.ms(an)}
        out["mechanism"][key] = res
    lots = [x for p in parts for x in p["hist"]["lots_per_window"]]
    causes = {}
    for p in parts:
        for k, v in p["hist"]["causes"].items():
            causes[k] = causes.get(k, 0) + v
    out["host_lots_per_window"] = fc.ms(lots)
    tot = sum(causes.values())
    out["host_exit_causes_share"] = {k: round(v / tot, 4) for k, v in sorted(causes.items())}
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--tools", type=Path)
    ap.add_argument("--host", choices=list(HOSTS), default="d155")
    ap.add_argument("--drift", choices=list(DRIFTS), default="log0")
    ap.add_argument("--sims", type=int, default=500)
    ap.add_argument("--chunk", type=int, default=0)
    ap.add_argument("--merge", nargs="*", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    if a.merge:
        import pickle
        parts, meta = [], None
        for p in a.merge:
            doc = pickle.loads(Path(p).read_bytes())
            parts.append(doc["raw"])
            meta = meta or doc["meta"]
            assert doc["meta"]["host"] == meta["host"] and doc["meta"]["drift"] == meta["drift"] and doc["meta"]["tools"] == meta["tools"]
        chunks = sorted(pickle.loads(Path(p).read_bytes())["meta"]["chunk"] for p in a.merge)
        assert len(set(chunks)) == len(chunks), "a chunk merged twice"
        out = {"script": "trade_null_sim.py", **{k: v for k, v in meta.items() if k != "chunk"},
               "chunks": chunks, "seconds": round(sum(pickle.loads(Path(p).read_bytes())["meta"]["seconds"]
                                                      for p in a.merge), 1),
               **summarise(parts)}
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(yaml.safe_dump(out, sort_keys=False), encoding="utf-8")
        for name, r in out["tests"].items():
            wins = "  ".join(f"h{hk} {v['rate']}" for hk, v in r["per_window_claimed_sign"].items())
            print(f"{name:30s} R5 {r['confirm_R5']['rate']:.4f}±{r['confirm_R5']['se']:.4f}  win+ {wins}"
                  f"  lots {r['selected_lots_per_fold']}  {r['status']}")
        return 0
    if a.tools is None:
        ap.error("--tools is required")
    global MU
    MU = DRIFTS[a.drift]
    ct, cmeas, fcf = fc.load_tools(a.tools)
    t = time.time()
    raw = run(ct, cmeas, fcf, a.host, a.sims, a.chunk)
    import pickle
    meta = {"host": a.host, "drift": a.drift, "mu_per_bar": MU, "tools": str(a.tools.resolve()), "seed": [SEED, 100 + list(HOSTS).index(a.host)],
            "chunk": a.chunk, "sims_chunk": a.sims, "seconds": round(time.time() - t, 1),
            "layout": {"windows": K, "bars": N, "warmup": WARM, "sd": SD, "cost": COST,
                       "band": BAND if a.host == "lifo" else None}}
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_bytes(pickle.dumps({"meta": meta, "raw": raw}))
    print(f"host {a.host} chunk {a.chunk} sims {a.sims} {meta['seconds']}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
