def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    def grid(H):
        rows = []
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].astype(float); n = len(b)
                r1 = c.pct_change()
                vol = r1.rolling(30, min_periods=20).std().shift(1)
                hi30 = c.rolling(30, min_periods=20).max(); lo30 = c.rolling(30, min_periods=20).min()
                pos = (c - lo30) / (hi30 - lo30)
                r30 = c / c.shift(30) - 1
                wn = int(w[1:])
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, win=w, half=1 if wn <= 12 else 2, f=b["forecast"].iloc[i],
                                     fwd=c.iloc[i + H] / c.iloc[i] - 1, r1=r1.iloc[i], vol=vol.iloc[i],
                                     pos=pos.iloc[i], r30=r30.iloc[i]))
        g = pd.DataFrame(rows)
        g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
        g["r1z"] = g["r1"] / g["vol"]
        g["exz"] = g["ex"] / g.groupby("coin")["fwd"].transform("std")
        return g.dropna(subset=["ex", "r1z", "f", "pos"])
    def ols(d, cols, y="ex"):
        X = np.column_stack([np.ones(len(d))] + [d[c].values for c in cols])
        beta, *_ = np.linalg.lstsq(X, d[y].values, rcond=None)
        res = d[y].values - X @ beta
        s2 = res @ res / (len(d) - X.shape[1])
        se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
        return pd.DataFrame({"beta": beta, "t": beta / se}, index=["const"] + cols).round(5)
    for H in [1, 3, 5, 10]:
        g = grid(H)
        g["dn"] = np.minimum(g["r1z"], 0)
        g["up"] = np.maximum(g["r1z"], 0)
        out[f"H{H}_ols_f_dn_up_n{len(g)}"] = ols(g, ["f", "dn", "up"])
        if H == 10:
            G = g
    g = G
    g["b"] = pd.qcut(g["r1z"].rank(method="first"), 10, labels=False)
    t = g.groupby("b").agg(lo=("r1z", "min"), hi=("r1z", "max"), n=("ex", "size"), mean_ex=("ex", "mean"), sd=("ex", "std"), mean_exz=("exz", "mean"))
    t["t"] = t["mean_ex"] / (t["sd"] / np.sqrt(t["n"])); out["H10_by_r1z_decile"] = t.drop(columns="sd").round(4)
    for h in [1, 2]:
        out[f"H10_half{h}_ols"] = ols(g[g["half"] == h], ["f", "dn", "up"])
    # per coin slope sign on dn
    pc = []
    for coin, s in g.groupby("coin"):
        if len(s) < 40: continue
        lr = stats.linregress(s["dn"], s["ex"]); pc.append(dict(coin=coin, n=len(s), slope=lr.slope, t=lr.slope / lr.stderr))
    pc = pd.DataFrame(pc).set_index("coin").round(4); out["H10_dn_slope_per_coin"] = pc
    # pos30 given forecast
    out["H10_ols_f_pos"] = ols(g, ["f", "pos"])
    g["pb"] = pd.qcut(g["pos"].rank(method="first"), 5, labels=False)
    g["fb"] = pd.qcut(g["f"].rank(method="first"), 3, labels=False)
    out["H10_ex_by_pos_x_ftercile"] = g.pivot_table(index="pb", columns="fb", values="ex", aggfunc="mean").round(4)
    # exz version (strength)
    out["H10_ols_exz"] = ols(g, ["f", "dn", "up"], y="exz")
    return out
