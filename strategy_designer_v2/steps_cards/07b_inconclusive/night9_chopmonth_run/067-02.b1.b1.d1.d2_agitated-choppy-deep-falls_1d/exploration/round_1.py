def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r30 = c / c.shift(30) - 1
            for h in (5, 10, 21, 42):
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(df) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i,
                                     day=str(df["timestamp"].iloc[i])[:10],
                                     inprof=(df["regime"].iloc[i] == "unknown"),
                                     fc=df["forecast"].iloc[i], r30=r30.iloc[i], fwd=fwd.iloc[i]))
    d = pd.DataFrame(rows).dropna(subset=["fwd"])
    drift = d.groupby(["coin", "h"])["fwd"].mean().rename("drift")
    d = d.join(drift, on=["coin", "h"])
    d["ex"] = d["fwd"] - d["drift"]
    out = {}

    def summ(g, sign=-1):
        x = sign * g["ex"]
        dd = (x - x.mean()).groupby(g["day"]).sum()
        K = len(dd)
        se = np.sqrt((dd ** 2).sum() * K / max(K - 1, 1)) / len(x) if len(x) > 1 else np.nan
        return pd.Series(dict(n=len(x), days=K, mean=x.mean(), t=x.mean() / se if se else np.nan,
                              total=(sign * g["fwd"]).mean()))

    p = d[d.inprof & d.r30.notna()].copy()
    p["side"] = np.where(p.r30 < 0, "fall", "rise")
    p["bin"] = pd.cut(p.r30, [-1, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 5])
    out["profile_by_h_side_shortdir"] = p.groupby(["h", "side"]).apply(summ)
    out["profile_h21_by_r30bin_shortdir"] = p[p.h == 21].groupby("bin").apply(summ)
    f = p[(p.side == "fall")]
    f = f.assign(deep=np.where(f.fc <= -10, "deep", np.where(f.fc < 0, "shallow", "zero")))
    out["fall_by_h_deep"] = f.groupby(["h", "deep"]).apply(summ)
    out["fall_h21_by_coin"] = f[f.h == 21].groupby("coin").apply(summ)
    f21 = f[f.h == 21].copy()
    f21["year"] = f21.day.str[:4]
    out["fall_h21_by_year"] = f21.groupby("year").apply(summ)
    out["fall_h21_by_window"] = f21.groupby("w").apply(summ)
    # outside profile, falls, for comparison
    o = d[(~d.inprof) & (d.r30 < 0)]
    out["outside_profile_falls_by_h"] = o.groupby("h").apply(summ)
    # correlation of r30 with fwd in profile, h=21
    q = p[p.h == 21]
    out["corr_r30_fwd_profile_h21"] = float(q[["r30", "ex"]].corr().iloc[0, 1])
    return out
