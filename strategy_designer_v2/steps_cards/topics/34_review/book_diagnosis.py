"""The diagnosis of a backtest's book: why it does or does not pay (definition: topics/34_review/book_diagnosis.md, topic 34; a discovery tool, not a step).
Reads one backtest record and the idea's horizon from its plan; writes diagnosis.json and diagnosis.md into the record.
An observation: it refuses nothing, it changes no decision, no model call.

  python book_diagnosis.py path/to/04_backtest/<run>/backtests/<record> [--horizon H] [--out-dir DIR]

The horizon is the plan's "Horizon: N" line (the plan named in the record's run.md), unless --horizon is given.
Decided (operator, 2026-11-20): a forecast that stays on with no new rise counts as past its bets; every bet is read
(bets overlap, only averages are given); numbers only, no threshold.

Why this can't leak: it reads a finished backtest after the fact and changes nothing the strategy decided.
"""
import argparse, json, math, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))
from lib import write_atomic  # noqa: E402
from bets import bets, band_of  # noqa: E402,F401

import numpy as np
import pandas as pd

COLS = ["timestamp", "close", "forecast", "previous_allocation", "postRebalance_current_allocation",
        "postRebalance_total_value"]


def horizon_of(record):
    """The idea's horizon in bars: the 'Horizon: N' line of the plan the record's run.md names."""
    run = (record / "run.md").read_text()
    m = re.search(r"^- Plan: `([^`]+)`", run, re.M)
    if not m:
        raise SystemExit(f"{record.name}: run.md names no plan; give --horizon")
    plan = (record / m.group(1)).resolve()
    h = re.search(r"Horizon:\s*(\d+)", plan.read_text())
    if not h:
        raise SystemExit(f"{record.name}: the plan has no 'Horizon: N' line; give --horizon")
    return int(h.group(1))


def read_coin(coin_dir):
    """The coin's windows (a list of frames, in window order) and its drift: the mean return per bar over all windows."""
    wins = sorted(coin_dir.glob("w*/bars.csv.gz"), key=lambda p: int(p.parent.name[1:]))
    frames = [pd.read_csv(f, usecols=COLS) for f in wins]
    rets = np.concatenate([f["close"].pct_change().to_numpy()[1:] for f in frames]) if frames else np.array([])
    return frames, (float(rets.mean()) if len(rets) else 0.0)


def diagnose_coin(frames, d, H, band=0.2):
    """The sums one coin gives; the readings are formed from them (per coin, and over all coins together)."""
    acc = {"bets": 0, "move": [], "bar0": [], "path": [], "units": 0.0, "free": 0.0, "real": 0.0,
           "in_bars": 0, "past_bars": 0, "earn_cov": 0.0, "pos_cov": 0.0, "earn_past": 0.0, "pos_past": 0.0}
    drift = lambda k: (1 + d) ** k - 1
    for f in frames:
        c = f["close"].to_numpy(float); fc = f["forecast"].fillna(0).to_numpy(float)
        a = f["postRebalance_current_allocation"].fillna(0).to_numpy(float)
        prev = f["previous_allocation"].fillna(0).to_numpy(float)
        v = f["postRebalance_total_value"].to_numpy(float)
        n = len(c)
        nxt = np.append(c[1:] / c[:-1] - 1, 0.0)                         # the coin's return from t's close to t+1's
        # costs: the book without costs minus the backtest's own book, per unit traded
        acc["units"] += float(np.abs(a - prev).sum())
        acc["free"] += float((a[:-1] * nxt[:-1]).sum())
        acc["real"] += float((v[1:] / v[:-1] - 1).sum())
        # every bet with 2H bars after it in the window (bets overlap; each is a bet the book takes; averages only)
        b = bets(fc, band)
        for t in b:
            if t < 1 or t + 2 * H >= n:
                continue
            s = np.sign(fc[t])
            acc["bets"] += 1
            acc["move"].append(s * (c[t + H] / c[t] - 1 - drift(H)))
            acc["bar0"].append(s * (c[t] / c[t - 1] - 1 - d))
            acc["path"].append([s * (c[t + k] / c[t] - 1 - drift(k)) for k in range(1, 2 * H + 1)])
        # holding past the bets: a bar in a position is covered when a bet of the same side is at most H-1 bars old
        last = {1.0: -10**9, -1.0: -10**9}
        bset = set(b.tolist())
        for t in range(n - 1):
            if t in bset:
                last[float(np.sign(fc[t]))] = t
            side = float(np.sign(a[t]))
            if side == 0:
                continue
            acc["in_bars"] += 1
            gain = a[t] * (nxt[t] - d)
            if t - last[side] < H:
                acc["earn_cov"] += gain; acc["pos_cov"] += abs(a[t])
            else:
                acc["past_bars"] += 1; acc["earn_past"] += gain; acc["pos_past"] += abs(a[t])
    return acc


def daily_parts(frames, d):
    """Per window, per UTC day: the book's daily return (after costs) and its gain from the market's own rise
    (the position held x the coin's mean return per bar, summed over the day's bars)."""
    out = []
    for w, f in enumerate(frames):
        ts = pd.to_datetime(f["timestamp"], utc=True).dt.normalize()
        v = pd.Series(f["postRebalance_total_value"].to_numpy(float)).groupby(ts.to_numpy()).last()
        book = v.pct_change().dropna()
        a = pd.Series(f["postRebalance_current_allocation"].fillna(0).to_numpy(float) * d).groupby(ts.to_numpy()).sum()
        out.append(pd.DataFrame({"w": w, "book": book, "market": a.reindex(book.index)}))
    return pd.concat(out) if out else pd.DataFrame(columns=["w", "book", "market"])


