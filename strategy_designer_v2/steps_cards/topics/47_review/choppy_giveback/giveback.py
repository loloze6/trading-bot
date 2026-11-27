"""Give-back of the best gain, per trade and per book (choppy confirmed vs reference profitable).

Reads, per book: chart_trades.csv.gz (the trades), chart_bars.csv.gz (the window's bar dates and closes), and the
coin's daily bars in trading-bot/local_data (high, low, close) only on dates present in chart_bars, i.e. inside the
fold windows the backtest ran. Nothing else is read (no holdout file, no ledger), nothing is written outside this folder.

Per trade (as trading-bot/backtest/run_protocol.py _compute_mae_mfe):
  - holding bars = the window's bars from the entry bar to the exit bar; excursions read on the bars AFTER the entry bar.
  - MFE, MAE in % of the entry price (high/low of those bars).
  - gross = (exit/entry - 1) signed, from the trade's fill prices (the engine's realized_return in trade_diagnostics).
  - net = chart_trades realized_return (after costs).
  - give-back = MFE - gross (in % points).
  - hold-N: exit at the close N bars after the entry bar (or the window's last bar if sooner), net of the same costs as
    the trade paid: net_N = cc_N - (cc_plan - net), cc = close-to-close from the entry bar's close.
Why this cannot leak: it is an after-the-fact reading of finished trades; it feeds no decision of any strategy.
"""
import csv, glob, gzip, json, os, statistics as st, sys
from collections import defaultdict

REPO = "/home/user/trading-bot"
BT = f"{REPO}/strategy_designer_v2/steps_cards/04_backtest"
DATA = f"{REPO}/trading-bot/local_data"
OUT = os.path.dirname(os.path.abspath(__file__))
HOLDS = [1, 2, 3, 5, 10]

_bars_cache = {}


def coin_bars(coin):
    if coin not in _bars_cache:
        d = {}
        with open(f"{DATA}/kraken_{coin}_1d.csv") as f:
            for r in csv.DictReader(f):
                d[r["timestamp"][:10]] = (float(r["high"]), float(r["low"]), float(r["close"]))
        _bars_cache[coin] = d
    return _bars_cache[coin]


def book_trades(run, backtest):
    d = f"{BT}/{run}/backtests/{backtest}"
    win = defaultdict(list)  # (coin, window) -> [dates]
    with gzip.open(f"{d}/chart_bars.csv.gz", "rt") as f:
        for r in csv.DictReader(f):
            win[(r["coin"], r["window"])].append(r["timestamp"][:10])
    out, skipped = [], 0
    with gzip.open(f"{d}/chart_trades.csv.gz", "rt") as f:
        for r in csv.DictReader(f):
            coin, w = r["coin"], r["window"]
            dates = win.get((coin, w), [])
            pos = {t: i for i, t in enumerate(dates)}
            e, x = r["entry_time"][:10], r["exit_time"][:10]
            if e not in pos or x not in pos or pos[x] < pos[e]:
                skipped += 1
                continue
            bars = coin_bars(coin)
            if any(t not in bars for t in dates[pos[e]:min(pos[e] + 10, len(dates) - 1) + 1]) or any(
                    t not in bars for t in dates[pos[e]:pos[x] + 1]):
                skipped += 1
                continue
            long = r["direction"].upper() == "LONG"
            sgn = 1 if long else -1
            ep, xp, net = float(r["entry_price"]), float(r["exit_price"]), float(r["realized_return"])
            after = dates[pos[e] + 1:pos[x] + 1]
            mfe = mae = 0.0
            for t in after:
                h, l, _ = bars[t]
                fav = (h - ep) / ep if long else (ep - l) / ep
                adv = (ep - l) / ep if long else (h - ep) / ep
                mfe, mae = max(mfe, fav), max(mae, adv)
            gross = sgn * (xp / ep - 1) * 100
            c0 = bars[e][2]
            cc_plan = sgn * (bars[x][2] / c0 - 1) * 100
            cost = cc_plan - net
            hold = {}
            for n in HOLDS:
                j = min(pos[e] + n, len(dates) - 1)
                hold[n] = sgn * (bars[dates[j]][2] / c0 - 1) * 100 - cost
            out.append(dict(coin=coin, window=w, entry=e, exit=x, mfe=mfe * 100, mae=mae * 100, gross=gross, net=net,
                            giveback=mfe * 100 - gross, bars=pos[x] - pos[e], hold=hold))
    return out, skipped


def engine_check(run, backtest, trades):
    """Compare with the engine's own trade_diagnostics (where the record kept them)."""
    eng = {}
    for p in glob.glob(f"{BT}/{run}/backtests/{backtest}/*/*/trade_diagnostics.json.gz"):
        with gzip.open(p, "rt") as f:
            for t in json.load(f)["trades"]:
                eng[(t["symbol"], t["entry_time"][:10], t["exit_time"][:10])] = t
    n = ok = 0
    worst = 0.0
    for t in trades:
        k = (t["coin"], t["entry"], t["exit"])
        if k in eng:
            n += 1
            dm = max(abs(eng[k]["mfe"] - t["mfe"]), abs(eng[k]["mae"] - t["mae"]),
                     abs(eng[k]["realized_return"] - t["gross"]))
            worst = max(worst, dm)
            ok += dm < 0.01
    return len(trades), len(eng), n, ok, worst


def summarise(trades):
    m = lambda xs: st.mean(xs) if xs else float("nan")
    mean_net = m([t["net"] for t in trades])
    mfe = m([t["mfe"] for t in trades])
    gross = m([t["gross"] for t in trades])
    s = dict(n=len(trades), mean_net=mean_net, mean_gross=gross, mean_mfe=mfe, mean_mae=m([t["mae"] for t in trades]),
             mean_giveback=m([t["giveback"] for t in trades]),
             giveback_share=(mfe - gross) / mfe if mfe > 0 else float("nan"),
             median_bars=st.median([t["bars"] for t in trades]))
    # literal reading: best gain >= 2x the book's mean final gain, then exited below that mean gain
    s["share_2x_mean_then_lower"] = (sum(1 for t in trades if t["mfe"] >= 2 * mean_net and t["net"] < mean_net)
                                     / len(trades)) if mean_net > 0 else float("nan")
    # per-trade reading: gave back more than half of its own best gain (trades with a best gain > 0)
    pos = [t for t in trades if t["mfe"] > 0]
    s["share_gave_back_half"] = sum(1 for t in pos if t["gross"] < t["mfe"] / 2) / len(pos) if pos else float("nan")
    for n in HOLDS:
        s[f"hold{n}"] = m([t["hold"][n] for t in trades])
    return s


def main():
    books = json.load(open(os.path.join(OUT, "choppy_books.json")))
    rows = []
    for grp, lst in books.items():
        for i, b in enumerate(lst):
            trades, skipped = book_trades(b["run"], b["backtest"])
            s = summarise(trades)
            group = b["profile"] if grp == "choppy_confirmed" else "reference profitable"
            rows.append(dict(group=group, run=b["run"], backtest=b["backtest"], skipped=skipped, **s))
            # every book: compared with the engine's own trade_diagnostics where the record kept them
            rows[-1].update(dict(zip(["chk_trades", "chk_engine", "chk_matched", "chk_equal", "chk_worst"],
                                     engine_check(b["run"], b["backtest"], trades))))
            print(f"{group:22} {b['backtest'][:45]:45} n={s['n']} skip={skipped}", file=sys.stderr)
    keys = list(rows[0].keys())
    with open(os.path.join(OUT, "per_book.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})


if __name__ == "__main__":
    main()
