"""FOLD-FLOORS-2 (b) and (c) on real returns: cell A of #495 on sign-shuffled blocks of the
campaign coins' daily returns, and the remedies' false-confirm rate and power there.

THE ONE PLACE THIS REPORT READS MARKET DATA (authorised by the operator 2026-10-20, "through
the normal data path"). Rules kept by the code below:
  * the normal data path: trading-bot DataManager(symbols=[coin], interval_seconds=86400,
    mode="backtest").fetch_historical_data(coin, start, end, exchange=<venue>) -- the call
    the backtester's load_data makes for each window -- with its own seal guards on
    (allow_sealed False);
  * cache only: before any load, CcxtFetcher._fetch_remote and BaseFetcher._merge_and_store
    are replaced by functions that record the call and raise, and socket connections raise;
    after each load the script STOPS (a STOP message, exit 1, nothing written) if either was called: the
    loader would have fetched or written, i.e. a window is not fully in the cache;
  * every window must come back whole: one bar per day from its first to its last day, no gap
    (else STOP, exit 1); with --skip-incomplete, a coin-fold with such a window is instead
    EXCLUDED (listed under excluded_coin_folds, its message carrying coin, fold and window
    index only) and the other coin-folds are measured: nothing is fetched, filled or graded on
    a window with a hole;
  * exploration windows only: the windows are folds A, B and C of config/folds.yaml, read
    through tools/research_folds.load_folds, which refuses any block outside the research
    period or touching the validation period or the holdout, all three read from
    config/campaign_data_policy.yaml (fold D, which lies in the validation period, is not
    used); holdout_policy.check_windows_before(windows, holdout start) must pass too;
  * no bar at or after the policy's holdout start: asserted on every request end and on
    every returned bar (exit 4 otherwise, nothing written);
  * NO DATE is printed, logged or written: the data path's logging is disabled and its
    stdout / stderr discarded during each load; right after the checks every window's
    timestamps are replaced by a synthetic daily grid, windows are named
    "<fold><index>" (A0..C5) and coins by symbol; error messages carry no date.

Campaign coins: config/campaign_config.yaml holds no coin list (verified); the coins are the
active daily briefs' set (briefs/L1_daily_trend_basket_sma50_v3.md and its sma100 / sma200
and refold siblings: BTCUSDT, ETHUSDT, LTCUSDT on venue kraken, product perp, timeframe 1d),
mapped to the venue's symbols by tools/venue_resolver.protocol_keys (BTCUSD, ETHUSD, LTCUSD).

The null: within each window, the daily log returns (close to close inside the window) are
cut into consecutive blocks of 5 bars (claim_tests.BLOCK_BARS["daily"], the block of
claim_tests.fake_window) starting at a random phase, each block's sign is flipped with
probability 1/2, and the path is rebuilt from the window's first close. Volatility and its
clustering within a block are kept; drift and direction are removed. One fold = the 6
windows of one config fold for one coin (labels A0..A5 etc.), graded as one-coin folds.

Cell A (#495): past_return(5) >= +5% event, fwd_return h=3, mean_diff vs the complement,
floor min_events 100 / min_windows 4, both directions; "pass" = R5's
fold_confirm.grade_test(result, fold_windows=the fold's 6 labels) == confirmed, with the
claim_tests / claim_measure blocks of --tools: run with
--tools <worktree of PR #496 (claims/fold-confirm-r5)>/strategy-research/tools.
Remedies (ff2_common docstring): rem1a / rem1b one value per non-overlapping stretch;
rem2_pooled / rem2_share a simulated null per selector, whose reference is --ref-sims
sign-shuffles of the SAME coin and fold with an independent seed. Planted effects 1% and
2%: delta in the claimed direction added to the selected bars' tool outcome.

Run (Git Bash, from the repo root, the venv's interpreter, under the shared test lock):
  python strategy-research/engineering/FOLD-FLOORS-2/real_return_null.py \
      --tools <r5 worktree>/strategy-research/tools --sims 2000 --ref-sims 2000 --check 50 \
      --out <dir>/real_return_null.yaml
"""
from __future__ import annotations

