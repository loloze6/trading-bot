def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        rets = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                rets.append(c[i + H] / c[i] - 1)
        mu = np.mean(rets); sd = np.std(rets, ddof=1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            mom28 = c / c.shift(28) - 1
            near90 = c / c.rolling(90, min_periods=30).max() - 1
            vol = -r1.rolling(30, min_periods=15).std()
            ret90 = c / c.shift(90) - 1
            fwd = c.shift(-H) / c - 1
            combo = b["debug_info.components.combo.post_pipeline_value"] if "debug_info.components.combo.post_pipeline_value" in b else pd.Series(np.nan, index=b.index)
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, len(b) - H, H):
                rows.append(dict(coin=coin, w=w, yr=ts.iat[i].year, reg=b["regime"].iat[i], fc=b["forecast"].iat[i],
                                 combo=combo.iat[i], r=fwd.iat[i] - mu, tot=fwd.iat[i], z=(fwd.iat[i]-mu)/sd,
                                 mom28=mom28.iat[i], rev1=-r1.iat[i], near=near90.iat[i], vol=vol.iat[i], ret90=ret90.iat[i]))
    df = pd.DataFrame(rows).dropna(subset=["r"])
    dec = df[df["reg"] == "mean_reversion"]
    ris = df[df["reg"] != "mean_reversion"]
    # what the combo loads on in declines
    cc = {}
    for s in ["mom28", "rev1", "near", "vol"]:
        x = dec[["combo", s]].dropna()
        cc[s] = dict(n=len(x), spearman=stats.spearmanr(x["combo"], x[s])[0])
    out["decline: combo vs each signal"] = pd.DataFrame(cc).T
    def tt(x):
        x = x.dropna(); return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))))
    # graded: 28d return quintiles in rising and declining, mean unusual move and total
    for nm, sub in [("rising90", ris), ("decline", dec)]:
        s = sub.dropna(subset=["mom28"]).copy()
        s["q"] = pd.qcut(s["mom28"], 5, labels=False)
        out[nm + ": by 28d return quintile"] = s.groupby("q").agg(n=("r","size"), mom28=("mom28","mean"), r=("r","mean"), tot=("tot","mean"), z=("z","mean"))
        top = s[s.q==4]["r"]; bot = s[s.q==0]["r"]
        out[nm + ": top minus bottom quintile"] = pd.Series(dict(diff=top.mean()-bot.mean(), t=stats.ttest_ind(top, bot, equal_var=False)[0]))
    # decline: depth of fall from 90d high, graded
    s = dec.dropna(subset=["near"]).copy()
    s["q"] = pd.qcut(s["near"], 5, labels=False)
    out["decline: by distance below 90d high"] = s.groupby("q").agg(n=("r","size"), near=("near","mean"), r=("r","mean"), tot=("tot","mean"), z=("z","mean"))
    # contrarian signal in declines: -mom28 sign; per case move & strength
    s = dec.dropna(subset=["mom28"]).copy()
    sg = -np.sign(s["mom28"] - s["mom28"].median())
    out["decline: bet against 28d return (vs median)"] = pd.DataFrame({"unusual": tt(sg*s["r"]), "strength": tt(sg*s["z"])}).T
    s = ris.dropna(subset=["mom28"]).copy()
    sg = np.sign(s["mom28"])
    out["rising: bet with sign of 28d return"] = pd.DataFrame({"unusual": tt(sg*s["r"]), "total": tt(sg*s["tot"]), "strength": tt(sg*s["z"])}).T
    # by year: decline signed move of forecast
    d = dec[dec.fc != 0].copy(); d["sr"] = np.sign(d.fc)*d.r
    out["decline forecast signed move by year"] = d.groupby("yr")["sr"].apply(tt).unstack()
    out["decline short-side raw total by year"] = d[d.fc<0].groupby("yr")["tot"].apply(tt).unstack()
    return out
