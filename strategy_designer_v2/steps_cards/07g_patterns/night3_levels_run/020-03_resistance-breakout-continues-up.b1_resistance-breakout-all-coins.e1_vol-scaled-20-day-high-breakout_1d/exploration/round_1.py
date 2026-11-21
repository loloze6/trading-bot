def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20).std()
            hi = c.shift(1).rolling(20).max()
            lo = c.shift(1).rolling(20).min()
            clr = (c / hi - 1) / vol
            brk = (lo / c - 1) / vol  # positive when close below prior 20d low
            r20 = c / c.shift(20) - 1
            r60 = c / c.shift(60) - 1
            f10 = c.shift(-10) / c - 1
            f20 = c.shift(-20) / c - 1
            f5 = c.shift(-5) / c - 1
            r1 = r / vol
            wd = pd.to_datetime(d["timestamp"]).dt.weekday
            yr = pd.to_datetime(d["timestamp"]).dt.year
            volrank = vol / vol.rolling(120, min_periods=40).median()
            n = len(d)
            pos = np.arange(n)
            tmp = pd.DataFrame(dict(coin=coin, w=w, pos=pos, clr=clr, brk=brk, r20=r20, r60=r60,
                                    f5=f5, f10=f10, f20=f20, r1=r1, wd=wd, yr=yr, volrank=volrank,
                                    fc=d["forecast"].astype(float)))
            rows.append(tmp)
    A = pd.concat(rows, ignore_index=True)
    # drift per coin on 10 grid
    g10 = A[A.pos % 10 == 0]
    drift10 = g10.groupby("coin")["f10"].mean()
    g20 = A[A.pos % 20 == 0]
    drift20 = g20.groupby("coin")["f20"].mean()
    A["x10"] = A["f10"] - A["coin"].map(drift10)
    A["x20"] = A["f20"] - A["coin"].map(drift20)
    G = A[A.pos % 10 == 0].dropna(subset=["x10"])
    def summ(df, col, key):
        out = df.groupby(key)[col].agg(["mean", "count", "std"])
        out["t"] = out["mean"] / (out["std"] / np.sqrt(out["count"]))
        return out.drop(columns="std")
    res = {}
    # clearance buckets (above high) and breakdown buckets
    G = G.copy()
    G["clrb"] = pd.cut(G["clr"], [-99, -3, -1.5, -0.5, 0, 0.5, 1.5, 99])
    res["x10_by_clearance"] = summ(G, "x10", "clrb")
    G["brkb"] = pd.cut(G["brk"], [-99, -1.5, -0.5, 0, 0.5, 1.5, 99])
    res["x10_by_below_low"] = summ(G, "x10", "brkb")
    # last-day move size in vol units
    G["r1b"] = pd.cut(G["r1"], [-99, -2, -1, 0, 1, 2, 99])
    res["x10_by_lastday_volunits"] = summ(G, "x10", "r1b")
    # 60-day return regime
    G["r60b"] = pd.qcut(G["r60"], 5)
    res["x10_by_r60_quintile"] = summ(G, "x10", "r60b")
    G["vrb"] = pd.qcut(G["volrank"], 4)
    res["x10_by_volrank"] = summ(G, "x10", "vrb")
    res["x10_by_weekday"] = summ(G, "x10", "wd")
    res["x10_by_year"] = summ(G, "x10", "yr")
    # 20-day horizon on 20-grid for clearance
    G2 = A[A.pos % 20 == 0].dropna(subset=["x20"]).copy()
    G2["clrb"] = pd.cut(G2["clr"], [-99, -3, -1.5, -0.5, 0, 0.5, 1.5, 99])
    res["x20_by_clearance"] = summ(G2, "x20", "clrb")
    # clearance positive interacted with r60 sign
    P = G[G.clr > 0].copy()
    P["r60pos"] = P["r60"] > 0
    res["breakout_x10_by_r60sign"] = summ(P, "x10", "r60pos")
    return res
