def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            f = b["forecast"].values
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for i in range(0, n - 10, 10):
                r = c[i+10]/c[i]-1
                p30 = c[i]/c[i-30]-1 if i >= 30 else np.nan
                p10 = c[i]/c[i-10]-1 if i >= 10 else np.nan
                p60 = c[i]/c[i-60]-1 if i >= 60 else np.nan
                rows.append(dict(coin=coin, win=w, year=ts.iloc[i].year, f=f[i], r=r, p10=p10, p30=p30, p60=p60,
                                 key=ts.iloc[i].strftime("%Y%m%d")))
    d = pd.DataFrame(rows)
    d["ex"] = d["r"] - d.groupby("coin")["r"].transform("mean")
    d["pos"] = d["f"] > 0
    # cross-sectional market: mean return of all coins on same start date
    d["mkt"] = d.groupby("key")["r"].transform("mean")
    d["ncoin"] = d.groupby("key")["r"].transform("size")
    d["rel"] = d["r"] - d["mkt"]
    tt = lambda x: x.mean()/x.std()*np.sqrt(len(x)) if len(x) > 2 else np.nan
    out = {}
    dd = d.dropna(subset=["p30"]).copy()
    dd["mom"] = np.where(dd["p30"] > 0, "up30", "down30")
    P = dd[dd.pos]
    out["pos_mom_by_coin"] = P.groupby(["coin","mom"]).agg(n=("ex","size"), mean_ex=("ex","mean"), t=("ex", tt)).unstack()
    out["pos_mom_by_year"] = P.groupby(["year","mom"]).agg(n=("ex","size"), mean_ex=("ex","mean"), t=("ex", tt)).unstack()
    # slope of ex on forecast within up30 subset
    U = P[P.mom=="up30"]
    s = stats.linregress(U["f"], U["ex"])
    out["slope_f_within_pos_up30"] = pd.Series(dict(n=len(U), slope=s.slope, t=s.slope/s.stderr))
    # p10 and p60 conditioning
    for col in ["p10","p60"]:
        q = d.dropna(subset=[col])
        q = q[q.pos]
        out[f"pos_by_{col}_sign"] = q.groupby(q[col] > 0).agg(n=("ex","size"), mean_ex=("ex","mean"), t=("ex", tt),
                                                              hit=("r", lambda x: (x>0).mean()))
    # p30 quintiles among pos
    P2 = P.copy(); P2["q"] = pd.qcut(P2["p30"], 5)
    out["pos_by_p30_q"] = P2.groupby("q").agg(n=("ex","size"), mean_ex=("ex","mean"), t=("ex", tt))
    # market drowning: relative return to cross-section
    m = d[d.ncoin >= 4]
    out["rel_to_mkt_pos"] = m.groupby("pos").agg(n=("rel","size"), mean_rel=("rel","mean"), sd_rel=("rel","std"),
                                                  t=("rel", tt), sd_ex=("ex","std"))
    mm = m.dropna(subset=["p30"]).copy(); mm["mom"] = np.where(mm["p30"]>0,"up30","down30")
    out["rel_pos_mom"] = mm.groupby(["pos","mom"]).agg(n=("rel","size"), mean_rel=("rel","mean"), t=("rel", tt))
    out["share_var_market"] = float(1 - m["rel"].var()/m["r"].var())
    return out
