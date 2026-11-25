def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            for h in (5, 10, 20):
                for i in range(0, n - h, h):
                    r = c[i + h] / c[i] - 1
                    f30 = c[i] / c[i - 30] - 1 if i >= 30 else np.nan
                    rows.append(dict(coin=coin, w=w, h=h, i=i, ret=r,
                                     fc=df["forecast"].iloc[i], reg=df["regime"].iloc[i],
                                     year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                     f30=f30))
    g = pd.DataFrame(rows)
    g["mu"] = g.groupby(["coin", "h"])["ret"].transform("mean")
    g["ex"] = g["ret"] - g["mu"]
    out = {}
    def tt(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=(x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan)))
    tr = g[g.reg == "trending"].copy()
    tr["grp"] = np.where(tr.fc < 0, "quiet", "heavy")
    out["trend_by_h_grp_excess"] = tr.groupby(["h", "grp"])["ex"].apply(tt).unstack()
    out["trend_by_h_grp_raw"] = tr.groupby(["h", "grp"])["ret"].apply(tt).unstack()
    t5 = tr[tr.h == 5].copy()
    q = t5[t5.fc < 0].copy()
    q["fq"] = pd.qcut(q.fc, 4, labels=["q1_quietest", "q2", "q3", "q4"])
    out["quiet_by_forecast_quartile_ex5"] = q.groupby("fq")["ex"].apply(tt).unstack()
    out["trend5_by_coin_grp"] = t5.groupby(["coin", "grp"])["ex"].apply(tt).unstack()
    out["trend5_by_year_grp"] = t5.groupby(["year", "grp"])["ex"].apply(tt).unstack()
    # depth of fall: brief's first claim
    d = t5.dropna(subset=["f30"]).copy()
    d["dq"] = pd.qcut(d.f30, 3, labels=["deep", "mid", "shallow"])
    out["trend5_by_fall_depth"] = d.groupby(["dq"])["ex"].apply(tt).unstack()
    out["trend5_depth_x_grp"] = d.groupby(["dq", "grp"])["ex"].apply(tt).unstack()
    for h in (5, 10, 20):
        dd = tr[(tr.h == h)].dropna(subset=["f30"])
        rho, p = stats.spearmanr(dd.f30, dd.ex)
        out[f"spearman_f30_ex_h{h}"] = f"rho {rho:.3f} p {p:.3f} n {len(dd)}"
    # other regimes
    out["all_regimes_ex5"] = g[g.h == 5].groupby("reg")["ex"].apply(tt).unstack()
    return out
