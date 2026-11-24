def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            up = np.zeros(n); dn = np.zeros(n)
            for i in range(1, n):
                if r1[i] > 0: up[i] = up[i-1] + 1
                if r1[i] < 0: dn[i] = dn[i-1] + 1
            ts = pd.to_datetime(b["timestamp"])
            vol30 = pd.Series(r1).rolling(30, min_periods=20).std().values
            ret3 = pd.Series(c).pct_change(3).values
            ret10 = pd.Series(c).pct_change(10).values
            ret60 = pd.Series(c).pct_change(60).values
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, win=w, day=ts.iloc[i].normalize(), wd=ts.iloc[i].dayofweek,
                                 fwd=c[i+H]/c[i]-1, r1=r1[i], up=up[i], dn=dn[i], vol30=vol30[i],
                                 ret3=ret3[i], ret10=ret10[i], ret60=ret60[i],
                                 pos=b["postRebalance_current_allocation"].iloc[i]))
    df = pd.DataFrame(rows)
    drift = df.groupby("coin")["fwd"].transform("mean")
    sd = df.groupby("coin")["fwd"].transform("std")
    df["unu"] = df["fwd"] - drift
    df["z"] = df["unu"] / sd
    df["streak"] = np.where(df.up > 0, df.up.clip(upper=5), -df.dn.clip(upper=5))
    def summ(g):
        x = g["z"].dropna()
        return pd.Series(dict(n=len(x), mean_unu=g["unu"].mean(), mean_z=x.mean(),
                              t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan))
    out = {}
    out["by signed streak (capped 5)"] = df.groupby("streak").apply(summ)
    df["r1z"] = df["r1"] / df["vol30"]
    df["r1z_q"] = pd.qcut(df["r1z"], 5, labels=False)
    out["by 1d move z quintile"] = df.groupby("r1z_q").apply(summ)
    df["r3_q"] = pd.qcut(df["ret3"], 5, labels=False)
    out["by 3d return quintile"] = df.groupby("r3_q").apply(summ)
    df["r10_q"] = pd.qcut(df["ret10"], 5, labels=False)
    out["by 10d return quintile"] = df.groupby("r10_q").apply(summ)
    df["trend"] = pd.cut(df["ret60"], [-np.inf, -0.1, 0.1, np.inf], labels=["fall", "chop", "rise"])
    df["vrank"] = df.groupby("coin")["vol30"].rank(pct=True)
    df["agit"] = np.where(df["vrank"] > 0.5, "agit", "calm")
    out["by trend x agit"] = df.dropna(subset=["trend"]).groupby(["trend", "agit"]).apply(summ)
    df["sgrp"] = np.sign(df["streak"])
    out["streak sign x trend"] = df.dropna(subset=["trend"]).groupby(["trend", "sgrp"]).apply(summ)
    out["weekday"] = df.groupby("wd").apply(summ)
    out["by coin streak>=3 up"] = df[df.up >= 3].groupby("coin").apply(summ)
    out["by coin streak>=3 down"] = df[df.dn >= 3].groupby("coin").apply(summ)
    # book daily
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dd.append(d)
    dd = pd.concat(dd)
    out["book by window mean daily ret"] = dd.groupby("win")[["book_return", "coin_return"]].mean()
    out["book by coin"] = dd.groupby("coin")[["book_return", "coin_return"]].mean()
    return out
