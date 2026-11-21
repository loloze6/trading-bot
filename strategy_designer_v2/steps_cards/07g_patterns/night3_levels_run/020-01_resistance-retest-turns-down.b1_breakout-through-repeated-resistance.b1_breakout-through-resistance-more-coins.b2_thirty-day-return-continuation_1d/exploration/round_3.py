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
                wn = int(w[1:])
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, win=w, half=1 if wn <= 12 else 2, f=b["forecast"].iloc[i],
                                     fwd=c.iloc[i + H] / c.iloc[i] - 1, r1=r1.iloc[i], vol=vol.iloc[i]))
        g = pd.DataFrame(rows)
        g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
        g["usual"] = g.groupby("coin")["fwd"].transform("std")
        g["r1z"] = g["r1"] / g["vol"]
        return g.dropna(subset=["ex", "r1z", "f"])
    for H in [1, 3]:
        g = grid(H)
        g["b"] = pd.qcut(g["r1z"].rank(method="first"), 10, labels=False)
        t = g.groupby("b").agg(lo=("r1z", "min"), hi=("r1z", "max"), n=("ex", "size"), mean_ex=("ex", "mean"), sd=("ex", "std"))
        t["strength"] = g.assign(s=g["ex"] / g["usual"]).groupby("b")["s"].mean()
        t["t"] = t["mean_ex"] / (t["sd"] / np.sqrt(t["n"]))
        out[f"H{H}_by_r1z_decile"] = t.drop(columns="sd").round(4)
        d = g[g["r1z"] < 0]
        res = []
        for k, s in d.groupby("half"):
            lr = stats.linregress(s["r1z"], s["ex"]); res.append(dict(half=k, n=len(s), slope=lr.slope, t=lr.slope / lr.stderr))
        for k, s in d.groupby(d["f"] > 0):
            lr = stats.linregress(s["r1z"], s["ex"]); res.append(dict(half=f"f_pos_{k}", n=len(s), slope=lr.slope, t=lr.slope / lr.stderr))
        out[f"H{H}_downday_slope_by_half_and_trend"] = pd.DataFrame(res).round(5)
        pc = []
        for coin, s in d.groupby("coin"):
            lr = stats.linregress(s["r1z"], s["ex"]); pc.append(lr.slope)
        pc = np.array(pc)
        out[f"H{H}_downday_coins_negative_slope"] = f"{(pc < 0).sum()} of {len(pc)}"
        # size of cases: down days beyond 1 usual daily move
        s = g[g["r1z"] < -1]
        out[f"H{H}_after_down_gt1sd"] = pd.Series({"n": len(s), "unusual": s["ex"].mean(), "total": s["fwd"].mean(),
                                                  "strength": (s["ex"] / s["usual"]).mean(),
                                                  "t": s["ex"].mean() / (s["ex"].std() / np.sqrt(len(s)))}).round(4)
    g = grid(10)
    d = g[g["f"] < 0].copy()
    d["b"] = pd.qcut(d["f"].rank(method="first"), 4, labels=False)
    t = d.groupby("b").agg(lo=("f", "min"), hi=("f", "max"), n=("ex", "size"), mean_ex=("ex", "mean"), sd=("ex", "std"))
    t["t"] = t["mean_ex"] / (t["sd"] / np.sqrt(t["n"]))
    out["H10_negative_forecast_quartiles"] = t.drop(columns="sd").round(4)
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    tr["days"] = tr["duration_minutes"] / 1440
    out["trades_side_duration"] = tr.groupby("side").agg(n=("days", "size"), med_days=("days", "median"),
                                                         gross_mean=("profit_loss_percent", "mean"),
                                                         gross_median=("profit_loss_percent", "median"),
                                                         win_share=("profit_loss_percent", lambda x: (x > 0).mean())).round(3)
    return out
