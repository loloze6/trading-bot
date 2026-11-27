import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = [3, 5, 7, 10]
    drift = {}
    for coin, wins in data["bars"].items():
        for h in H:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs))
    rows = []; allrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            r = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vol = pd.Series(r).rolling(30, min_periods=10).std().values
            inprof = (b["regime"] != "chop").values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            up = 0; runret = 0.0
            for t in range(1, len(c)):
                # all in-profile days: 3-day past return in vol units vs forward
                if inprof[t] and t >= 3 and vol[t] > 0:
                    d = dict(coin=coin, win=w, t=t, past3z=(c[t]/c[t-3]-1)/vol[t], year=yr[t])
                    for h in H:
                        d[f"u{h}"] = -(c[t+h]/c[t]-1-drift[(coin,h)][0]) if t+h < len(c) else np.nan
                    allrows.append(d)
                if r[t] > 0:
                    up += 1; runret = (1+runret)*(1+r[t])-1; continue
                if r[t] < 0 and up >= 1 and inprof[t]:
                    d = dict(coin=coin, win=w, t=t, run=up,
                             runz=runret/vol[t] if vol[t] > 0 else np.nan, year=yr[t])
                    for h in H:
                        d[f"u{h}"] = -(c[t+h]/c[t]-1-drift[(coin,h)][0]) if t+h < len(c) else np.nan
                        d[f"s{h}"] = d[f"u{h}"]/drift[(coin,h)][1] if t+h < len(c) else np.nan
                    rows.append(d)
                up = 0; runret = 0.0
    df = pd.DataFrame(rows); A = pd.DataFrame(allrows)
    res = {}
    def summ(g, h):
        x = g[f"u{h}"].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    # non-overlapping: keep first case per h-grid cell per coin-window
    out = {}
    for h in H:
        g = df.copy(); g["cell"] = g["t"] // h
        g = g.drop_duplicates(["coin", "win", "cell"])
        s = summ(g, h); out[f"h{h}_all"] = s
        s2 = summ(g[g.run >= 2], h); out[f"h{h}_run2+"] = s2
        out[f"h{h}_strength"] = pd.Series({"n": g[f"s{h}"].notna().sum(), "mean": g[f"s{h}"].mean(), "t": np.nan})
    res["inprof_firstdown_nonoverlap"] = pd.DataFrame(out).T
    g = df.copy(); g["cell"] = g["t"] // 7; g = g.drop_duplicates(["coin", "win", "cell"])
    res["h7_by_coin"] = g.groupby("coin").apply(lambda x: summ(x, 7))
    res["h7_by_year"] = g.groupby("year").apply(lambda x: summ(x, 7))
    res["h7_by_window"] = g.groupby("win").apply(lambda x: summ(x, 7))
    g["runzq"] = pd.qcut(g["runz"], 3, labels=False, duplicates="drop")
    res["h7_by_runz_tercile"] = g.groupby("runzq").apply(lambda x: summ(x, 7))
    res["h3_by_runz_tercile"] = g.groupby("runzq").apply(lambda x: summ(x, 3))
    # all in-profile days: past 3-day move vs forward (non-overlapping 3-grid)
    a = A[(A.t % 3) == 0].copy()
    a["pq"] = pd.qcut(a["past3z"], 5, labels=False, duplicates="drop")
    res["allprof_past3z_quintile_u3"] = a.groupby("pq").apply(lambda x: summ(x, 3))
    a7 = A[(A.t % 7) == 0].copy()
    a7["pq"] = pd.qcut(a7["past3z"], 5, labels=False, duplicates="drop")
    res["allprof_past3z_quintile_u7"] = a7.groupby("pq").apply(lambda x: summ(x, 7))
    res["allprof_baseline"] = pd.DataFrame({f"u{h}": summ(A[(A.t % h) == 0], h) for h in H}).T
    return res
