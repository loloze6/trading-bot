def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 5
    # coin mean 5-bar return over all windows
    rows = []
    bookrows = []
    for coin, wins in data["bars"].items():
        rets = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                rets.append(c[i + H] / c[i] - 1)
        mu = np.mean(rets) if rets else 0.0
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            mom28 = c / c.shift(28) - 1
            rev1 = -r1
            hi = c.rolling(60, min_periods=20).max()
            near = c / hi - 1
            vol = -r1.rolling(30, min_periods=15).std()
            ret90 = c / c.shift(90) - 1
            ret30 = c / c.shift(30) - 1
            fwd = c.shift(-H) / c - 1
            pos = b["postRebalance_current_allocation"]
            g = b["forecast"]
            for i in range(0, len(b) - H, H):
                rows.append(dict(coin=coin, w=w, reg=b["regime"].iat[i], fc=g.iat[i],
                                 combo=b.get("debug_info.components.combo.post_pipeline_value", pd.Series(np.nan, index=b.index)).iat[i],
                                 pos=pos.iat[i], r=fwd.iat[i] - mu, tot=fwd.iat[i],
                                 mom28=mom28.iat[i], rev1=rev1.iat[i], near=near.iat[i], vol=vol.iat[i],
                                 ret90=ret90.iat[i], ret30=ret30.iat[i]))
            # bar-level gain split by side
            gain = pos * (c.shift(-1) / c - 1)
            bookrows.append(pd.DataFrame(dict(coin=coin, side=np.sign(pos), gain=gain, reg=b["regime"])))
    df = pd.DataFrame(rows)
    out["regime share of grid"] = df["reg"].value_counts(normalize=True)
    d = df[df["reg"] == "mean_reversion"].dropna(subset=["r"])
    d = d[d["fc"] != 0]
    d["s"] = np.sign(d["fc"])
    d["sr"] = d["s"] * d["r"]
    d["stot"] = d["s"] * d["tot"]
    def tt(x):
        x = x.dropna(); return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x)>2 else np.nan))
    out["signed unusual move by forecast side"] = d.groupby("s")["sr"].apply(tt).unstack()
    out["signed total move by forecast side"] = d.groupby("s")["stot"].apply(tt).unstack()
    d["fq"] = pd.qcut(d["fc"], 5, labels=False, duplicates="drop")
    out["raw r by forecast quintile"] = d.groupby("fq").agg(n=("r","size"), fc=("fc","mean"), r=("r","mean"), tot=("tot","mean"))
    out["signed unusual move by coin"] = d.groupby("coin")["sr"].apply(tt).unstack()
    # single signals on decline cases and on all cases
    allc = df.dropna(subset=["r"])
    sig = {}
    for name, sub in [("decline", d), ("all", allc), ("rising90", allc[allc["reg"] != "mean_reversion"])]:
        for s in ["mom28", "rev1", "near", "vol", "ret30", "ret90"]:
            x = sub[[s, "r"]].dropna()
            if len(x) > 10:
                rho, p = stats.spearmanr(x[s], x["r"])
                sig[(name, s)] = dict(n=len(x), spearman=rho, t=rho*np.sqrt((len(x)-2)/(1-rho**2)))
    out["single signals vs next 5d unusual move"] = pd.DataFrame(sig).T
    # by depth of ret90 in decline
    dd = d.dropna(subset=["ret90"]).copy()
    if len(dd) > 20:
        dd["q"] = pd.qcut(dd["ret90"], 3, labels=False)
        out["decline by ret90 tercile"] = dd.groupby("q").agg(n=("r","size"), ret90=("ret90","mean"), r=("r","mean"), sr=("sr","mean"), short_share=("s", lambda x:(x<0).mean()))
    # mom28 terciles within decline: what follows
    d2 = d.dropna(subset=["mom28"]).copy()
    d2["q"] = pd.qcut(d2["mom28"], 5, labels=False)
    out["decline: r by 28d return quintile"] = d2.groupby("q").agg(n=("r","size"), mom28=("mom28","mean"), r=("r","mean"), short_share=("s", lambda x:(x<0).mean()))
    br = pd.concat(bookrows).dropna()
    out["bar gain by side"] = br.groupby("side")["gain"].agg(["size", "mean", "sum"])
    # book daily
    days = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            days.append(x.assign(coin=coin, w=w))
    D = pd.concat(days)
    dm = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book vs hold daily"] = pd.DataFrame(dict(mean=dm.mean(), sharpe=dm.mean()/dm.std()*np.sqrt(365)))
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tr.append(t.assign(coin=coin))
    T = pd.concat(tr)
    out["trades by side"] = T.groupby("side").agg(n=("side","size"), pl=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"), days=("duration_minutes", lambda x: x.mean()/1440))
    return out
