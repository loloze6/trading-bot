def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [18, 36]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            rs = np.concatenate(rs)
            drift[(coin, h)] = (np.nanmean(rs), np.nanstd(rs))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; hi = df["high"]; lo = df["low"]
            prmin = lo.shift(1).rolling(12).min()
            prmax = hi.shift(1).rolling(12).max()
            mbr = (hi - lo).shift(1).rolling(180, min_periods=90).mean()
            width = (prmax - prmin) / mbr
            ret180 = c / c.shift(180) - 1
            brk = (c < prmin)
            n = len(df)
            for h in H:
                for start in range(0, n - h, h):
                    for i in range(start, min(start + h, n - h)):
                        if brk.iloc[i] and not np.isnan(width.iloc[i]) and not np.isnan(ret180.iloc[i]):
                            r = c.iloc[i + h] / c.iloc[i] - 1
                            m, s = drift[(coin, h)]
                            rows.append(dict(coin=coin, w=w, h=h, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                             ret180=ret180.iloc[i], width=width.iloc[i],
                                             unusual_short=-(r - m), total_short=-r, strength=-(r - m) / s))
                            break
    d = pd.DataFrame(rows)
    def summ(g):
        x = g["unusual_short"]
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              total=g["total_short"].mean(), strength=g["strength"].mean()))
    out = {}
    dn = d[d.ret180 <= 0].copy()
    for h in H:
        g = dn[dn.h == h].copy()
        g["wq"] = pd.qcut(g["width"], 5, labels=False)
        out[f"down_h{h}_by_widthq"] = g.groupby("wq").apply(summ)
        rho, p = stats.spearmanr(g["width"], g["unusual_short"])
        out[f"down_h{h}_spearman_width"] = f"rho={rho:.4f} p={p:.4f} n={len(g)}"
    g = dn[dn.h == 18].copy()
    g["narrow"] = g["width"] <= g["width"].median()
    out["down_h18_by_year_narrow"] = g.groupby(["year", "narrow"]).apply(summ)
    cc = g[g.narrow].groupby("coin").apply(summ)
    out["down_h18_narrow_by_coin"] = cc
    out["down_h18_narrow_coins_positive_share"] = float((cc["mean"] > 0).mean())
    g["rq"] = pd.qcut(g["ret180"], 4, labels=False)
    out["down_h18_by_rq_narrow"] = g.groupby(["rq", "narrow"]).apply(summ)
    allh = d[d.h == 18]
    rho, p = stats.spearmanr(allh["ret180"], allh["unusual_short"])
    out["all_h18_spearman_ret180"] = f"rho={rho:.4f} p={p:.4f} n={len(allh)}"
    return out
