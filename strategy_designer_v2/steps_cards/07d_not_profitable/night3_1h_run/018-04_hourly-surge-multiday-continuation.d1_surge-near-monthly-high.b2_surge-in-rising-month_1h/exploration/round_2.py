import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    coins = list(bars.keys())
    wins = sorted({w for c in coins for w in bars[c]}, key=lambda s: int(s[1:]))
    # daily book by window with per-coin contributions and allocation
    seg = []
    for w in wins:
        frames = []
        for c in coins:
            if w not in days[c]: continue
            d = days[c][w][["day", "book_return", "coin_return"]].copy()
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b.timestamp).dt.floor("D")
            al = b.groupby("day").postRebalance_current_allocation.mean()
            d["dayk"] = pd.to_datetime(d.day).dt.floor("D")
            if d["dayk"].dt.tz is not None and al.index.tz is None:
                al.index = al.index.tz_localize(d["dayk"].dt.tz)
            d["alloc"] = d.dayk.map(al).values
            d["coin"] = c
            frames.append(d)
        df = pd.concat(frames)
        df["long"] = (df.alloc.abs() > 0.01).astype(float)
        g = df.groupby("day").agg(book_return=("book_return", "mean"), coin_return=("coin_return", "mean"),
                                  alloc=("alloc", "mean"), nlong=("long", "sum")).sort_index().dropna()
        g["win"] = w
        seg.append(g)
    allb = pd.concat(seg).reset_index(drop=True)
    eq = (1 + allb.book_return).cumprod()
    dd = eq / eq.cummax() - 1
    allb["in_fall"] = dd < -0.2
    out["fall_vs_not"] = allb.groupby("in_fall").agg(n=("book_return", "size"), book=("book_return", "mean"),
                                                    coin=("coin_return", "mean"), alloc=("alloc", "mean"),
                                                    nlong=("nlong", "mean")).round(4)
    # book daily return by number of coins long
    out["by_nlong"] = allb.groupby("nlong").agg(n=("book_return", "size"), book=("book_return", "mean"),
                                               sd=("book_return", "std"), worst=("book_return", "min")).round(4)
    # trade level: surge size in usual daily moves, path after first 24/48h
    rows = []
    for c in coins:
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            s = b.close.astype(float)
            r24 = s / s.shift(24) - 1
            mabs = r24.abs().rolling(720, min_periods=200).mean()
            z = r24 / mabs
            lr = np.log(s).diff()
            vol720 = lr.rolling(720, min_periods=200).std() * np.sqrt(24)
            r720 = s / s.shift(720) - 1
            tsn = pd.to_datetime(b.timestamp)
            if tsn.dt.tz is not None: tsn = tsn.dt.tz_localize(None)
            t = trades[c].get(w)
            if t is None or len(t) == 0: continue
            cl = s.values
            for _, tr in t.iterrows():
                et = pd.to_datetime(tr.entry_time)
                if et.tzinfo: et = et.tz_localize(None)
                i = int(np.searchsorted(tsn.values, np.datetime64(et), side="right") - 1)
                if i < 0 or i + 240 >= len(cl): continue
                rows.append({"z": z[i], "r24": r24[i], "vol": vol720[i], "r720n": r720[i] / (vol720[i] * np.sqrt(30)) if vol720[i] > 0 else np.nan,
                             "r48": cl[i + 48] / cl[i] - 1, "r48_240": cl[i + 240] / cl[i + 48] - 1,
                             "ret240": cl[i + 240] / cl[i] - 1,
                             "mae": (cl[i:i + 241] / cl[i] - 1).min()})
    T = pd.DataFrame(rows).replace([np.inf, -np.inf], np.nan)
    out["n"] = len(T)
    for f in ["z", "vol", "r720n", "r48"]:
        x = T.dropna(subset=[f])
        q = pd.qcut(x[f], 5, labels=False, duplicates="drop")
        out["by_" + f] = x.groupby(q).agg(lo=(f, "min"), hi=(f, "max"), n=("ret240", "size"),
                                         ret240=("ret240", "mean"), sd=("ret240", "std"),
                                         r48_240=("r48_240", "mean"), mae=("mae", "mean")).round(4)
    x = T.dropna(subset=["r48", "r48_240"])
    out["corr_r48_later"] = pd.Series(stats.spearmanr(x.r48, x.r48_240)).round(4)
    return out
