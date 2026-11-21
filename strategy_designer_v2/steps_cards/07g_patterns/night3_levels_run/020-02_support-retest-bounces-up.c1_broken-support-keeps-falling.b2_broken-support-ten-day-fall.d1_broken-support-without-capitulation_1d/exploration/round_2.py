def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            lr = np.r_[np.nan, np.diff(np.log(c))]
            for i in range(0, n - H, H):
                r = c[i+H]/c[i]-1
                p10 = c[i]/c[i-10]-1 if i >= 10 else np.nan
                p5 = c[i]/c[i-5]-1 if i >= 5 else np.nan
                p1 = c[i]/c[i-1]-1 if i >= 1 else np.nan
                v = np.nanstd(lr[max(1,i-19):i+1]) if i >= 10 else np.nan
                rows.append(dict(coin=coin, w=w, r=r, f=b["forecast"].iloc[i],
                                 reg=b["regime"].iloc[i], p10=p10, p5=p5, p1=p1, v=v,
                                 yr=pd.Timestamp(b["timestamp"].iloc[i]).year))
    g = pd.DataFrame(rows)
    g["mu"] = g.groupby("coin")["r"].transform("mean")
    g["sd"] = g.groupby("coin")["r"].transform("std")
    g["ex"] = (g["r"]-g["mu"])/g["sd"]
    g["xr"] = g["r"]-g["mu"]
    # graded continuation: 10-day return scaled by vol
    g["z10"] = g["p10"]/(g["v"]*np.sqrt(10))
    res = {}
    for col in ["p10","z10","p5","p1"]:
        d = g.dropna(subset=[col])
        rho, p = stats.spearmanr(d[col], d["ex"])
        res[col] = dict(rho=rho, p=p, n=len(d))
    out["spearman_past_vs_ex10_pooled"] = pd.DataFrame(res).T
    pc = []
    for coin, d in g.dropna(subset=["z10"]).groupby("coin"):
        rho, p = stats.spearmanr(d["z10"], d["ex"])
        pc.append(dict(coin=coin, rho=rho, n=len(d)))
    out["spearman_z10_by_coin"] = pd.DataFrame(pc)
    # signed-z10 bet: sign-size continuation gain in excess
    d = g.dropna(subset=["z10"]).copy()
    d["bet"] = np.clip(d["z10"], -2, 2) * d["xr"]
    out["z10_bet_by_year"] = d.groupby("yr")["bet"].agg(["mean","count"])
    out["z10_bet_by_regime"] = d.groupby("reg")["bet"].agg(["mean","count","std"])
    # mean-reversion regime: does forecast size matter or just being in regime?
    m = g[g.reg == "mean_reversion"].copy()
    m["fbin"] = pd.cut(m["f"].abs(), [-0.01, 0.0001, 1, 5, 21])
    t = m.groupby("fbin")["xr"].agg(["mean","count","std"])
    t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["deepfall_xr10_by_absforecast"] = t
    # unknown regime: shorts by forecast size
    u = g[g.reg == "unknown"].copy()
    u["fbin"] = pd.cut(u["f"].abs(), [-0.01, 0.0001, 1, 5, 21])
    t = u.groupby("fbin")["xr"].agg(["mean","count","std"])
    t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["normal_xr10_by_absforecast"] = t
    t = g.groupby("reg")["r"].agg(["mean","count","std"])
    t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["raw_r10_by_regime"] = t
    # deep-fall regime: by coin, mean raw r
    out["deepfall_r10_by_coin"] = m.groupby("coin")["r"].agg(["mean","count"])
    out["deepfall_r10_by_year"] = m.groupby("yr")["r"].agg(["mean","count"])
    # daily: next-day return after large daily moves (vol-scaled), from days table
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.reset_index(drop=True)
            cr = x["coin_return"]
            vv = cr.rolling(20, min_periods=10).std()
            dd.append(pd.DataFrame({"z": cr/vv, "nxt": cr.shift(-1), "coin": coin}))
    dd = pd.concat(dd).dropna()
    dd["zb"] = pd.qcut(dd["z"], 5, labels=False)
    t = dd.groupby("zb")["nxt"].agg(["mean","count","std"])
    t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["nextday_by_today_z_quintile"] = t
    # book: daily book returns by regime state and side
    return out
