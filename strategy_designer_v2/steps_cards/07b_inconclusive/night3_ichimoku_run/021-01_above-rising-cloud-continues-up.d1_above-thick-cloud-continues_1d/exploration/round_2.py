def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; hi = df["high"]; lo = df["low"]
            mid = lambda n: (hi.rolling(n).max() + lo.rolling(n).min()) / 2
            a = ((mid(9) + mid(26)) / 2).shift(26); b = mid(52).shift(26)
            rw = df["debug_info.components.cloud_width.last_history_value"]
            r20 = c / c.shift(20) - 1
            for h in [10, 26]:
                for i in range(0, len(c) - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, reg=df["regime"].iloc[i] == "trending",
                                     fc=df["forecast"].iloc[i], rawW=rw.iloc[i],
                                     recomp_ok=not np.isnan(a.iloc[i]) and not np.isnan(b.iloc[i]),
                                     r20=r20.iloc[i], ret=c.iloc[i + h] / c.iloc[i] - 1))
    R = pd.DataFrame(rows)
    R["mu"] = R.groupby(["coin", "h"])["ret"].transform("mean")
    R["ex"] = R["ret"] - R["mu"]
    out = {}
    out["window_lengths"] = pd.Series([len(df) for wins in bars.values() for df in wins.values()]).describe()
    out["share_recomputable_26"] = R[(R.h == 26) & R.reg]["recomp_ok"].mean()
    for h in [10, 26]:
        d = R[(R.h == h) & R.reg].dropna(subset=["fc"]).copy()
        d["q"] = pd.qcut(d.fc.rank(method="first"), 4, labels=False)
        out[f"fcq_h{h}"] = d.groupby("q").agg(n=("ex", "size"), fc=("fc", "mean"), rawW=("rawW", "mean"),
            mean_ex=("ex", "mean"), med_ex=("ex", "median"), pos_share=("ex", lambda x: (x > 0).mean()))
        out[f"spearman_fc_ex_h{h}"] = pd.Series(stats.spearmanr(d.fc, d.ex)[:2], index=["rho", "p"])
        d2 = d[d.coin != "ZECUSD"]
        out[f"fcq_noZEC_h{h}"] = d2.groupby("q").agg(n=("ex", "size"), mean_ex=("ex", "mean"), med_ex=("ex", "median"))
        dr = d.dropna(subset=["rawW"])
        rr = stats.linregress(dr.rawW, dr.ex)
        out[f"rawW_slope_h{h}"] = pd.Series([len(dr), rr.slope, rr.slope / rr.stderr], index=["n", "slope", "t"])
        r2 = stats.linregress(d.dropna(subset=["r20"]).r20, d.dropna(subset=["r20"]).ex)
        out[f"r20_slope_h{h}"] = pd.Series([r2.slope, r2.slope / r2.stderr], index=["slope", "t"])
    d = R[(R.h == 26) & R.reg]
    trim = d[(d.ex > d.ex.quantile(0.05)) & (d.ex < d.ex.quantile(0.95))]
    out["level_26"] = pd.Series({"mean": d.ex.mean(), "median": d.ex.median(), "pos_share": (d.ex > 0).mean(),
        "trim_mean": trim.ex.mean(), "trim_t": trim.ex.mean() / (trim.ex.std() / np.sqrt(len(trim))),
        "max_ex": d.ex.max(), "n": len(d)})
    return out
