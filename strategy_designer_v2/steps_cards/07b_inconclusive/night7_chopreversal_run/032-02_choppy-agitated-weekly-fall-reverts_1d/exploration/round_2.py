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
            r1 = pd.Series(c).pct_change()
            vol30 = r1.rolling(30).std().values
            for h in (5, 7, 10):
                for i in range(0, n, h):
                    if i + h >= n or i - 7 < 0:
                        continue
                    rows.append(dict(coin=coin, win=w, h=h, day=ts[i].normalize(), year=ts[i].year,
                                     past=c[i]/c[i-7]-1, fwd=c[i+h]/c[i]-1, inprof=bool(inprof[i]),
                                     vol=vol30[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["drift"]
    d["usual"] = d.groupby(["coin", "h"])["fwd"].transform("std")
    d["side"] = np.where(d["past"] < 0, "fall", "rise")
    d["pz"] = d["past"] / (d["vol"] * np.sqrt(7))

    def clus_t(v, days):
        s = pd.Series(v).groupby(days.values).sum()
        k = pd.Series(v).groupby(days.values).size()
        m = v.mean()
        dev = (pd.Series(v) - m).groupby(days.values).sum()
        se = np.sqrt((dev**2).sum()) / len(v)
        return m / se if se > 0 else np.nan, len(s)

    def summ(g):
        rev = np.where(g["past"] < 0, g["ex"], -g["ex"]).astype(float)
        t, nd = clus_t(rev, g["day"].reset_index(drop=True))
        sl = stats.linregress(g["pz"], g["ex"]) if len(g) > 5 else None
        return pd.Series(dict(n=len(g), days=nd, rev_mean=rev.mean(), rev_t_day=t,
                              strength=(rev / g["usual"].values).mean(),
                              slope_pz_t=(sl.slope/sl.stderr) if sl is not None else np.nan))
    ip = d[d.inprof]
    out["inprof_by_h_side"] = ip.groupby(["h", "side"]).apply(summ).round(4)
    r7 = ip[(ip.h == 7) & (ip.side == "rise")].copy()
    out["rise7_by_coin"] = r7.groupby("coin").agg(n=("ex", "size"), ex=("ex", "mean")).round(4)
    out["rise7_by_year"] = r7.groupby("year").agg(n=("ex", "size"), ex=("ex", "mean")).round(4)
    r7["q"] = pd.qcut(r7["pz"], 2, labels=["smaller", "larger"])
    out["rise7_halves"] = r7.groupby("q").agg(n=("ex", "size"), pz=("pz", "mean"), ex=("ex", "mean")).round(4)
    f7 = ip[(ip.h == 7) & (ip.side == "fall")].copy()
    out["fall7_ex_without_2020"] = summ(f7[f7.year != 2020]).round(4)
    # out of profile mirror for comparison: rises over 7 days
    op = d[~d.inprof & (d.h == 7)]
    out["outprof_h7_side"] = op.groupby("side").apply(summ).round(4)
    return out
