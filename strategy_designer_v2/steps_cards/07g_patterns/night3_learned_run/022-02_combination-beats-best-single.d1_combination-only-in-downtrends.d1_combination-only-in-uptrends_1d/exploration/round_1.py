def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            ts = pd.to_datetime(b["timestamp"])
            r1 = pd.Series(c).pct_change().values
            lr = np.log(pd.Series(c)).diff()
            vol30 = lr.rolling(30, min_periods=20).std().values
            r28 = pd.Series(c).pct_change(28).values
            r90 = pd.Series(c).pct_change(90).values
            hi90 = pd.Series(c).rolling(90, min_periods=30).max().values
            near = c / hi90 - 1
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, win=w, pos=i,
                    fwd=c[i+H]/c[i]-1, r1=r1[i], vol=vol30[i], r28=r28[i], r90=r90[i], near=near[i],
                    fc=b["forecast"].iloc[i],
                    comb=b.get("debug_info.components.combined.post_pipeline_value", pd.Series([np.nan]*n)).iloc[i],
                    best=b.get("debug_info.components.best.post_pipeline_value", pd.Series([np.nan]*n)).iloc[i],
                    alloc=b["postRebalance_current_allocation"].iloc[i],
                    wd=ts.iloc[i].weekday(), yr=ts.iloc[i].year))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    d["volz"] = d["vol"] / d.groupby("coin")["vol"].transform("median")
    def tab(col, q=5, sub=None):
        x = d if sub is None else d[sub]
        x = x.dropna(subset=[col, "ex"])
        x = x.assign(b=x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False)))
        g = x.groupby("b")["ex"]
        return pd.DataFrame({"n": g.size(), "mean_ex": g.mean(), "t": g.mean()/(g.std()/np.sqrt(g.size())),
                             "mean_raw": x.groupby("b")["fwd"].mean()})
    out = {}
    out["by_r1_quint"] = tab("r1")
    out["by_r28_quint"] = tab("r28")
    out["by_r90_quint"] = tab("r90")
    out["by_near_quint"] = tab("near")
    out["by_vol_quint"] = tab("volz")
    out["by_comb_quint_active"] = tab("comb", sub=d["comb"].notna())
    out["by_best_quint_active"] = tab("best", sub=d["comb"].notna())
    g = d.groupby("wd")["ex"]
    out["weekday"] = pd.DataFrame({"n": g.size(), "m": g.mean(), "t": g.mean()/(g.std()/np.sqrt(g.size()))})
    g = d.groupby("yr")["ex"]
    out["year"] = pd.DataFrame({"n": g.size(), "m": g.mean(), "t": g.mean()/(g.std()/np.sqrt(g.size()))})
    a = d[d["comb"].notna()]
    out["active_share_long"] = float((a["fc"] > 0).mean())
    out["active_long_ex"] = float(a.loc[a.fc>0,"ex"].mean()); out["active_short_ex"] = float(a.loc[a.fc<0,"ex"].mean())
    out["corr_comb_best"] = float(a[["comb","best"]].corr().iloc[0,1])
    # book daily: long vs short
    dd = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float)
            g_ = b["postRebalance_current_allocation"].astype(float) * (c.shift(-1)/c - 1)
            dd.append(pd.DataFrame({"g": g_, "al": b["postRebalance_current_allocation"].astype(float), "coin": coin}))
    dd = pd.concat(dd).dropna()
    out["gain_long_short"] = pd.DataFrame({"sum_g": dd.groupby(np.sign(dd.al))["g"].sum(), "n": dd.groupby(np.sign(dd.al))["g"].size(), "mean": dd.groupby(np.sign(dd.al))["g"].mean()})
    out["gain_by_coin"] = dd.groupby("coin")["g"].agg(["mean","count"])
    return out
