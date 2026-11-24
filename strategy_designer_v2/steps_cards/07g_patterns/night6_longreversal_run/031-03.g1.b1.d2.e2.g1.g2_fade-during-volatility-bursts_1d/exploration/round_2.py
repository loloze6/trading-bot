def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    coin = list(data["bars"].keys())[0]
    rows = []
    for w, b in data["bars"][coin].items():
        c = b["close"].astype(float).reset_index(drop=True)
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
        ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
        d["wd"] = ts.dt.weekday.values
        d["yr"] = ts.dt.year.values
        d["i"] = np.arange(len(d))
        rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D["r"].mean()
    D["e1"] = D["f1"] - mu1
    D["sgn_e"] = -np.sign(D["z"]) * D["e1"]
    D["fcq"] = pd.qcut(D["fc"].rank(method="first"), 5, labels=False)
    D["zq"] = pd.qcut(D["z"].rank(method="first"), 7, labels=False)
    D["vrq"] = pd.qcut(D["vr"].rank(method="first"), 3, labels=False)
    D["s30q"] = pd.qcut(D["s30"].rank(method="first"), 3, labels=False)
    D["r60q"] = pd.qcut(D["r60"].rank(method="first"), 3, labels=False)
    D["r20q"] = pd.qcut(D["r20"].rank(method="first"), 3, labels=False)
    out = {}
    def tab(df, g, col):
        x = df.dropna(subset=[col, g]).groupby(g)[col]
        t = x.agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t[["mean", "count", "t"]]
    big = D[D.z.abs() > 1]
    small = D[D.z.abs() <= 1]
    out["next day by forecast quintile"] = tab(D, "fcq", "e1")
    out["next day by z septile"] = tab(D, "zq", "e1")
    out["fade gain by vr tercile |z|>1"] = tab(big, "vrq", "sgn_e")
    out["fade gain by vr tercile |z|<=1"] = tab(small, "vrq", "sgn_e")
    out["fade gain by s30 tercile |z|>1"] = tab(big, "s30q", "sgn_e")
    out["fade gain by r60 tercile |z|>1"] = tab(big, "r60q", "sgn_e")
    out["fade gain by r20 tercile |z|>1"] = tab(big, "r20q", "sgn_e")
    big = big.assign(up=(big.z > 0).astype(int))
    out["fade gain |z|>1, up(1) vs down(0)"] = tab(big, "up", "sgn_e")
    out["fade gain |z|>1 by year"] = tab(big, "yr", "sgn_e")
    res = {}
    for h in (1, 2, 3, 5):
        g = D[(D["i"] % h) == 0].dropna(subset=[f"f{h}", "z"])
        y = g[f"f{h}"] - g[f"f{h}"].mean()
        sl = stats.linregress(g["z"], y)
        res[f"z_h{h}"] = {"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(g)}
        for col in ("r5", "r20", "r60"):
            g2 = D[(D["i"] % h) == 0].dropna(subset=[f"f{h}", col])
            y2 = g2[f"f{h}"] - g2[f"f{h}"].mean()
            sl = stats.linregress(g2[col] / g2[col].std(), y2)
            res[f"{col}_h{h}"] = {"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(g2)}
    out["fwd return on past moves (std units)"] = pd.DataFrame(res).T
    out["book gain by weekday"] = tab(D, "wd", "gain")
    out["coin next day by weekday"] = tab(D, "wd", "e1")
    out["book gain by year"] = tab(D, "yr", "gain")
    g = D.dropna(subset=["gain"])
    q = g["gain"].quantile([0.02, 0.98])
    out["worst 2% bars means"] = g[g.gain <= q.iloc[0]][["z", "vr", "pos", "r", "f1", "s30"]].mean()
    out["best 2% bars means"] = g[g.gain >= q.iloc[1]][["z", "vr", "pos", "r", "f1", "s30"]].mean()
    out["share of book gain from top 5% bars"] = float(g.gain.nlargest(int(len(g) * 0.05)).sum() / g.gain.sum())
    return out
