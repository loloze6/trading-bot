import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            v = df["volume"].values.astype(float)
            h = df["high"].values.astype(float); l = df["low"].values.astype(float)
            n = len(df)
            rng = (h - l) / c
            rng_s = pd.Series(rng)
            r28 = pd.Series(c) / pd.Series(c).shift(28) - 1
            vs = pd.Series(v)
            vr = vs.rolling(28).mean() / vs.shift(28).rolling(90, min_periods=30).mean()
            rr = rng_s.rolling(28).mean() / rng_s.shift(28).rolling(90, min_periods=30).mean()
            fc = df["forecast"].values.astype(float)
            for H in [1, 3, 5, 10, 20]:
                for t in range(0, n - H, H):
                    rows.append(dict(coin=coin, w=w, H=H, t=t, fc=fc[t],
                                     ret=c[t+H]/c[t]-1, r28=r28.iloc[t], vr=vr.iloc[t], rr=rr.iloc[t],
                                     day=str(df["timestamp"].iloc[t])[:10],
                                     year=str(df["timestamp"].iloc[t])[:4]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "H"])["ret"].transform("mean")
    d["un_s"] = -(d["ret"] - d["drift"])
    def tday(x):
        s = x.groupby("day")["un_s"].sum()
        return pd.Series(dict(n=len(x), days=len(s), mean=x["un_s"].mean(),
                              t=s.mean()/(s.std(ddof=1)/np.sqrt(len(s))) if len(s) > 2 else np.nan))
    out = {}
    cs = d[d.fc < 0]
    out["by_horizon_cases"] = cs.groupby("H").apply(tday)
    c5 = cs[cs.H == 5].copy()
    out["by_coin_H5"] = c5.groupby("coin").apply(tday)
    out["by_window_H5"] = c5.groupby("w").apply(tday)
    c5["q"] = pd.qcut(c5["fc"].rank(method="first"), 4, labels=["deepest", "q2", "q3", "shallow"])
    out["by_fc_quartile_H5"] = c5.groupby("q").apply(tday)
    c5["rq"] = pd.qcut(c5["rr"].rank(method="first"), 3, labels=["calm_range", "mid", "wide_range"])
    out["by_range_ratio_H5"] = c5.groupby("rq").apply(tday)
    # all bars with 28d fall, split by vol regime
    a5 = d[(d.H == 5) & (d.r28 < 0)].copy()
    a5["vreg"] = np.where(a5.vr < 1, "lowvol", "highvol")
    a5["fq"] = pd.qcut(a5["r28"].rank(method="first"), 3, labels=["deep", "mid", "small"])
    out["fall28_by_volreg_depth_H5"] = a5.groupby(["vreg", "fq"]).apply(tday)
    a10 = d[(d.H == 10) & (d.r28 < 0)].copy()
    a10["vreg"] = np.where(a10.vr < 1, "lowvol", "highvol")
    out["fall28_by_volreg_H10"] = a10.groupby("vreg").apply(tday)
    return out
