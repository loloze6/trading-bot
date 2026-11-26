def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            hi = df["high"].astype(float).rolling(20, min_periods=20).max()
            lo = df["low"].astype(float).rolling(20, min_periods=20).min()
            pos = 2 * (c - lo) / (hi - lo) - 1
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            sdw = r1.expanding(min_periods=40).median()
            ret60 = c / c.shift(60) - 1
            ret20 = c / c.shift(20) - 1
            for h in (5, 10):
                fr = c.shift(-h) / c - 1
                for i in np.arange(0, len(df), h):
                    if pd.isna(fr.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, win=w, h=h, fr=fr.iloc[i], fc=df["forecast"].iloc[i],
                                     reg=df["regime"].iloc[i], pos=pos.iloc[i], sd30=sd30.iloc[i],
                                     ret60=ret60.iloc[i], ret20=ret20.iloc[i],
                                     day=str(df["timestamp"].iloc[i])[:10], year=str(df["timestamp"].iloc[i])[:4]))
    R = pd.DataFrame(rows)
    R["ex"] = R["fr"] - R.groupby(["coin", "h"])["fr"].transform("mean")
    R["sdcoin"] = R.groupby(["coin", "h"])["fr"].transform("std")
    R["exs"] = R["ex"] / R["sdcoin"]
    R["exw"] = R.groupby("h")["ex"].transform(lambda s: s.clip(s.quantile(.01), s.quantile(.99)))
    R["mkt"] = R.groupby(["h", "day"])["fr"].transform("mean")
    R["exm"] = R["fr"] - R["mkt"]
    R["sd30med"] = R.groupby(["coin"])["sd30"].transform("median")
    R["agit"] = np.where(R.sd30 > R.sd30med, "agitated", "calm")
    R["trend"] = np.where(R.ret60 > .1, "rising", np.where(R.ret60 < -.1, "falling", "choppy"))
    out = {}

    def st(d, x, y):
        d = d.dropna(subset=[x, y])
        if len(d) < 20:
            return dict(n=len(d), slope=np.nan, t=np.nan)
        X = d[x].values; Y = d[y].values
        Xc = X - X.mean(); b = (Xc * (Y - Y.mean())).sum() / (Xc ** 2).sum()
        e = Y - Y.mean() - b * Xc
        g = pd.Series(Xc * e).groupby(d["day"].values).sum()
        se = np.sqrt((g ** 2).sum()) / (Xc ** 2).sum()
        return dict(n=len(d), slope=b, t=b / se, days=d.day.nunique())

    act = R[(R.fc != 0) & (R.reg == "unknown")]
    L = []
    for h in (5, 10):
        d = act[act.h == h]
        for y in ("ex", "exw", "exs", "exm"):
            L.append(dict(h=h, y=y, **st(d, "pos", y)))
    out["robust_choppy"] = pd.DataFrame(L)
    d5 = act[act.h == 5]
    out["choppy_mean_ex_h5"] = pd.Series(dict(mean_ex=d5.ex.mean(), median_ex=d5.ex.median(), n=len(d5)))
    q = pd.qcut(d5.pos, 5, labels=False)
    out["quint_choppy_h5_robust"] = d5.groupby(q).agg(n=("ex", "size"), median_ex=("ex", "median"),
                                                     exw=("exw", "mean"), exm=("exm", "mean"), max_ex=("ex", "max"))
    L = []
    for (tr, ag), d in R[R.h == 5].groupby(["trend", "agit"]):
        L.append(dict(trend=tr, agit=ag, **{k + "_w": v for k, v in st(d, "pos", "exw").items()},
                      t_mkt=st(d, "pos", "exm")["t"]))
    out["trend_x_agit_h5_pos"] = pd.DataFrame(L)
    L = []
    for (tr, ag), d in R[R.h == 10].groupby(["trend", "agit"]):
        L.append(dict(trend=tr, agit=ag, **st(d, "pos", "exw")))
    out["trend_x_agit_h10_pos"] = pd.DataFrame(L)
    L = []
    for (tr, yr), d in R[R.h == 5].groupby(["trend", "year"]):
        L.append(dict(trend=tr, year=yr, **st(d, "pos", "exw")))
    out["trend_by_year_h5"] = pd.DataFrame(L)
    return out
