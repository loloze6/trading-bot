def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            f = b["forecast"].fillna(0).values
            lr = np.log(c)
            n = len(b)
            s50 = pd.Series(c).rolling(50).mean().values
            for i in range(0, n - 10, 10):
                if i < 20: continue
                rows.append(dict(coin=coin, year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                 f=f[i], fwd=c[i+10]/c[i]-1, p20=lr[i]-lr[i-20],
                                 p10=lr[i]-lr[i-10],
                                 above50=(c[i] > s50[i]) if not np.isnan(s50[i]) else np.nan))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    d["pos"] = (d.fwd > 0).astype(float) - d.groupby("coin")["fwd"].transform(lambda x: (x > 0).mean())
    def summ(g):
        s = g["ex"]
        return pd.Series({"n": len(s), "mean_ex": s.mean(), "t": s.mean()/s.std()*np.sqrt(len(s)) if len(s) > 2 else np.nan,
                          "pos_minus": g["pos"].mean(), "median_ex": s.median()})
    out = {}
    d["act"] = d.f > 0
    d["up20"] = d.p20 > 0
    out["act_x_up20"] = d.groupby(["act", "up20"]).apply(summ)
    au = d[d.act & d.up20]
    out["act_up20_by_coin"] = au.groupby("coin").apply(summ)
    out["act_up20_by_year"] = au.groupby("year").apply(summ)
    a = d[d.act].copy()
    a["p20q"] = pd.qcut(a.p20, 5)
    out["act_by_p20_quint"] = a.groupby("p20q").apply(summ)
    out["act_x_above50"] = a.groupby("above50").apply(summ)
    a["up10"] = a.p10 > 0
    out["act_by_up10"] = a.groupby("up10").apply(summ)
    # slope of ex on p20 within active, and in flat
    from scipy import stats
    for nm, g in [("act", a), ("flat", d[~d.act])]:
        r = stats.linregress(g.p20, g.ex)
        out["slope_ex_on_p20_" + nm] = f"slope={r.slope:.4f} t={r.slope/r.stderr:.2f} n={len(g)}"
    return out
