import numpy as np
import pandas as pd

def _t(x):
    x = pd.Series(x).dropna()
    if len(x) < 3 or x.std() == 0:
        return np.nan
    return x.mean() / (x.std() / np.sqrt(len(x)))

def _summ(g, col):
    return pd.Series({"n": g[col].notna().sum(), "mean_bps": g[col].mean()*1e4, "t": _t(g[col])})

def explore(data):
    out = {}
    rows, rev = [], []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r1 = c.pct_change()
            sd = r1.rolling(720, min_periods=240).std()
            vol = b["volume"].astype(float)
            vr = vol / vol.rolling(720, min_periods=240).mean()
            fwd2 = c.shift(-2) / c - 1
            # sample at close of hour 19 bar (start 19) -> next 2 bars cover hours 20,21
            m = (ts.dt.hour == 19).values
            past20 = (c / c.shift(20) - 1) / (sd * np.sqrt(20))
            past4 = (c / c.shift(4) - 1) / (sd * np.sqrt(4))
            rows.append(pd.DataFrame({"coin": coin, "win": w, "p20": past20[m].values, "p4": past4[m].values,
                                      "vr": vr[m].values, "sd": sd[m].values,
                                      "fwd": fwd2[m].values, "fwd_all_mean": np.nan}))
            # all 2h grid returns for drift
            idx = np.arange(0, len(b), 2)
            rev.append(pd.DataFrame({"coin": coin, "fwd": fwd2.values[idx]}))
            # book's own return in hours 20-21 vs others
    g = pd.concat(rows, ignore_index=True).dropna(subset=["fwd", "p20", "sd"])
    dr = pd.concat(rev).dropna().groupby("coin")["fwd"].mean()
    g["unus"] = g["fwd"] - g["coin"].map(dr)
    out["evening2h_overall"] = _summ(g, "unus")
    for col in ("p20", "p4", "vr", "sd"):
        g["q"] = g.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        out[f"evening2h_by_{col}_quintile"] = g.groupby("q").apply(lambda x: _summ(x, "unus"))
    # book's gain by hour of day
    bh = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            v = b["postRebalance_total_value"].astype(float)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            bh.append(pd.DataFrame({"hour": ts.dt.hour, "br": v.pct_change().shift(-1),
                                    "alloc": b["postRebalance_current_allocation"].astype(float)}))
    bh = pd.concat(bh).dropna()
    hb = bh.groupby("hour").agg(book_bps=("br", lambda s: s.mean()*1e4), alloc=("alloc", "mean"))
    out["book_bar_by_hour"] = hb
    return out
