def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 3
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            if len(b) < 40: continue
            rr = (b.high - b.low) / (b.high - b.low).rolling(30, min_periods=20).mean()
            clv = ((b.close - b.low) / (b.high - b.low)).replace([np.inf, -np.inf], np.nan)
            r1 = b.close.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            r5 = b.close / b.close.shift(5) - 1
            z5 = r5 / (vol30 * np.sqrt(5))
            r10 = b.close / b.close.shift(10) - 1
            z10 = r10 / (vol30 * np.sqrt(10))
            r60 = b.close / b.close.shift(60) - 1
            fwd = b.close.shift(-H) / b.close - 1
            reg = b.regime
            for i in range(0, len(b), H):
                tr = r60.iloc[i]
                if pd.notna(tr):
                    prof = "rising" if tr > 0.10 else ("falling" if tr < -0.10 else "choppy")
                else:
                    prof = "falling" if reg.iloc[i] != "chop" else "notfall_na"
                rows.append(dict(coin=coin, w=w, day=str(b.timestamp.iloc[i])[:10], rr=rr.iloc[i], clv=clv.iloc[i],
                                 z5=z5.iloc[i], z10=z10.iloc[i], fwd=fwd.iloc[i], prof=prof,
                                 yr=pd.Timestamp(b.timestamp.iloc[i]).year))
    d = pd.DataFrame(rows).dropna(subset=["fwd"])
    drift = d.groupby("coin").fwd.mean(); sd = d.groupby("coin").fwd.std()
    d["ex"] = d.fwd - d.coin.map(drift); d["exz"] = d.ex / d.coin.map(sd)
    def tday(g, col="ex"):
        s = g.groupby("day")[col].sum(); n = len(g); m = g[col].mean()
        se = np.sqrt((( g.groupby("day")[col].sum() - g.groupby("day").size()*m)**2).sum()) / n
        return m / se if se > 0 else np.nan
    def summ(g):
        return pd.Series({"n": len(g), "days": g.day.nunique(), "mean_ex": g.ex.mean(), "t_day": tday(g), "strength": g.exz.mean()})
    def slope(g, x):
        g = g.dropna(subset=[x, "exz"])
        if len(g) < 20: return pd.Series({"n": len(g)})
        r = stats.linregress(g[x], g.exz)
        return pd.Series({"n": len(g), "slope": r.slope, "t": r.slope / r.stderr})
    out = {}
    out["profile_counts"] = d.prof.value_counts()
    d["z5q"] = pd.qcut(d.z5, 5, labels=False)
    out["z5q_by_prof"] = d.groupby(["prof", "z5q"]).apply(summ)
    out["z5_slope_by_prof"] = d.groupby("prof").apply(lambda g: slope(g, "z5"))
    out["z10_slope_by_prof"] = d.groupby("prof").apply(lambda g: slope(g, "z10"))
    out["z5_slope_by_window"] = d.groupby("w").apply(lambda g: slope(g, "z5"))
    out["z5_slope_by_coin"] = d.groupby("coin").apply(lambda g: slope(g, "z5"))
    out["z5_slope_by_year"] = d.groupby("yr").apply(lambda g: slope(g, "z5"))
    out["z5_slope_all_daycluster"] = pd.Series({"top_minus_bottom_q": d[d.z5q==4].ex.mean()-d[d.z5q==0].ex.mean()})
    wide = d[d.rr >= 1.5].copy()
    wide["clvq"] = pd.cut(wide.clv, [0, .33, .67, 1.0001], labels=["low", "mid", "high"], include_lowest=True)
    out["wide_by_prof_clv"] = wide.groupby(["prof", "clvq"]).apply(summ)
    out["wide_by_prof"] = wide.groupby("prof").apply(summ)
    out["rr_slope_by_prof"] = d.groupby("prof").apply(lambda g: slope(g, "rr"))
    nf = d[d.prof.isin(["rising", "choppy"])]
    out["rr_slope_notfalling_by_window"] = nf.groupby("w").apply(lambda g: slope(g, "rr"))
    return out
