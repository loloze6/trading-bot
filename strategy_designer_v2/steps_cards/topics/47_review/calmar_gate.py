"""Topic 47, measurement 1: why real books do not pay. For every book step 5 confirmed in the night-5 runs (paying
or not), from its committed chart files (the same daily chain as step 6: equal-weight coins, windows in order):
its Calmar and holding's Calmar on the same coins and days; where its deepest fall lies and what holding did over
those same days; its time in the market; its trades: count, mean net return per trade (the engine's, after costs)
and mean gross move (prices only). Writes calmar_gate.csv beside this file and prints the summary.
  python3 topics/47_review/calmar_gate.py
Reads only files of finished backtests (no dates of the sealed holdout: night-5 records cover the folds only)."""
import json, math, pathlib, sys
import numpy as np, pandas as pd

STEPS = pathlib.Path(__file__).resolve().parents[2]
RUNS = ["retest_weekend_run", "retest_learned_run", "retest_settlement_run", "brief_absorption_run", "retest_monday_run"]
ROUND_TRIP = 0.193            # % of a position, the core round-trip cost (topic 45)


def chain(parts, by_date=False):
    """Equal-weight daily returns per window (mean over coins), windows in step 6's order (window number, which is
    fold order) or, with by_date, in date order: one array."""
    frames = [pd.concat(v, axis=1, sort=True).mean(axis=1) for _, v in sorted(parts.items())]
    if by_date: frames = sorted(frames, key=lambda f: f.index[0])
    return np.concatenate([f.to_numpy() for f in frames])


def calmar(r):
    curve = np.cumprod(1 + r); years = len(r) / 365
    ann = curve[-1] ** (1 / years) - 1 if years > 0 and curve[-1] > 0 else -1.0
    peak = np.maximum.accumulate(np.concatenate([[1.0], curve]))[1:]
    dd = 1 - curve / peak
    i = int(np.argmax(dd)); j = int(np.argmax(curve[:i + 1] >= peak[i] - 1e-15)) if i > 0 else 0
    fall = float(dd[i])
    return (math.inf if fall == 0 and ann > 0 else (ann / fall if fall > 0 else 0.0)), ann, fall, j, i


def book(record):
    b = pd.read_csv(record / "chart_bars.csv.gz", parse_dates=["timestamp"])
    b["day"] = b["timestamp"].dt.normalize(); b["w"] = b["window"].str[1:].astype(int)
    bk, hd, days = {}, {}, {}
    for (coin, w), d in b.groupby(["coin", "w"]):
        last = d.groupby("day").last()
        bk.setdefault(w, []).append(last["value"].pct_change().dropna().rename(coin))
        hd.setdefault(w, []).append(last["close"].pct_change().dropna().rename(coin))
        days.setdefault(w, last.index[1:])
    idx = np.concatenate([np.asarray(pd.concat(v, axis=1, sort=True).index) for _, v in sorted(bk.items())])
    return chain(bk), chain(hd), idx, chain(bk, True), chain(hd, True)


def trades(record):
    t = pd.read_csv(record / "chart_trades.csv.gz")
    if t.empty: return 0, float("nan"), float("nan")
    sign = np.where(t["direction"].str.upper() == "SHORT", -1.0, 1.0)
    gross = 100 * sign * (t["exit_price"] / t["entry_price"] - 1)
    return len(t), float(t["realized_return"].mean()), float(gross.mean())


