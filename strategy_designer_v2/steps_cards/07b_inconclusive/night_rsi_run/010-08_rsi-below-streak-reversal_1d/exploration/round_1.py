import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    raw_col = "debug_info.components.below_age.last_history_value"
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in (7, 14, 28):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=yr[i],
                                     fc=df["forecast"].iloc[i],
                                     raw=df[raw_col].iloc[i] if raw_col in df else np.nan,
                                     ret=c[i + h] / c[i] - 1))
    g = pd.DataFrame(rows)
    g["ex"] = g["ret"] - g.groupby(["coin", "h"])["ret"].transform("mean")
    out = {}
    out["raw_describe"] = g[g.h == 14]["raw"].describe()

    def slope_t(d, x="fc"):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 10 or d[x].std() == 0:
            return (len(d), np.nan, np.nan)
        r = stats.linregress(d[x], d["ex"])
        return (len(d), r.slope, r.slope / r.stderr)

    res = []
    for h in (7, 14, 28):
        d = g[(g.h == h) & (g.fc > 0)]
        n, s, t = slope_t(d)
        res.append(dict(h=h, part="all_fc>0", n=n, slope=s, t=t, mean_ex=d.ex.mean()))
        for coin in d.coin.unique():
            n, s, t = slope_t(d[d.coin == coin])
            res.append(dict(h=h, part=coin, n=n, slope=s, t=t, mean_ex=d[d.coin == coin].ex.mean()))
        # all bars: below vs above
        dd = g[g.h == h]
        b = dd[dd.fc > 0].ex; a = dd[dd.fc <= 0].ex
        tt = stats.ttest_ind(b, a, equal_var=False)
        res.append(dict(h=h, part="fc>0 minus fc<=0", n=len(b), slope=b.mean() - a.mean(), t=tt.statistic, mean_ex=np.nan))
        # signed raw over all bars
        n, s, t = slope_t(dd, "raw")
        res.append(dict(h=h, part="raw_signed_all", n=n, slope=s, t=t, mean_ex=np.nan))
    out["slopes"] = pd.DataFrame(res)

    d14 = g[g.h == 14].copy()
    d14["absraw"] = d14["raw"]
    d14["bin"] = pd.cut(d14["raw"], [-61, -30, -15, -8, -4, -0.5, 0.5, 4, 8, 15, 30, 61])
    out["by_raw_bin_h14"] = d14.groupby("bin", observed=True)["ex"].agg(["count", "mean", "std"])
    dp = d14[d14.fc > 0].copy()
    dp["third"] = pd.qcut(dp.fc.rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["thirds_h14"] = dp.groupby("third", observed=True)["ex"].agg(["count", "mean", "std"])
    yrr = []
    for y, dy in dp.groupby("year"):
        n, s, t = slope_t(dy)
        yrr.append(dict(year=y, n=n, slope=s, t=t, mean_ex=dy.ex.mean()))
    out["by_year_h14"] = pd.DataFrame(yrr)
    return out
