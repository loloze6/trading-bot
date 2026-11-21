def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = pd.Series(b["close"].astype(float).values)
            n = len(c)
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change().values
            lr = np.log(c).diff()
            vol30 = lr.rolling(30, min_periods=20).std().values
            r28 = c.pct_change(28).values
            r5p = c.pct_change(5).values
            hi90 = c.rolling(90, min_periods=30).max().values
            near = (c / hi90 - 1).values
            comb = b.get("debug_info.components.combined.post_pipeline_value", pd.Series([np.nan]*n))
            best = b.get("debug_info.components.best.post_pipeline_value", pd.Series([np.nan]*n))
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, win=w, fwd=c[i+H]/c[i]-1, r1=r1[i], vol=vol30[i], r28=r28[i],
                    r5p=r5p[i], near=near[i], comb=comb.iloc[i], best=best.iloc[i],
                    act=(b["regime"].iloc[i]=="trending"), wd=ts.iloc[i].weekday(), yr=ts.iloc[i].year))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    d["r1z"] = d["r1"] / d["vol"]
    d["absr1z"] = d["r1z"].abs()
    d["r28z"] = d["r28"] / (d["vol"]*np.sqrt(28))
    d["exz"] = d["ex"] / (d["vol"]*np.sqrt(5))
    out = {}
    def ic(x, col, by):
        x = x.dropna(subset=[col, "ex"])
        res = {}
        for k, g in x.groupby(by):
            if len(g) > 20:
                r, p = stats.spearmanr(g[col], g["ex"]); res[k] = (len(g), r, r*np.sqrt(len(g)))
        return pd.DataFrame(res, index=["n","ic","t_approx"]).T
    a = d[d.act & d.comb.notna()]
    out["comb_ic_by_year_active"] = ic(a, "comb", "yr")
    out["comb_ic_by_coin_active"] = ic(a, "comb", "coin")
    a2 = a.assign(diff=a.comb - a.best)
    out["diff_ic_by_year"] = ic(a2, "diff", "yr")
    # pooled signals: graded ics overall, by year
    for col in ["r1z","absr1z","r28z","near","r5p","vol"]:
        x = d.dropna(subset=[col,"ex"])
        r, p = stats.spearmanr(x[col], x["ex"])
        out["ic_all_"+col] = f"n={len(x)} ic={r:.4f} p={p:.4f}"
    out["absr1z_ic_by_year"] = ic(d, "absr1z", "yr")
    out["absr1z_ic_by_coin"] = ic(d, "absr1z", "coin")
    out["r28z_ic_by_year"] = ic(d, "r28z", "yr")
    out["r28z_ic_by_coin"] = ic(d, "r28z", "coin")
    # abs r1 by sign
    x = d.dropna(subset=["r1z","ex"])
    x = x.assign(q=pd.qcut(x["absr1z"], 5, labels=False), s=np.sign(x["r1z"]))
    g = x.groupby(["q","s"])["ex"]
    out["absr1z_q_by_sign"] = pd.DataFrame({"n": g.size(), "m": g.mean(), "t": g.mean()/(g.std()/np.sqrt(g.size()))})
    # weekday by year halves
    d["half"] = np.where(d.yr <= 2021, "early", "late")
    g = d.groupby(["half","wd"])["ex"]
    out["weekday_by_half"] = pd.DataFrame({"n": g.size(), "m": g.mean(), "t": g.mean()/(g.std()/np.sqrt(g.size()))})
    # book largest losses: what precedes
    dd = []
    for coin, wins in data["days"].items():
        for w, dy in wins.items():
            dd.append(dy.assign(coin=coin)[["book_return","coin_return"]])
    dd = pd.concat(dd).dropna()
    out["book_vs_coin_corr"] = float(dd.corr().iloc[0,1])
    q = dd["coin_return"].quantile([0.1,0.9]).values
    out["book_on_coin_tails"] = pd.DataFrame({
        "coin_down10": [dd.loc[dd.coin_return<q[0],"book_return"].mean()],
        "coin_mid": [dd.loc[(dd.coin_return>=q[0])&(dd.coin_return<=q[1]),"book_return"].mean()],
        "coin_up10": [dd.loc[dd.coin_return>q[1],"book_return"].mean()]})
    return out
