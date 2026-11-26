def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    coin = list(data["bars"].keys())[0]
    rows = []
    for w, b in data["bars"][coin].items():
        b = b.copy()
        c = b["close"].astype(float)
        r = c.pct_change()
        d = pd.DataFrame({"w": w, "r": r})
        d["s30"] = r.rolling(30, min_periods=20).std()
        d["s5"] = r.rolling(5, min_periods=5).std()
        d["z"] = r / d["s30"]
        d["vr"] = d["s5"] / d["s30"]
        d["r5"] = c / c.shift(5) - 1
        d["r20"] = c / c.shift(20) - 1
        d["r60"] = c / c.shift(60) - 1
        for h in (1, 2, 3, 5):
            d[f"f{h}"] = c.shift(-h) / c - 1
        d["fc"] = b["forecast"].values
        d["pos"] = b["postRebalance_current_allocation"].values
        d["gain"] = d["pos"] * d["f1"]
        ts = pd.to_datetime(b["timestamp"])
        d["wd"] = ts.dt.weekday.values
        d["yr"] = ts.dt.year.values
        d["i"] = np.arange(len(d))
        rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D["r"].mean()
    D["e1"] = D["f1"] - mu1
    out = {}
    def tab(g, col="e1"):
        x = D.dropna(subset=[col]).groupby(g)[col]
        t = x.agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t[["mean", "count", "t"]]
    D["fcq"] = pd.qcut(D["fc"].rank(method="first"), 5, labels=False)
    out["next day by forecast quintile"] = tab("fcq")
    D["zq"] = pd.qcut(D["z"].rank(method="first"), 7, labels=False)
    out["next day by z septile"] = tab("zq")
    D["vrq"] = pd.qcut(D["vr"].rank(method="first"), 3, labels=False)
    D["sgn_e"] = -np.sign(D["z"]) * D["e1"]
    x = D.dropna(subset=["sgn_e", "vrq"])
    out["fade gain by volratio tercile, |z|>1"] = x[x["z"].abs() > 1].groupby("vrq")["sgn_e"].agg(["mean", "count"])
    out["fade gain by volratio tercile, |z|<=1"] = x[x["z"].abs() <= 1].groupby("vrq")["sgn_e"].agg(["mean", "count"])
    # asymmetry up vs down days
    x = D.dropna(subset=["z", "e1"])
    out["fade gain up days |z|>1"] = float(x[(x.z > 1)]["sgn_e"].mean())
    out["fade gain down days z<-1"] = float(x[(x.z < -1)]["sgn_e"].mean())
    # regressions per horizon, non-overlapping grid
    res = {}
    for h in (1, 2, 3, 5):
        g = D[(D["i"] % h) == 0].dropna(subset=[f"f{h}", "z"])
        y = g[f"f{h}"] - g[f"f{h}"].mean()
        sl = stats.linregress(g["z"], y)
        res[h] = {"slope_z": sl.slope, "t": sl.slope / sl.stderr, "n": len(g)}
    out["fwd return on z by horizon"] = pd.DataFrame(res).T
    # longer past returns
    res = {}
    for col in ("r5", "r20", "r60", "s30"):
        for h in (1, 5):
            g = D[(D["i"] % h) == 0].dropna(subset=[f"f{h}", col])
            y = g[f"f{h}"] - g[f"f{h}"].mean()
            sl = stats.linregress(g[col] / g[col].std(), y)
            res[f"{col}_h{h}"] = {"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(g)}
    out["fwd on past returns / vol"] = pd.DataFrame(res).T
    D["s30q"] = pd.qcut(D["s30"].rank(method="first"), 3, labels=False)
    out["fade gain by s30 tercile |z|>1"] = x[x.z.abs() > 1].groupby("s30q")["sgn_e"].agg(["mean", "count"])
    out["book gain by weekday"] = D.groupby("wd")["gain"].agg(["mean", "count"])
    out["next day coin by weekday"] = tab("wd")
    out["book gain by year"] = D.groupby("yr")["gain"].agg(["mean", "count"])
    out["fade gain |z|>1 by year"] = x[x.z.abs() > 1].groupby("yr")["sgn_e"].agg(["mean", "count"])
    # regime of r60 interaction
    D["r60q"] = pd.qcut(D["r60"].rank(method="first"), 3, labels=False)
    x2 = D.dropna(subset=["sgn_e", "r60q"])
    out["fade gain |z|>1 by 60d return tercile"] = x2[x2.z.abs() > 1].groupby("r60q")["sgn_e"].agg(["mean", "count"])
    # largest book gains/losses
    g = D.dropna(subset=["gain"])
    q = g["gain"].quantile([0.02, 0.98])
    out["worst 2% bars: mean z, vr, pos"] = g[g.gain <= q.iloc[0]][["z", "vr", "pos", "r", "f1"]].mean()
    out["best 2% bars: mean z, vr, pos"] = g[g.gain >= q.iloc[1]][["z", "vr", "pos", "r", "f1"]].mean()
    out["share of book gain from top 5% bars"] = float(g.gain.nlargest(int(len(g)*0.05)).sum() / g.gain.sum())
    return out
