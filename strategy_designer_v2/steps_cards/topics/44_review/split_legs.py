"""Split a long-and-short book into its long leg and its short leg, and compare each leg with every paying book of the
register and with holding (the similarity check's own functions). The operator's test 1 of 2026-11-22 (runs/NIGHT4_RUN.md); usage: split_legs.py HELPER_DIR RECORD OUT_JSON.
Rule: per coin, each bar's return goes to the side held coming into the bar (the allocation after the previous bar's
rebalance); a bar entered from flat goes to the side entered (its cost). The two legs' bar returns sum to the book's.
Why this can't leak: it reads a finished record after the fact; it changes no decision."""
import sys, json, math
from pathlib import Path
import numpy as np, pandas as pd
H = Path(sys.argv[1]); REC = Path(sys.argv[2])
sys.path.insert(0, str(H)); sys.path.insert(0, str(H.parents[2] / "common"))
from book_returns import coin_windows, period_returns
import ideas_similarities_check as isc
legs = {"long": {}, "short": {}}; worst = 0.0; nbars = 0
for coin, w, f in coin_windows(REC):
    d = pd.read_csv(f, usecols=["timestamp", "close", "postRebalance_total_value", "postRebalance_current_allocation"])
    v = d["postRebalance_total_value"].to_numpy(float); a = d["postRebalance_current_allocation"].to_numpy(float)
    r = np.r_[0.0, v[1:] / v[:-1] - 1]
    held = np.r_[0.0, a[:-1]]; side = np.where(held != 0, np.sign(held), np.sign(a))
    rl, rs = np.where(side > 0, r, 0.0), np.where(side < 0, r, 0.0)
    worst = max(worst, float(np.max(np.abs(rl + rs - r)))); nbars += len(r)
    for name, rr in (("long", rl), ("short", rs)):
        val = pd.Series(np.cumprod(1 + rr))
        legs[name].setdefault(w, []).append(period_returns(val, d["timestamp"], "1d").rename(coin))
print(f"split exact: {nbars} bars, largest |long + short - book| per bar {worst:.2e}")
def series(parts): return pd.concat([pd.concat(p, axis=1, sort=True).mean(axis=1) for _, p in sorted(parts.items())]).sort_index()
book = isc.series(isc.key("night4_fallingbounce_run", REC.name), "1d")
L, Sh = series(legs["long"]), series(legs["short"])
def stats(s):
    s = s.dropna(); m, sd = s.mean(), s.std(); return f"mean {m*100:+.4f} % a day, t {m/sd*math.sqrt(len(s)):.2f}, Sharpe {m/sd*math.sqrt(365):.2f}, days {len(s)}"
print("book :", stats(book)); print("long :", stats(L)); print("short:", stats(Sh))
print(f"share of the book's total return: long {L.sum()/book.sum():.2f}, short {Sh.sum()/book.sum():.2f}")
print(f"days in a short position (share of days with a short-leg return not 0): {(Sh != 0).mean():.2f}; long {(L != 0).mean():.2f}")
hold = isc.series(isc.key("night4_fallingbounce_run", REC.name), "1d", column="hold")
out = {}
for name, s in (("long", L), ("short", Sh)):
    rows = []
    for o in isc.books():
        if o["id"] == REC.name: continue
        c = isc.compare(s, isc.series(o["key"], "1d"), 24)
        if c.get("comparable"): rows.append((c["share_explained"], o["id"], o["bar"], c))
    rows.sort(reverse=True)
    h = isc.compare(s, hold, 24); lv = isc.compare(s, L if name == "short" else Sh, 24)
    print(f"\n{name} leg: nearest paying books (share explained, who leads, direction, left per day and t):")
    for sh, i, b, c in rows[:5]:
        print(f"  {sh:.2f} {c['who_leads']:>22} {c['direction']} {c['what_is_left']*100:+.4f} % (t {c['what_is_left_t']:.2f})  {i[:90]} [{b}]")
    print(f"  against holding its coins: {h['share_explained']:.2f} {h['direction']}, left {h['what_is_left']*100:+.4f} % (t {h['what_is_left_t']:.2f})")
    print(f"  against the other leg: {lv['share_explained']:.2f} {lv['direction']}")
    out[name] = {"nearest": [{"share_explained": sh, "id": i, "bar": b, **{k: c[k] for k in ('who_leads','direction','what_is_left','what_is_left_t')}} for sh, i, b, c in rows[:5]],
                 "against_holding": {k: h[k] for k in ('share_explained','direction','what_is_left','what_is_left_t')}}
json.dump(out, open(Path(sys.argv[3]), "w"), indent=2)
