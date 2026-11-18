import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    rows = []
    H = [1, 3, 5, 10]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float); v = df["volume"].values.astype(float)
            n = len(df)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vm = pd.Series(v).shift(1).rolling(30, min_periods=30).mean().values
            vr = v / vm
            sd = pd.Series(r1).shift(1).rolling(60, min_periods=20).std().values
            yr = pd.to_datetime(df["timestamp"].iloc[0]).year
            for h in H:
                for t in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, yr=yr, h=h, fwd=c[t + h] / c[t] - 1,
                                     r1=r1[t], vr=vr[t], z=r1[t] / sd[t] if sd[t] > 0 else np.nan))
    d = pd.DataFrame(rows)
    d["mu"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["mu"]
    d = d.dropna(subset=["vr", "z", "ex"])

    def tt(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))

    out = {}
    # big up days (z>1), graded by log volume ratio x z
    up = d[d.z > 1].copy()
    up["lv"] = np.log(up.vr)
    up["vq"] = pd.qcut(up.lv.rank(method="first"), 4, labels=False)
    out["bigup_by_volq_h"] = up.groupby(["h", "vq"])["ex"].apply(tt).unstack()
    up["sig"] = up.z * up.lv
    out["bigup_corr_sig_ex"] = up.groupby("h").apply(lambda g: pd.Series(dict(n=len(g), spearman=g[["sig", "ex"]].corr("spearman").iloc[0, 1], pearson_lv=g[["lv", "ex"]].corr().iloc[0, 1])))
    u5 = up[(up.h == 5) & (up.vr > 1)]
    out["bigup_heavy_h5_by_year"] = u5.groupby("yr")["ex"].apply(tt).unstack()
    out["bigup_heavy_h5_by_coin"] = u5.groupby("coin")["ex"].apply(tt).unstack()
    # big down days (z<-1), graded by volume
    dn = d[d.z < -1].copy()
    dn["lv"] = np.log(dn.vr)
    dn["vq"] = pd.qcut(dn.lv.rank(method="first"), 4, labels=False)
    out["bigdown_by_volq_h"] = dn.groupby(["h", "vq"])["ex"].apply(tt).unstack()
    d3 = dn[(dn.h == 3) & (dn.vr > 1)]
    out["bigdown_heavy_h3_by_year"] = d3.groupby("yr")["ex"].apply(tt).unstack()
    out["bigdown_heavy_h3_by_coin"] = d3.groupby("coin")["ex"].apply(tt).unstack()
    dn["sig"] = -dn.z * dn.lv
    out["bigdown_corr"] = dn.groupby("h").apply(lambda g: pd.Series(dict(n=len(g), spearman_sig_ex=g[["sig", "ex"]].corr("spearman").iloc[0, 1])))
    return out
