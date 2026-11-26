import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    H = [1, 3, 5, 10]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            n = len(c)
            ret1 = c.pct_change()
            up = (ret1 > 0).astype(int).values
            dn = (ret1 < 0).astype(int).values
            us = np.zeros(n, int); ds = np.zeros(n, int)
            for i in range(1, n):
                us[i] = us[i-1] + 1 if up[i] else 0
                ds[i] = ds[i-1] + 1 if dn[i] else 0
            tr60 = c / c.shift(60) - 1
            vol30 = ret1.rolling(30).std()
            agit = vol30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            fc = b["forecast"].astype(float).reset_index(drop=True)
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, us=us[i], ds=ds[i],
                                     r=c[i+h]/c[i]-1, fc=fc[i],
                                     tr=tr60[i], ag=agit[i],
                                     year=pd.Timestamp(b["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["r"].transform("mean")
    d["sd"] = d.groupby(["coin", "h"])["r"].transform("std")
    d["u"] = (d["r"] - d["drift"]) / d["sd"]  # strength, long direction
    d["usb"] = d["us"].clip(upper=5)
    d["dsb"] = d["ds"].clip(upper=5)
    out = {}
    def summ(g):
        return pd.Series(dict(n=len(g), mean_str=g["u"].mean(), mean_ret=g["r"].mean(),
                              t=g["u"].mean() / (g["u"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan))
    out["up streak x horizon (long-dir strength)"] = d.groupby(["h", "usb"]).apply(summ).unstack(0)["mean_str"]
    out["up streak x horizon t"] = d.groupby(["h", "usb"]).apply(summ).unstack(0)["t"]
    out["down streak x horizon strength"] = d.groupby(["h", "dsb"]).apply(summ).unstack(0)["mean_str"]
    out["down streak x horizon t"] = d.groupby(["h", "dsb"]).apply(summ).unstack(0)["t"]
    d5 = d[d.h == 5].copy()
    upd = d5[d5.us > 0]
    out["h5 up-day by coin"] = upd.groupby("coin").apply(summ)
    out["h5 up-day by year"] = upd.groupby("year").apply(summ)
    upd = upd.assign(trend=np.where(upd.tr > .1, "rising", np.where(upd.tr < -.1, "falling", "choppy")),
                     agi=np.where(upd.ag > .5, "agit", "calm"))
    out["h5 up-day by profile"] = upd.dropna(subset=["tr", "ag"]).groupby(["trend", "agi"]).apply(summ)
    upd["fq"] = pd.qcut(upd["fc"].abs().rank(method="first"), 3, labels=["low", "mid", "high"])
    out["h5 up-day by |forecast| third"] = upd.groupby("fq").apply(summ)
    out["h5 up-day by streak, slope corr t"] = pd.Series(stats.spearmanr(upd["us"], upd["u"])[:2], index=["rho", "p"])
    return out
