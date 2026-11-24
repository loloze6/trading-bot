def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            n = len(c)
            ret1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            # streaks (counted inside window)
            dn = np.zeros(n); up = np.zeros(n)
            for i in range(1, n):
                if ret1[i] < 0: dn[i] = dn[i-1] + 1
                if ret1[i] > 0: up[i] = up[i-1] + 1
            r30 = np.r_[[np.nan]*30, c[30:] / c[:-30] - 1] if n > 30 else np.full(n, np.nan)
            for h in (1, 3, 5, 10):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, ts=b["timestamp"].iloc[i],
                                     year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                     fwd=c[i+h] / c[i] - 1, dn=dn[i], up=up[i],
                                     fc=b["forecast"].iloc[i], r30=r30[i],
                                     ret1=ret1[i]))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby(["coin", "h"])["fwd"].transform("mean")
    df["usd"] = df.groupby(["coin", "h"])["fwd"].transform("std")
    df["ex_short"] = -(df["fwd"] - df["drift"])
    df["day"] = pd.to_datetime(df["ts"]).dt.floor("D")

    def stat(g, col="ex_short"):
        s = g.groupby("day")[col].sum()
        m = g[col].mean()
        se = s.std(ddof=1) * np.sqrt(len(s)) / len(g) if len(s) > 1 else np.nan
        return pd.Series(dict(n=len(g), days=len(s), mean=m, t=m / se if se else np.nan,
                              strength=(g[col] / g["usd"]).mean()))

    out = {}
    d = df[df.dn >= 1].copy()
    d["len"] = d.dn.clip(upper=5)
    out["short ex by horizon x downstreak len"] = d.groupby(["h", "len"]).apply(stat).round(4)
    d5 = d[d.h == 5]
    out["h5 by coin"] = d5.groupby("coin").apply(stat).round(4)
    out["h5 by year"] = d5.groupby("year").apply(stat).round(4)
    d5 = d5.assign(trend=np.where(d5.r30 > 0, "30d up", np.where(d5.r30 <= 0, "30d down", "na")))
    out["h5 by 30d trend x len"] = d5.groupby(["trend", d5.dn.clip(upper=3)]).apply(stat).round(4)
    u = df[(df.up >= 1)].copy()
    u["len"] = u.up.clip(upper=5)
    u["ex_long"] = -u["ex_short"]
    out["long ex after UP streaks by h x len"] = u.groupby(["h", "len"]).apply(lambda g: stat(g, "ex_long")).round(4)
    return out
