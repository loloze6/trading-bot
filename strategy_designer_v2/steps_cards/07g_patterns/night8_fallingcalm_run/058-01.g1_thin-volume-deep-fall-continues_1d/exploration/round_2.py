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
            b["r1"] = r1
            b["z1"] = r1 / r1.rolling(30).std().shift(1)
            b["v_z"] = np.log(v / v.rolling(30).mean().shift(1))
            b["fwd1"] = c.shift(-1) / c - 1
            b["fwd3"] = c.shift(-3) / c - 1
            b["ret60"] = c / c.shift(60) - 1
            b["ret30p"] = c / c.shift(30) - 1
            b["vr"] = v.rolling(30).mean().shift(30) / v.rolling(30).mean()
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["coin"] = coin; b["win"] = w; b["pos"] = np.arange(len(b))
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    B["ex1"] = B["fwd1"] - B.groupby("coin")["fwd1"].transform("mean")
    B["ex3"] = B["fwd3"] - B.groupby("coin")["fwd3"].transform("mean")
    def summ(df, col, key):
        g = df.dropna(subset=[col, key]).groupby(key)[col]
        r = g.agg(["count", "mean", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.round(5)
    B["trend"] = pd.cut(B["ret60"], [-np.inf, -0.10, 0.10, np.inf], labels=["falling", "choppy", "rising"])
    B["fc"] = B["regime"].eq("unknown")
    D = B[B["z1"] < -1.5].copy()
    D["hv"] = D["v_z"] > D["v_z"].quantile(2/3)
    D["key"] = D["trend"].astype(str) + "_hv" + D["hv"].astype(str)
    out["down>1.5sd next-day ex by trend x heavyvol"] = summ(D, "ex1", "key")
    out["down>1.5sd next-day ex by fallingcalm x heavyvol"] = summ(D.assign(k=D["fc"].astype(str) + "_" + D["hv"].astype(str)), "ex1", "k")
    H = D[D["hv"]]
    out["heavyvol down: next-day ex by year"] = summ(H, "ex1", "year")
    out["heavyvol down: next-day ex by coin"] = summ(H, "ex1", "coin")
    # grading: continuous regression among all down days z<-1, of ex1 on v_z and on z1*v_z
    A = B[(B["z1"] < -1)].dropna(subset=["ex1", "v_z", "z1"]).copy()
    A["score"] = -A["z1"] * A["v_z"].clip(lower=0)
    for col in ["v_z", "score"]:
        s = stats.linregress(A[col], A["ex1"])
        out[f"z<-1: slope ex1 on {col}"] = f"slope {s.slope:.5f} t {s.slope/s.stderr:.2f} n {len(A)}"
    # day-clustered t for heavyvol down rebound
    hd = H.dropna(subset=["ex1"]).groupby(["day"])["ex1"].sum()
    out["heavyvol down day-clustered"] = f"mean/day {hd.mean():.5f} t {hd.mean()/(hd.std()/np.sqrt(len(hd))):.2f} days {len(hd)}"
    # 3-day horizon non-overlapping grid not applicable to events; report 3-day ex after event
    out["down>1.5sd 3-day ex by heavyvol"] = summ(D, "ex3", "hv")
    # mean day-1 return of the event bar itself vs heavyvol (to see size of fall)
    out["event day return by hv"] = D.groupby("hv")["r1"].agg(["count", "mean"]).round(4)
    # z<-2 bucket by trend
    E = B[B["z1"] < -2]
    out["down>2sd next-day ex by trend"] = summ(E, "ex1", "trend")
    return out
