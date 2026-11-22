def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r6 = c / c.shift(6) - 1
            mabs = r6.abs().rolling(180, min_periods=60).mean()
            z6 = r6 / mabs
            r1 = c / c.shift(1) - 1
            z1 = r1 / r1.abs().rolling(180, min_periods=60).mean()
            ts = pd.to_datetime(df["timestamp"])
            out = pd.DataFrame({"coin": coin, "win": w, "wn": int(w[1:]), "pos": np.arange(len(df)), "z6": z6, "z1": z1,
                                "hour": ts.dt.hour, "wd": ts.dt.weekday, "year": ts.dt.year})
            for H in [1, 3, 6, 12, 18]:
                out[f"f{H}"] = c.shift(-H) / c - 1
            rows.append(out)
    A = pd.concat(rows, ignore_index=True)
    res = {}
    def grid(H):
        g = A[A["pos"] % H == 0].dropna(subset=[f"f{H}"]).copy()
        g["ex"] = g[f"f{H}"] - g.groupby("coin")[f"f{H}"].transform("mean")
        g["exs"] = g["ex"] / g.groupby("coin")[f"f{H}"].transform("std")
        return g
    def tt(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    # graded fall depth -> next 6/18 bars, deciles of falls only
    for H in [3, 6, 12, 18]:
        g = grid(H).dropna(subset=["z6"])
        f = g[g.z6 < 0].copy()
        f["b"] = pd.qcut(f.z6.rank(method="first"), 5, labels=False)
        t = f.groupby("b").apply(lambda x: pd.concat([pd.Series({"z6_mean": x.z6.mean()}), tt(x.ex)]))
        res[f"falls only quintiles -> ex {H}"] = t
        s = stats.linregress(-f.z6, f.exs)
        res[f"falls only slope exs on depth H{H}"] = pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(f)})
    g6 = grid(6).dropna(subset=["z6"])
    f6 = g6[g6.z6 < 0]
    pc = {}
    for coin, x in f6.groupby("coin"):
        s = stats.linregress(-x.z6, x.exs); pc[coin] = {"slope": s.slope, "t": s.slope / s.stderr, "n": len(x)}
    res["falls H6 slope per coin"] = pd.DataFrame(pc).T
    py = {}
    for y, x in f6.groupby("year"):
        s = stats.linregress(-x.z6, x.exs); py[y] = {"slope": s.slope, "t": s.slope / s.stderr, "n": len(x)}
    res["falls H6 slope per year"] = pd.DataFrame(py).T
    # rises symmetric? full z6 slope H6
    s = stats.linregress(g6.z6, g6.exs)
    res["all z6 slope H6"] = pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(g6)})
    r6 = g6[g6.z6 > 0]; s = stats.linregress(r6.z6, r6.exs)
    res["rises only slope H6"] = pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(r6)})
    # hour effect robustness
    g1 = grid(1)
    for hr in [16, 20]:
        x = g1[g1.hour == hr]
        res[f"hour {hr} per coin"] = x.groupby("coin")["ex"].apply(tt).unstack()
        res[f"hour {hr} per year"] = x.groupby("year")["ex"].apply(tt).unstack()
    # hour 16 bar following 4-bar return: graded?
    g1 = g1.dropna(subset=["z1"])
    pr = {}
    for hr, x in g1.groupby("hour"):
        s = stats.linregress(x.z1, x.exs); pr[hr] = {"slope": s.slope, "t": s.slope / s.stderr, "n": len(x)}
    res["next bar on previous bar z1 slope by hour"] = pd.DataFrame(pr).T
    # Friday
    g6b = grid(6)
    x = g6b[g6b.wd == 4]
    res["friday per coin"] = x.groupby("coin")["ex"].apply(tt).unstack()
    res["friday per year"] = x.groupby("year")["ex"].apply(tt).unstack()
    res["friday by start hour"] = x.groupby("hour")["ex"].apply(tt).unstack()
    return res