rows = []
for run in RUNS:
    for r in json.load(open(STEPS / "orchestration/run_idea" / run / "table.json")):
        s5, s6 = r.get("step5") or "", r.get("step6") or ""
        if not s5.startswith("confirmed") or not s6: continue
        rec = STEPS / "04_backtest" / run / "backtests" / r["backtest"]
        chk = STEPS / "06_profitability" / run / "checks" / r["backtest"] / "result.json"
        if not (rec / "chart_bars.csv.gz").exists() or not chk.exists(): continue
        res = json.load(open(chk)); m = {x["measure"]: x for x in res["measures"]}
        br, hr, idx, brd, hrd = book(rec)
        bc, ba, bf, bp, bt = calmar(br); hc, ha, hf, _, _ = calmar(hr)
        hold_over_fall = float(np.prod(1 + hr[bp + 1:bt + 1]) - 1) if bt > bp else 0.0
        n, net, gross = trades(rec)
        rows.append({"run": run, "backtest": r["backtest"], "pays": res["status"] == "profitable enough",
                     "failed": ";".join(x["label"] for x in res["measures"] if not x["passed"]),
                     "calmar_step6": m["calmar_min"]["value"], "calmar_here": bc, "calmar_by_date": calmar(brd)[0],
                     "fall_by_date": calmar(brd)[2], "holding_calmar_by_date": calmar(hrd)[0], "yearly_return": ba, "deepest_fall": bf,
                     "fall_years": f"{pd.Timestamp(idx[bp]).year}-{pd.Timestamp(idx[bt]).year}", "fall_days": int(bt - bp),
                     "holding_over_the_fall": hold_over_fall, "holding_calmar": hc, "holding_fall": hf,
                     "share_in_position": (res.get("informative") or {}).get("share_of_days_in_a_position"),
                     "trades": n, "net_per_trade_pct": net, "gross_per_trade_pct": gross})
d = pd.DataFrame(rows); d.to_csv(pathlib.Path(__file__).with_name("calmar_gate.csv"), index=False, float_format="%.5g")
nopay = d[~d.pays]
print(f"confirmed books: {len(d)}; paying {int(d.pays.sum())}; not paying {len(nopay)}")
print(f"Calmar here vs step 6 (check): max abs difference {float((d.calmar_here - d.calmar_step6).abs().max()):.3g}")
for name, x in (("not paying", nopay), ("paying", d[d.pays])):
    print(f"\n== {name} ({len(x)})")
    print(" median Calmar", round(x.calmar_here.median(), 3), "| median holding Calmar same coins/days", round(x.holding_calmar.median(), 3),
          "| holding below 0.75:", int((x.holding_calmar <= 0.75).sum()))
    print(" median yearly return", round(100 * x.yearly_return.median(), 1), "% | median deepest fall", round(100 * x.deepest_fall.median(), 1), "%")
    print(" median share of days in a position", round(x.share_in_position.median(), 3))
    print(" holding fell over the book's deepest fall (< -20 %):", int((x.holding_over_the_fall < -0.2).sum()), "| rose:", int((x.holding_over_the_fall > 0).sum()))
    print(" years of the deepest fall:", x.fall_years.value_counts().head(6).to_dict())
    print(" median trades", int(x.trades.median()), "| median net per trade", round(x.net_per_trade_pct.median(), 3), "% | median gross", round(x.gross_per_trade_pct.median(), 3), "% | round trip", ROUND_TRIP, "%")
    print(" net per trade <= 0:", int((x.net_per_trade_pct <= 0).sum()), "| gross under 2 round trips:", int((x.gross_per_trade_pct < 2 * ROUND_TRIP).sum()))
    print(" Calmar if the book were in the market every day (Calmar / share, a ceiling, not a rule):", round((x.calmar_here / x.share_in_position).median(), 2))

print("\n== windows in date order instead of fold order (same days, same returns; only the order of the chain changes)")
print(" verdict on Calmar alone would change for:", int(((d.calmar_here > 0.75) != (d.calmar_by_date > 0.75)).sum()), "of", len(d),
      "| fail -> pass:", int(((d.calmar_here <= 0.75) & (d.calmar_by_date > 0.75)).sum()), "| pass -> fail:", int(((d.calmar_here > 0.75) & (d.calmar_by_date <= 0.75)).sum()))
print(" median deepest fall: fold order", round(100 * d.deepest_fall.median(), 1), "% | date order", round(100 * d.fall_by_date.median(), 1), "%")
print(" not paying, failed Calmar alone, would pass Calmar by date:", int(((~d.pays) & (d.failed == "Calmar") & (d.calmar_by_date > 0.75)).sum()), "of", int(((~d.pays) & (d.failed == "Calmar")).sum()))
print(" holding Calmar median: fold order", round(d.holding_calmar.median(), 3), "| date order", round(d.holding_calmar_by_date.median(), 3))
