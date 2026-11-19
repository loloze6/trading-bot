def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 72
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; v = df["volume"].values; n = len(df)
            ppv = df["debug_info.components.vol_share.post_pipeline_value"]
            for i in range(0, n, H):
                if i < 72: continue
                vv = v[i-71:i+1]
                share = np.sort(vv)[-3:].sum()/vv.sum() if vv.sum() > 0 else np.nan
                rows.append(dict(coin=coin, w=w, regime=df["regime"].iloc[i], ppv=ppv.iloc[i],
                                 share=share, past=c[i]/c[i-72]-1,
                                 f72=c[i+72]/c[i]-1 if i+72 < n else np.nan))
    d = pd.DataFrame(rows)
    d["x"] = d["f72"] - d.groupby("coin")["f72"].transform("mean")
    r = d[(d.regime == "mean_reversion")].dropna(subset=["ppv", "x", "share"]).copy()
    out = {}
    r["absq"] = pd.qcut(r.ppv.abs().rank(method="first"), 3, labels=["lo", "mid", "hi"])
    r["sgn"] = np.where(r.ppv < 0, "neg(conc)", "pos(even)")
    g = r.groupby(["absq", "sgn"])["x"].agg(["count", "mean"])
    out["absthird_by_sign"] = g
    # signed ppv thirds: most negative = most concentrated vs own past
    q = r.ppv.rank(pct=True)
    a = r.loc[q <= 1/3, "x"]; b = r.loc[q > 2/3, "x"]
    out["signed_conc_minus_even"] = pd.Series({"n_each": len(a), "conc_mean": a.mean(), "even_mean": b.mean(),
                                               "t": stats.ttest_ind(a, b, equal_var=False).statistic})
    # raw share thirds in pooled, and weighted by share rank within coin
    r["sq"] = r.groupby("coin")["share"].rank(pct=True)
    a = r.loc[r.sq > 2/3, "x"]; b = r.loc[r.sq <= 1/3, "x"]
    out["share_within_coin_top_minus_bot"] = pd.Series({"n_top": len(a), "top": a.mean(), "bot": b.mean(),
                                                        "t": stats.ttest_ind(a, b, equal_var=False).statistic})
    out["spearman_share_x"] = pd.Series(stats.spearmanr(r.share, r.x)[:2], index=["rho", "p"])
    out["spearman_share_x_smallrise"] = pd.Series(stats.spearmanr(r.loc[r.past < r.past.quantile(1/3), "share"], r.loc[r.past < r.past.quantile(1/3), "x"])[:2], index=["rho", "p"])
    return out
