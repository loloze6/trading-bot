import numpy as np, pandas as pd

def explore(data):
    H = [1, 3, 5, 10]
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std().shift(1)
            vsr = r / sd
            vsr_inc = r / r.rolling(30, min_periods=20).std()
            reg = df["regime"].astype(str)
            n = len(df)
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, day=str(df["timestamp"].iloc[i])[:10],
                                     vsr=vsr_inc.iloc[i], reg=reg.iloc[i],
                                     inprof=reg.iloc[i] != "chop",
                                     fwd=c.iloc[i + h] / c.iloc[i] - 1,
                                     year=str(df["timestamp"].iloc[i])[:4]))
    d = pd.DataFrame(rows).dropna(subset=["vsr", "fwd"])
    drift = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - drift

    def ct(x, g):
        x = np.asarray(x); m = x.mean(); n = len(x)
        s = pd.Series(x - m).groupby(np.asarray(g)).sum()
        G = len(s)
        if G < 3: return np.nan
        se = np.sqrt(G / (G - 1) * (s ** 2).sum()) / n
        return m / se

    def summ(sub):
        return pd.Series(dict(n=len(sub), mean_ex=sub["ex"].mean(), t=ct(sub["ex"], sub["day"]),
                              mean_fwd=sub["fwd"].mean()))

    bins = [-np.inf, -2, -1, 0, 1, 2, np.inf]
    d["bucket"] = pd.cut(d["vsr"], bins).astype(str)
    out = {}
    out["regime_share"] = d[d.h == 1]["reg"].value_counts(normalize=True)
    out["h5_by_prof_bucket"] = d[d.h == 5].groupby(["inprof", "bucket"]).apply(summ)
    out["all_h_prof_big_up"] = d[(d.vsr >= 1)].groupby(["h", "inprof"]).apply(summ)
    out["all_h_prof_big_down"] = d[(d.vsr <= -1)].groupby(["h", "inprof"]).apply(summ)
    s5 = d[(d.h == 5) & (d.vsr >= 1) & d.inprof]
    out["h5_inprof_up_by_coin"] = s5.groupby("coin").apply(summ)
    out["h5_inprof_up_by_year"] = s5.groupby("year").apply(summ)
    a5 = d[(d.h == 5) & (d.vsr >= 1)]
    out["h5_allprof_up_by_year"] = a5.groupby("year").apply(summ)
    # signed continuation: ex * sign(vsr) for |vsr|>=1, by profile and horizon
    b = d[d.vsr.abs() >= 1].copy()
    b["ex"] = b["ex"] * np.sign(b["vsr"])
    out["signed_cont"] = b.groupby(["h", "inprof"]).apply(summ)
    return out
