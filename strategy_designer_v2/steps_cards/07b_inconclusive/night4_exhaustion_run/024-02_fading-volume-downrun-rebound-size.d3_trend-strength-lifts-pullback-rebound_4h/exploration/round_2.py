def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = 18
    drift = {}; usual = {}
    for c in bars:
        rs = []
        for w, df in bars[c].items():
            cl = df["close"].values
            idx = np.arange(0, len(cl) - H, H)
            rs += list(cl[idx + H] / cl[idx] - 1)
        drift[c] = np.mean(rs); usual[c] = np.std(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; f = df["forecast"].fillna(0).values
            n = len(cl)
            d = np.diff(f, prepend=0.0)
            s = pd.Series(cl)
            r180 = s.pct_change(180).values
            r360 = s.pct_change(360).values
            r42 = s.pct_change(42).values
            lr = np.log(s).diff()
            vol = lr.rolling(180).std().values
            vol42 = lr.rolling(42).std().values
            drop = s.pct_change(2).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            seen = set()
            for i in range(n):
                if d[i] >= 2:
                    cell = i // H
                    if cell in seen: continue
                    seen.add(cell)
                    if i + H >= n: continue
                    u = (cl[i+H]/cl[i]-1) - drift[c]
                    rows.append(dict(coin=c, year=yr[i], f=f[i], u=u, s=u/usual[c],
                                     tot=cl[i+H]/cl[i]-1, r180=r180[i], r360=r360[i],
                                     r42=r42[i], vol=vol[i], vr=vol42[i]/vol[i], drop=drop[i]))
    cs = pd.DataFrame(rows)
    def summ(g, col="u"):
        x = g[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan))
    out = {}
    out["strength_mean"] = cs["s"].mean()
    cs["top"] = cs["f"] >= cs["f"].quantile(0.75)
    out["top_q_by_year"] = cs[cs.top].groupby("year").apply(summ)
    out["top_q_by_coin"] = cs[cs.top].groupby("coin").apply(summ)
    out["top_q_total"] = summ(cs[cs.top], "tot")
    out["top_q_strength"] = cs.loc[cs.top, "s"].mean()
    cs["r360pos"] = np.where(cs.r360.isna(), "na", np.where(cs.r360 > 0, "up", "down"))
    out["by_r360_sign"] = cs.groupby("r360pos").apply(summ)
    out["by_r42_sign"] = cs.groupby(cs.r42 > 0).apply(summ)
    out["by_r42_sign_top"] = cs[cs.top].groupby(cs.r42 > 0).apply(summ)
    out["by_vol_q"] = cs.groupby(pd.qcut(cs.vol.rank(method="first"), 3, labels=False)).apply(summ)
    out["by_volratio_q"] = cs.groupby(pd.qcut(cs.vr.rank(method="first"), 3, labels=False)).apply(summ)
    out["by_drop_q"] = cs.groupby(pd.qcut(cs.drop.rank(method="first"), 3, labels=False)).apply(summ)
    out["corr_f_u_spearman"] = cs[["f", "u"]].corr(method="spearman").iloc[0, 1]
    return out
