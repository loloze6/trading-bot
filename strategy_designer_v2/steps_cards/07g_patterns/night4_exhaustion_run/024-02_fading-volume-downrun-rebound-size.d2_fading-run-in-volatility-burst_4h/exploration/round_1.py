import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = 18
    rows = []
    bar1 = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            v = b["volume"].astype(float).values
            n = len(c)
            if n < H + 200:
                continue
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            s = pd.Series(r1)
            mabs = s.abs().rolling(180, min_periods=90).mean().values
            vol30 = s.rolling(30, min_periods=20).std()
            vr = (vol30 / vol30.rolling(180, min_periods=90).mean()).values
            r6 = pd.Series(c).pct_change(6).values
            r18 = pd.Series(c).pct_change(18).values
            sd6 = s.rolling(180, min_periods=90).std().values * np.sqrt(6)
            # signed streak
            streak = np.zeros(n)
            for i in range(1, n):
                d = np.sign(c[i] - c[i - 1])
                if d != 0 and np.sign(streak[i - 1]) == d:
                    streak[i] = streak[i - 1] + d
                else:
                    streak[i] = d
            # streak return and volume slope
            strret = np.full(n, np.nan); vslope = np.full(n, np.nan)
            for i in range(1, n):
                L = int(abs(streak[i]))
                if L >= 1 and i - L >= 0:
                    strret[i] = c[i] / c[i - L] - 1
                    if L >= 2:
                        vv = v[i - L + 1:i + 1]
                        x = np.arange(L)
                        vslope[i] = np.polyfit(x, vv, 1)[0] / (vv.mean() + 1e-12)
            ts = pd.to_datetime(b["timestamp"])
            fc = b["forecast"].astype(float).values
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, fwd=c[i + H] / c[i] - 1,
                                 streak=streak[i], strz=strret[i] / mabs[i] if mabs[i] > 0 else np.nan,
                                 vslope=vslope[i], vr=vr[i], z6=r6[i] / sd6[i], z18=r18[i] / (sd6[i] * np.sqrt(3)),
                                 fc=fc[i], hour=ts.iloc[i].hour, wd=ts.iloc[i].dayofweek))
            bar1.append(pd.DataFrame(dict(coin=coin, r=r1[1:], hour=ts.dt.hour.values[:-1],
                                          wd=ts.dt.dayofweek.values[:-1], vr=vr[:-1],
                                          z6p=np.r_[r6[:-1]] / sd6[:-1])))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    usual = g.groupby("coin")["fwd"].transform("std")
    g["str_"] = g["ex"] / usual

    def summ(df, key):
        o = df.groupby(key)["ex"].agg(["mean", "std", "count"])
        o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
        o["strength"] = df.groupby(key)["str_"].mean()
        return o.drop(columns="std").round(5)

    out = {}
    g["z18q"] = pd.qcut(g["z18"], 10, labels=False)
    out["fwd3d by past 3d return z decile"] = summ(g.dropna(subset=["z18"]), "z18q")
    g["z6q"] = pd.qcut(g["z6"], 10, labels=False)
    out["fwd3d by past 1d return z decile"] = summ(g.dropna(subset=["z6"]), "z6q")
    g["vrq"] = pd.qcut(g["vr"], 5, labels=False)
    out["fwd3d by vol ratio quintile"] = summ(g.dropna(subset=["vr"]), "vrq")
    g["stc"] = g["streak"].clip(-5, 5)
    out["fwd3d by signed streak"] = summ(g, "stc")
    d = g[(g["streak"].abs() >= 2) & g["vslope"].notna()].copy()
    d["cell"] = np.sign(d["streak"]).astype(int).astype(str) + "_vol" + np.where(d["vslope"] < 0, "fade", "rise")
    out["fwd3d streak>=2 by side and volume"] = summ(d, "cell")
    out["fwd3d by forecast bucket"] = summ(g.assign(fq=pd.cut(g["fc"], [-0.1, 0.01, 1, 2, 4, 21])), "fq")
    out["fwd3d by year-agnostic window"] = summ(g, "w")
    bb = pd.concat(bar1).dropna(subset=["r"])
    bb["ex"] = bb["r"] - bb.groupby("coin")["r"].transform("mean")
    bb["str_"] = bb["ex"] / bb.groupby("coin")["r"].transform("std")
    out["4h return by bar start hour"] = summ(bb, "hour")
    out["4h return by weekday"] = summ(bb, "wd")
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin, w=w))
    dd = pd.concat(dd).dropna(subset=["book_return", "coin_return"])
    bk = dd.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    out["book vs coin daily corr"] = float(bk["book_return"].corr(bk["coin_return"]))
    bk["q"] = pd.qcut(bk["book_return"].rank(method="first"), 10, labels=False)
    out["book decile: mean book, mean coin"] = bk.groupby("q")[["book_return", "coin_return"]].mean().round(5)
    out["book by window: mean, sharpe"] = bk.groupby("w")["book_return"].agg(lambda x: x.mean() / x.std() * np.sqrt(365)).round(2)
    return out