def readings(acc, H):
    m = lambda x: float(np.mean(x)) if len(x) else None
    cost = (acc["free"] - acc["real"]) / acc["units"] if acc["units"] else None
    path = np.mean(np.array(acc["path"]), axis=0) if acc["path"] else None
    peak = int(np.argmax(path)) if path is not None else None
    return {
        "bets_read": acc["bets"],
        "1_big_enough": {"move_over_horizon": m(acc["move"]), "round_trip_cost": 2 * cost if cost is not None else None,
                         "cost_per_unit_traded": cost, "units_traded": acc["units"]},
        "2_opening_time": {"move_on_bar_0": m(acc["bar0"])},
        "3_closing_time": {"peak_bar": peak + 1 if peak is not None else None,
                           "move_at_peak": float(path[peak]) if path is not None else None,
                           "move_at_H": float(path[H - 1]) if path is not None else None,
                           "move_at_2H": float(path[-1]) if path is not None else None,
                           "path": [round(float(x), 6) for x in path] if path is not None else None},
        "4_holding_past_the_bets": {
            "bars_in_position": acc["in_bars"],
            "share_past_the_bets": acc["past_bars"] / acc["in_bars"] if acc["in_bars"] else None,
            "earned_per_bar_per_unit_covered": acc["earn_cov"] / acc["pos_cov"] if acc["pos_cov"] else None,
            "earned_per_bar_per_unit_past": acc["earn_past"] / acc["pos_past"] if acc["pos_past"] else None},
    }


def merge(accs):
    out = {k: ([] if isinstance(v, list) else 0) for k, v in accs[0].items()}
    for a in accs:
        for k, v in a.items():
            out[k] = out[k] + v
    return out


def diagnose(record, H):
    coins, accs, parts = {}, [], []
    for coin_dir in sorted(p for p in record.iterdir() if p.is_dir()):
        frames, d = read_coin(coin_dir)
        if not frames:
            continue
        acc = diagnose_coin(frames, d, H, band_of(record))
        accs.append(acc)
        coins[coin_dir.name] = readings(acc, H)
        dp = daily_parts(frames, d); dp["coin"] = coin_dir.name; parts.append(dp)
        coins[coin_dir.name]["5_trend"] = trend(dp)
    allp = pd.concat(parts)
    eq = allp.reset_index().groupby(["w", "index"])[["book", "market"]].mean()   # equal weight per day, like the book
    whole = readings(merge(accs), H)
    whole["5_trend"] = trend(eq)
    return {"horizon": H, "whole_book": whole, "per_coin": coins}


def trend(df):
    book, market = float(df["book"].mean()), float(df["market"].mean())
    return {"book_mean_daily_gain": book, "market_part": market, "timing_part": book - market,
            "market_share": market / book if book > 0 else None}


def bps(x):
    return "–" if x is None else f"{x * 1e4:.1f}"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("record", type=Path)
    p.add_argument("--horizon", type=int)
    p.add_argument("--out-dir", type=Path, help="write diagnosis.json and .md here instead of into the record")
    args = p.parse_args()
    record = args.record.resolve()
    H = args.horizon or horizon_of(record)
    res = diagnose(record, H)
    out = args.out_dir.resolve() if args.out_dir else record
    out.mkdir(parents=True, exist_ok=True)
    write_atomic(out / "diagnosis.json", json.dumps(res, indent=1) + "\n")
    w = res["whole_book"]; r1, r2, r3, r4, r5 = (w[k] for k in ("1_big_enough", "2_opening_time", "3_closing_time",
                                                               "4_holding_past_the_bets", "5_trend"))
    share = lambda x: "–" if x is None else f"{x * 100:.0f} %"
    lines = [f"# Diagnosis of {record.name}", "",
             f"Horizon {H} bars; {w['bets_read']} bets read. Definition: `common/book_diagnosis.md`.",
             "Moves are in the bet's direction, minus the coin's drift, in bps of the price.", "",
             "| Reading | Value |", "|---|---|",
             f"| 1. Big enough: move over the horizon / round trip cost | {bps(r1['move_over_horizon'])} / {bps(r1['round_trip_cost'])} bps |",
             f"| 2. Opening time: move on the signal's bar (not captured) | {bps(r2['move_on_bar_0'])} bps |",
             f"| 3. Closing time: peak (bar) / at H / at 2H | {bps(r3['move_at_peak'])} (bar {r3['peak_bar']}) / {bps(r3['move_at_H'])} / {bps(r3['move_at_2H'])} bps |",
             f"| 4. Holding past the bets: share of the time in a position / earned per bar, covered vs past | {share(r4['share_past_the_bets'])} / {bps(r4['earned_per_bar_per_unit_covered'])} vs {bps(r4['earned_per_bar_per_unit_past'])} bps |",
             f"| 5. Trend: the market's share of the book's mean daily gain | {share(r5['market_share'])} (book {bps(r5['book_mean_daily_gain'])} bps a day, market {bps(r5['market_part'])}) |",
             ""]
    write_atomic(out / "diagnosis.md", "\n".join(lines))
    print(f"{record.name}: H={H} bets={w['bets_read']} move={bps(r1['move_over_horizon'])} trip={bps(r1['round_trip_cost'])} "
          f"bar0={bps(r2['move_on_bar_0'])} peak={bps(r3['move_at_peak'])}@{r3['peak_bar']} atH={bps(r3['move_at_H'])} "
          f"at2H={bps(r3['move_at_2H'])} past={share(r4['share_past_the_bets'])} market={share(r5['market_share'])}")


if __name__ == "__main__":
    main()
