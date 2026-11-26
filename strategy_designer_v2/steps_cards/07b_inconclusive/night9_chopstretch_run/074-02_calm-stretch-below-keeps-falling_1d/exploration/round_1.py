def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r = c.pct_change()
            sma = c.rolling(20).mean()
            sd = r.rolling(20).std()
            stretch = (c - sma) / sma / sd
            tr60 = c / c.shift(60) - 1
            for h in [3, 5, 10, 20]:
                for i in range(0, len(df) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i,
                        yr=pd.Timestamp(df["timestamp"].iloc[i]).year,
                        fc=df["forecast"].iloc[i], reg=df["regime"].iloc[i],
                        st=stretch.iloc[i], tr=tr60.iloc[i],
                        ret=c.iloc[i + h] / c.iloc[i] - 1))
    g = pd.DataFrame(rows)
    g["drift"] = g.groupby(["coin", "h"])["ret"].transform("mean")
    g["ex"] = g["ret"] - g["drift"]
    g["calm"] = g["reg"] == "unknown"
    def reg(s, x="st"):
        s = s.dropna(subset=[x, "ex"])
        if len(s) < 8: return pd.Series(dict(n=len(s)))
        lr = stats.linregress(s[x], s["ex"])
        return pd.Series(dict(n=len(s), slope=lr.slope, t=lr.slope / lr.stderr, mean_ex=s["ex"].mean(), t_mean=stats.ttest_1samp(s["ex"], 0).statistic))
    out = {}
    # slope of ex on stretch (positive slope = deeper below -> lower return? stretch negative below; positive slope => deeper below lower return => keeps falling)
    sub = g[(g.st < 0)]
    out["by_h_calm"] = sub[sub.calm].groupby("h").apply(reg)
    out["by_h_agit"] = sub[~sub.calm].groupby("h").apply(reg)
    out["by_h_fc_neg"] = g[(g.fc < 0)].groupby("h").apply(lambda s: reg(s, "fc"))
    s10 = sub[(sub.h == 10) & sub.calm]
    out["calm10_by_coin"] = s10.groupby("coin").apply(reg)
    out["calm10_by_year"] = s10.groupby("yr").apply(reg)
    s10 = s10.copy()
    s10["trend"] = np.where(s10.tr > 0.1, "rising", np.where(s10.tr < -0.1, "falling", np.where(s10.tr.isna(), "na", "choppy")))
    out["calm10_by_trend"] = s10.groupby("trend").apply(reg)
    s10["q"] = pd.qcut(s10.st, 4, labels=False)
    out["calm10_by_depth_q"] = s10.groupby("q").agg(n=("ex", "size"), st=("st", "mean"), ex=("ex", "mean"), ret=("ret", "mean"))
    a10 = sub[(sub.h == 10) & ~sub.calm].copy()
    a10["q"] = pd.qcut(a10.st, 4, labels=False)
    out["agit10_by_depth_q"] = a10.groupby("q").agg(n=("ex", "size"), st=("st", "mean"), ex=("ex", "mean"), ret=("ret", "mean"))
    return out
