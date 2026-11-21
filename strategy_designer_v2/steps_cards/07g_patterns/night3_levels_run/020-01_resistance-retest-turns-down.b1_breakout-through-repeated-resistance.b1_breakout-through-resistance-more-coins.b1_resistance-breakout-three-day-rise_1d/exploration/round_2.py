def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    def nonover(df, h):
        c = df["close"].values
        idx = np.arange(0, len(c)-h, h)
        return c[idx+h]/c[idx]-1
    H = [1,2,3,5]
    drift = {}; usual = {}
    for coin, ws in bars.items():
        for h in H:
            r = np.concatenate([nonover(df,h) for df in ws.values()])
            drift[(coin,h)] = np.nanmean(r); usual[(coin,h)] = np.nanstd(r)
    def grid(h_fut):
        rr = []
        for coin, ws in bars.items():
            for w, df in ws.items():
                c = df["close"].values; n = len(c)
                lr = np.r_[np.nan, np.log(c[1:]/c[:-1])]
                vol = pd.Series(lr).rolling(20).std().values
                vol60 = pd.Series(lr).rolling(60, min_periods=40).std().values
                hi = pd.Series(c).rolling(20).max().values
                ts = pd.to_datetime(df["timestamp"]).values
                for i in range(0, n-h_fut, h_fut):
                    if i < 1: continue
                    fut = c[i+h_fut]/c[i]-1 - drift[(coin,h_fut)]
                    rr.append({"coin": coin, "w": w,
                               "p1": (c[i]/c[i-1]-1)/usual[(coin,1)],
                               "vr": vol[i]/vol60[i] if vol60[i]==vol60[i] and vol60[i]>0 else np.nan,
                               "dist": c[i]/hi[i]-1 if hi[i]==hi[i] else np.nan,
                               "fut": fut, "sfut": fut/usual[(coin,h_fut)],
                               "year": pd.Timestamp(ts[i]).year, "wd": pd.Timestamp(ts[i]).weekday()})
        return pd.DataFrame(rr)
    def tq(g, key, q, by=None):
        g = g.dropna(subset=[key]).copy()
        g["b"] = g.groupby("coin")[key].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        keys = ["b"] if by is None else [by, "b"]
        a = g.groupby(keys).agg(n=("fut","count"), key=(key,"mean"), fut=("fut","mean"), sfut=("sfut","mean"), sd=("fut","std"))
        a["t"] = a["fut"]/(a["sd"]/np.sqrt(a["n"]))
        return a.drop(columns="sd")
    g1 = grid(1); g2 = grid(2); g3 = grid(3); g5 = grid(5)
    # 1-day reversal: deciles, horizon 2, by year (bottom quintile only)
    out["p1_deciles_next1d"] = tq(g1, "p1", 10)
    out["p1_quint_next2d"] = tq(g2, "p1", 5)
    a = tq(g1, "p1", 5, by="year").reset_index(); out["p1_bottomq_by_year"] = a[a["b"]==0].set_index("year")[["n","fut","t"]]
    a = tq(g1, "p1", 5, by="coin").reset_index(); out["p1_bottomq_by_coin"] = a[a["b"]==0].set_index("coin")[["n","fut","t"]]
    # vol contraction
    out["vr_deciles_next3d"] = tq(g3, "vr", 10)
    out["vr_quint_next5d"] = tq(g5, "vr", 5)
    a = tq(g3, "vr", 5, by="year").reset_index(); out["vr_lowq_by_year"] = a[a["b"]==0].set_index("year")[["n","fut","t"]]
    a = tq(g3, "vr", 5, by="coin").reset_index(); out["vr_lowq_by_coin"] = a[a["b"]==0].set_index("coin")[["n","fut","t"]]
    # nearness to 20d high
    a = tq(g3, "dist", 5, by="year").reset_index(); out["dist_topq_by_year"] = a[a["b"]==4].set_index("year")[["n","fut","t"]]
    # weekday by year halves
    g1["half"] = np.where(g1["year"] <= 2021, "early", "late")
    wd = g1.groupby(["half","wd"]).agg(n=("fut","count"), fut=("fut","mean"), sd=("fut","std"))
    wd["t"] = wd["fut"]/(wd["sd"]/np.sqrt(wd["n"])); out["weekday_by_half"] = wd.drop(columns="sd")
    return out