import argparse
import contextlib
import io
import logging
import socket
import sys
import time
from pathlib import Path

import numpy as np
import yaml

HERE = Path(__file__).resolve().parent
SR = HERE.parents[1]                        # strategy-research/
TBOT = SR.parent / "trading-bot"
sys.path.insert(0, str(HERE))
import ff2_common as fc  # noqa: E402

SEED = 20261020
COINS = ["BTCUSDT", "ETHUSDT", "LTCUSDT"]
BRIEF_VENUE = {"venue": "kraken", "product": "perp"}
FOLDS = ("A", "B", "C")
DAY = 86400
T0 = 1577836800                              # the synthetic grid's origin (not a market date)
EDGES = (0.0, 0.01, 0.02)
DIRS = ("less", "greater")


class Stop(SystemExit):
    pass


def _epoch_day(day: str) -> int:
    import pandas as pd
    return int(pd.Timestamp(day, tz="UTC").timestamp())


def load_real(coins, folds_path, policy_path, skip_incomplete=False):
    """{(coin, fold): [close array per window]} through the normal data path, cache only.
    Every check fails loud with a message that carries no date."""
    import holdout_policy as hp
    import research_folds as rf
    import venue_resolver as vr
    doc = rf.load_folds(folds_path, policy_path=policy_path)
    policy = hp.load_policy(policy_path)
    hstart = hp.holdout_start_of(policy)
    bound = _epoch_day(hstart)
    keys = vr.protocol_keys(BRIEF_VENUE, coins)
    exchange, symbols = keys["exchange"], keys["symbols"]
    sys.path.insert(0, str(TBOT))
    from data import data_manager as dmm
    from data.fetchers import base_fetcher as bf
    from data.fetchers import ccxt_fetcher as cf
    calls = []

    def no_fetch(self, *a, **k):
        calls.append("fetch")
        raise RuntimeError("FOLD-FLOORS-2: network fetch refused (cache-only read)")

    def no_store(self, *a, **k):
        calls.append("store")
        raise RuntimeError("FOLD-FLOORS-2: cache write refused (cache-only read)")

    def no_connect(self, *a, **k):
        calls.append("socket")
        raise OSError("FOLD-FLOORS-2: network refused")

    cf.CcxtFetcher._fetch_remote = no_fetch
    bf.BaseFetcher._merge_and_store = no_store
    socket.socket.connect = no_connect
    out = {}
    excluded = {}
    windows_seen = {}
    for fid in FOLDS:
        wins = rf.fold_windows(doc, fid)
        hp.check_windows_before(wins, hstart)
        windows_seen[fid] = len(wins)
        for coin, sym in zip(coins, symbols):
            try:
                out[(coin, fid)] = _load_fold(dmm, coin, sym, fid, wins, exchange, bound, calls)
            except Stop as exc:
                if not skip_incomplete:
                    raise
                excluded[f"{coin}|{fid}"] = str(exc)
    return out, {"exchange": exchange, "symbols": dict(zip(coins, symbols)),
                 "windows_per_fold": windows_seen, "excluded_coin_folds": excluded}


