def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    cm = {}
    for c in data["days"]:
        cm[c] = pd.concat([d["coin_return"] for d in data["days"][c].values()]).dropna().mean()
    # decomposition of book gain: drift part vs timing
    rows = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True).copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["coin"] = c; b["w"] = w
            rows.append(b)
    B = pd.concat(rows)
    B["pos"] = B["postRebalance_current_allocation"]
    out["mean_pos"] = pd.Series(dict(mean_pos=B["pos"].mean(), share_short=(B["pos"]<0).mean(),
        drift_part=(B["pos"]*B["coin"].map(cm)).mean()))
    # trades joined to entry features
    feats = []
    for c in data["trades"]:
        for w, t in data["trades"][c].items():
            if not len(t): continue
            b = data["bars"][c][w].reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]); cl = b["close"].values
            for _, r in t.iterrows():
                et = pd.to_datetime(r["entry_time"])
                i = ts.searchsorted(et, side="right") - 1
                if i < 0: continue
                vol = pd.Series(cl[max(0,i-20):i+1]).pct_change().std()
                feats.append(dict(coin=c, year=et.year,
                    net=r["net_profit_loss_percent"], gross=r["profit_loss_percent"],
                    ret20=cl[i]/cl[i-20]-1 if i>=20 else np.nan,
                    ret5=cl[i]/cl[i-5]-1 if i>=5 else np.nan,
                    ret60=cl[i]/cl[i-60]-1 if i>=60 else np.nan,
                    vol20=vol, dur=r["duration_minutes"]/1440))
    T = pd.DataFrame(feats)
    def s(g):
        return pd.Series(dict(n=len(g), gross=g["gross"].mean(), net=g["net"].mean(),
            t=stats.ttest_1samp(g["gross"],0).statistic if len(g)>2 else np.nan))
    out["trades_by_year"] = T.groupby("year").apply(s)
    for k in ["ret20","ret5","ret60","vol20"]:
        q = pd.qcut(T[k], 4, labels=False, duplicates="drop")
        out["trades_by_"+k] = T.groupby(q).apply(s).join(T.groupby(q)[k].mean())
    out["dur_dist"] = T["dur"].describe()
    # book deepest falls per coin-window chained: falls per year
    D = pd.concat([d.assign(coin=c, w=w) for c in data["days"] for w, d in data["days"][c].items()])
    D["year"] = pd.to_datetime(D["day"]).dt.year
    P = D.groupby(["w","day"])["book_return"].mean().dropna()
    eq = (1+P.groupby(level=0).apply(lambda x: x)).cumprod() if False else None
    chain = (1+P.reset_index(drop=True)).cumprod()
    dd = chain/chain.cummax()-1
    out["deepest_fall"] = pd.Series(dict(maxdd=dd.min(), total=chain.iloc[-1]-1))
    yrs = D.groupby(["w","day"])["year"].first()
    ddy = pd.Series(dd.values, index=yrs.loc[P.index].values)
    out["dd_by_year"] = ddy.groupby(level=0).min()
    return out
