def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 7, 14]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            raw = df.get("debug_info.components.month_fall.last_history_value")
            fc = df["forecast"].values
            reg = df["regime"].values
            for h in H:
                for i in range(0, n - h, h):
                    r = c[i + h] / c[i] - 1
                    rows.append(dict(coin=coin, w=w, h=h, i=i, ret=r,
                                     raw=(raw.iloc[i] if raw is not None else np.nan),
                                     fc=fc[i], chop=(reg[i] == "unknown"),
                                     year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                     ts=pd.Timestamp(df["timestamp"].iloc[i]).normalize()))
    R = pd.DataFrame(rows)
    drift = R.groupby(["coin", "h"])["ret"].mean().rename("drift")
    usual = R.groupby(["coin", "h"])["ret"].std().rename("usual")
    R = R.join(drift, on=["coin", "h"]).join(usual, on=["coin", "h"])
    R["unus"] = R["ret"] - R["drift"]

    def summ(g, sign):
        x = sign * g["unus"]
        d = (sign * g["unus"]).groupby(g["ts"]).sum()
        m = x.mean()
        u = (sign * g["unus"] - m).groupby(g["ts"]).sum()
        G = len(u)
        se = np.sqrt(G / (G - 1) * (u ** 2).sum()) / len(x) if G > 1 else np.nan
        return pd.Series(dict(n=len(x), days=G, mean=m, t=m / se if se else np.nan,
                              total=(sign * g["ret"]).mean(),
                              strength=(x / g["usual"]).mean()))

    C = R[R["chop"] & R["raw"].notna()].copy()
    out = {}
    hor = []
    for h in H:
        g = C[(C.h == h) & (C.raw < 0)]
        s = summ(g, -1); s["h"] = h; s["side"] = "short(fall)"; hor.append(s)
        g = C[(C.h == h) & (C.raw > 0)]
        s = summ(g, 1); s["h"] = h; s["side"] = "long(rise)"; hor.append(s)
    out["by horizon and side (chop)"] = pd.DataFrame(hor)
    g7 = C[(C.h == 7)].copy()
    g7["q"] = pd.qcut(g7["raw"], 6)
    out["7d continuation by 30d return sextile"] = g7.groupby("q").apply(
        lambda g: summ(g, np.sign(g["raw"].mean())))
    f7 = g7[g7.raw < 0]
    out["7d fall cases by coin"] = f7.groupby("coin").apply(lambda g: summ(g, -1))
    out["7d fall cases by window"] = f7.groupby("w").apply(lambda g: summ(g, -1))
    out["7d fall cases by year"] = f7.groupby("year").apply(lambda g: summ(g, -1))
    # slope of 7d unusual return on raw 30d return within chop
    sl = stats.linregress(g7["raw"], g7["unus"])
    out["slope 7d unusual on 30d ret (chop, all)"] = pd.Series(dict(slope=sl.slope, t=sl.slope / sl.stderr, n=len(g7)))
    sl = stats.linregress(f7["raw"], f7["unus"])
    out["slope 7d unusual on 30d ret (chop, falls)"] = pd.Series(dict(slope=sl.slope, t=sl.slope / sl.stderr, n=len(f7)))
    out["drift 7d mean over coins"] = R[R.h == 7].groupby("coin")["drift"].first()
    return out