def _load_fold(dmm, coin, sym, fid, wins, exchange, bound, calls):
    """The 6 windows of one coin and fold, each checked (module docstring)."""
    closes = []
    for j, w in enumerate(wins):
        start, end = w["test"]["start"], w["test"]["end"]
        s_ep, e_ep = _epoch_day(start), _epoch_day(end)
        if not (e_ep + DAY <= bound):
            raise SystemExit(4)   # a window reaching the holdout start: never loaded
        n_calls = len(calls)
        logging.disable(logging.CRITICAL)
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                dm = dmm.DataManager(symbols=[sym], interval_seconds=DAY, mode="backtest")
                df = dm.fetch_historical_data(sym, start, end, exchange=exchange)
        finally:
            logging.disable(logging.NOTSET)
        where = f"coin {coin} fold {fid} window {j}"
        if len(calls) > n_calls:
            raise Stop(f"STOP: the loader would {sorted(set(calls[n_calls:]))} for {where} "
                       f"(not fully in the cache); nothing written")
        if df is None or df.empty:
            raise Stop(f"STOP: no rows for {where}; nothing written")
        import pandas as pd
        ts = (pd.to_datetime(df["timestamp"], utc=True).astype("int64") // 10 ** 9).to_numpy()
        if len(ts) and int(ts.max()) >= bound:
            raise SystemExit(4)   # a bar at or after the holdout start came back
        close = df["close"].astype(float).to_numpy()
        n_exp = (e_ep - s_ep) // DAY + 1
        if not (len(ts) == n_exp and ts[0] == s_ep and np.all(np.diff(ts) == DAY)
                and np.all(np.isfinite(close)) and np.all(close > 0)):
            raise Stop(f"STOP: {where} is not whole ({len(ts)} rows, {n_exp} days expected, "
                       f"gaps or bad closes); nothing written")
        closes.append(close)
        del df, ts
    return closes


def shuffled(ct, closes, coin, fid, rng, B):
    ws = []
    for j, c in enumerate(closes):
        r = np.diff(np.log(c))
        phase = int(rng.integers(0, B))
        blk = (np.arange(len(r)) + (B - phase)) // B          # block id, first block of `phase` rows
        s = rng.choice([-1.0, 1.0], size=int(blk.max()) + 1)[blk]
        close = c[0] * np.exp(np.r_[0.0, np.cumsum(s * r)])
        n = len(close)
        ts = (T0 + (j * 200 + np.arange(n)) * DAY).astype(np.int64)
        ws.append(ct.Window(coin, f"{fid}{j}", ts, close, np.full(n, np.nan),
                            np.array(["unknown"] * n, dtype=object), DAY))
    return ws


def run(ct, cmeas, fcf, data, sims, ref_sims, check, B, coins):
    out = {}
    for ci, (key, closes) in enumerate(sorted(data.items())):
        coin, fid = key
        labels = [f"{fid}{j}" for j in range(len(closes))]
        fi = FOLDS.index(fid)
        rng = np.random.default_rng([SEED, 1, coins.index(coin), fi])
        ref = {d: fc.Tally(len(closes)) for d in DIRS}
        for _ in range(ref_sims):
            ws = shuffled(ct, closes, coin, fid, rng, B)
            for d in DIRS:
                ref[d].add(fc.cell_a_fold(ct, cmeas, fcf, ws, d, labels))
        refs = {d: ref[d].reference() for d in DIRS}
        rng = np.random.default_rng([SEED, 2, coins.index(coin), fi])
        cells = {f"{'null' if e == 0 else f'edge{e}'}|{d}": fc.Tally(len(closes), refs[d])
                 for e in EDGES for d in DIRS}
        for s in range(sims):
            ws = shuffled(ct, closes, coin, fid, rng, B)
            for e in EDGES:
                for d in DIRS:
                    cells[f"{'null' if e == 0 else f'edge{e}'}|{d}"].add(
                        fc.cell_a_fold(ct, cmeas, fcf, ws, d, labels, edge=e, check=(s < check and e == 0)))
        out[f"{coin}|{fid}"] = {"bars_per_window": [int(len(c)) for c in closes],
                                "reference": refs,
                                "cells": {k: v.summary() for k, v in cells.items()},
                                "_tallies": cells}
        c = out[f"{coin}|{fid}"]["cells"]
        print(f"{coin} {fid}: " + "  ".join(
            f"{k} win+ {v['per_window_claimed_sign']['rate']:.3f} R5 {v['confirm']['R5']['rate']:.3f}"
            f" r1a {v['confirm']['rem1a']['rate']:.3f} r1b {v['confirm']['rem1b']['rate']:.3f}"
            f" r2p {v['confirm']['rem2_pooled']['rate']:.3f}"
            for k, v in c.items() if k.startswith("null")), flush=True)
    return out


def pooled(out):
    """Every (coin, fold) cell summed: one rate per rule over all 9 folds."""
    tot = {}
    for v in out.values():
        for k, t in v["_tallies"].items():
            a = tot.setdefault(k, {"sims": 0, "conf": {r: 0 for r in fc.Tally.RULES},
                                   "wp": 0, "wt": 0})
            a["sims"] += t.sims
            for r in fc.Tally.RULES:
                a["conf"][r] += t.conf[r]
            a["wp"] += t.win_pos
            a["wt"] += t.win_tot
    return {k: {"folds_x_sims": a["sims"], "per_window_claimed_sign": fc.rate(a["wp"], a["wt"]),
                "confirm": {r: fc.rate(v, a["sims"]) for r, v in a["conf"].items()}}
            for k, a in tot.items()}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--tools", type=Path, required=True)
    ap.add_argument("--coins", nargs="+", default=COINS)
    ap.add_argument("--sims", type=int, default=2000)
    ap.add_argument("--ref-sims", type=int, default=2000)
    ap.add_argument("--check", type=int, default=0)
    ap.add_argument("--skip-incomplete", action="store_true",
                    help="a coin-fold with a window not fully in the cache (the loader would fetch, or "
                         "a gap) is EXCLUDED and listed instead of stopping the run; never fetched, "
                         "never filled")
    ap.add_argument("--block", type=int, default=None, help="block length (default claim_tests.BLOCK_BARS daily)")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    ct, cmeas, fcf = fc.load_tools(a.tools)
    B = a.block or ct.BLOCK_BARS["daily"]
    t0 = time.time()
    try:
        data, meta = load_real(a.coins, SR / "config" / "folds.yaml", SR / "config" / "campaign_data_policy.yaml",
                               a.skip_incomplete)
    except SystemExit:
        raise
    except BaseException as exc:  # noqa: BLE001 -- the message may carry a date: name only
        raise Stop(f"STOP: loading failed with {type(exc).__name__} (message withheld: it may carry a date); "
                   f"nothing written")
    t1 = time.time()
    print(f"loaded {len(data)} coin-folds, {sum(len(v) for v in data.values())} windows "
          f"({t1 - t0:.0f}s); exchange {meta['exchange']}, symbols {meta['symbols']}", flush=True)
    res = run(ct, cmeas, fcf, data, a.sims, a.ref_sims, a.check, B, list(a.coins))
    t2 = time.time()
    doc = {"script": "real_return_null.py", "tools": str(a.tools.resolve()),
           "coins": list(a.coins), **meta, "folds": list(FOLDS), "block_bars": B,
           "seed": SEED, "sims": a.sims, "ref_sims": a.ref_sims, "check_sims_full_chain": a.check,
           "cell": "A: past_return(5) >= +0.05, fwd_return h=3, mean_diff vs complement",
           "floor": fc.FLOOR, "spacing_remedy1": fc.SPACING,
           "per_coin_fold": {k: {kk: vv for kk, vv in v.items() if kk != "_tallies"} for k, v in res.items()},
           "all_coin_folds": pooled(res),
           "seconds": {"load": round(t1 - t0, 1), "simulate": round(t2 - t1, 1)}}
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    for k, v in doc["all_coin_folds"].items():
        c = v["confirm"]
        print(f"ALL {k:16s} win+ {v['per_window_claimed_sign']['rate']:.3f}  R5 {c['R5']['rate']:.4f}"
              f"  r1a {c['rem1a']['rate']:.4f}  r1b {c['rem1b']['rate']:.4f}"
              f"  r2p {c['rem2_pooled']['rate']:.4f}  r2s {c['rem2_share']['rate']:.4f}")
    print(f"total {t2 - t0:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
