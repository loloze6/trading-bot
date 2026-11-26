def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            inprof = (df["regime"] == "unknown").values
            for h in (3, 7, 14):
                for i in range(0, n, h):
                    if i + h >= n or i - 7 < 0:
                        continue
                    rows.append(dict(coin=coin, win=w, h=h, day=ts[i].normalize(), year=ts[i].year,
                                     past=c[i]/c[i-7]-1, fwd=c[i+h]/c[i]-1, inprof=bool(inprof[i]),
                                     fc=df["forecast"].iloc[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["drift"]
    d["side"] = np.where(d["past"] < 0, "fall", "rise")

    def reg(g):
        if len(g) < 8:
            return pd.Series(dict(n=len(g)))
        r = stats.linregress(g["past"], g["ex"])
        # mean excess in reversal direction (long after fall, short after rise)
        rev = np.where(g["past"] < 0, g["ex"], -g["ex"])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope/r.stderr,
                              mean_ex=g["ex"].mean(), rev_mean=rev.mean(),
                              rev_t=rev.mean()/(rev.std(ddof=1)/np.sqrt(len(rev)))))
    out["by_h_prof_side"] = d.groupby(["h", "inprof", "side"]).apply(reg).round(4)
    out["by_h_prof_all"] = d.groupby(["h", "inprof"]).apply(reg).round(4)
    d7 = d[d.h == 7]
    out["h7_inprof_fall_by_coin"] = d7[d7.inprof & (d7.side == "fall")].groupby("coin").apply(reg).round(4)
    out["h7_inprof_fall_by_year"] = d7[d7.inprof & (d7.side == "fall")].groupby("year").apply(reg).round(4)
    out["h7_inprof_all_by_year"] = d7[d7.inprof].groupby("year").apply(reg).round(4)
    # quantile of past fall in profile
    f = d7[d7.inprof & (d7.side == "fall")].copy()
    f["q"] = pd.qcut(f["past"], 3, labels=["big", "mid", "small"])
    out["h7_inprof_fall_terciles"] = f.groupby("q").agg(n=("ex", "size"), past=("past", "mean"),
                                                         ex=("ex", "mean"), fwd=("fwd", "mean")).round(4)
    out["share_inprof"] = float(d7.inprof.mean())
    return out
