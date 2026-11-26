def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            n = len(b)
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n),
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "regime": b["regime"].astype(str),
                "r1": r1,
                "f1": c.shift(-1)/c-1,
                "f5": c.shift(-5)/c-1,
                "past5": c/c.shift(5)-1,
                "past20": c/c.shift(20)-1,
                "volr": np.log(v.rolling(5).mean()/v.shift(5).rolling(20).mean()),
                "vol20": r1.rolling(20).std(),
                "rng": (b["high"]-b["low"])/c,
                "clv": (c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "vs_raw": b.get("debug_info.components.vol_shrink.last_history_value", pd.Series(np.nan,index=b.index)).astype(float),
                "nl_raw": b.get("debug_info.components.near_low.last_history_value", pd.Series(np.nan,index=b.index)).astype(float),
            })
            df["z1"] = df["r1"]/df["vol20"].shift(1)
            df["gain"] = df["alloc"]*df["f1"]
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    mu5 = A.groupby("coin").apply(lambda d: d.loc[d.pos%5==0,"f5"].mean())
    mu1 = A.groupby("coin")["f1"].mean()
    A["x5"] = A["f5"] - A["coin"].map(mu5)
    A["x1"] = A["f1"] - A["coin"].map(mu1)
    G = A[A.pos%5==0].dropna(subset=["x5"])
    def tab(d, col, val="x5", q=5):
        d = d.dropna(subset=[col,val]).copy()
        d["b"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        g = d.groupby("b")[val]
        return pd.DataFrame({"n":g.size(),"mean%":g.mean()*100,"t":g.mean()/(g.std()/np.sqrt(g.size()))}).round(3)
    out["regime counts"] = A["regime"].value_counts()
    out["x5 by regime"] = G.groupby("regime")["x5"].agg(["size","mean"]).assign(mean=lambda d:d["mean"]*100).round(3)
    U = G[G.regime=="unknown"]
    out["FC in-profile: x5 by forecast quintile"] = tab(U[U.fc<0],"fc")
    out["FC in-profile: x5 by vol_shrink raw"] = tab(U,"vs_raw")
    out["FC in-profile: x5 by near_low raw"] = tab(U,"nl_raw")
    out["FC in-profile: x5 by past20"] = tab(U,"past20")
    out["all: x5 by past20"] = tab(G,"past20")
    out["all: x5 by past5"] = tab(G,"past5")
    out["all: x5 by volr"] = tab(G,"volr")
    out["chop: x5 by past20"] = tab(G[G.regime!="unknown"],"past20")
    # daily: next-day after big moves, all bars (overlap-free at h=1)
    D = A.dropna(subset=["z1","x1"])
    out["all: next-day x1 by z1 decile"] = tab(D,"z1","x1",10)
    out["all: next-day x1 by clv quintile"] = tab(D,"clv","x1")
    out["all: next-day x1 by range quintile"] = tab(D,"rng","x1")
    g = D.groupby("wd")["x1"]
    out["x1 by weekday"] = pd.DataFrame({"n":g.size(),"mean%":g.mean()*100,"t":g.mean()/(g.std()/np.sqrt(g.size()))}).round(3)
    gw = A.groupby("win")["gain"]
    out["position gain by window (sum%)"] = (gw.sum()*100).round(2)
    out["short share of in-position bars"] = float((A.alloc<0).sum()/max((A.alloc!=0).sum(),1))
    out["in-profile x5 by vol20 quintile"] = tab(U,"vol20")
    return out
