import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            n = len(c)
            r1 = c.pct_change()
            us = np.zeros(n, int); ds = np.zeros(n, int)
            for i in range(1, n):
                us[i] = us[i-1] + 1 if r1[i] > 0 else 0
                ds[i] = ds[i-1] + 1 if r1[i] < 0 else 0
            rank = b["debug_info.components.up_streak_rank.last_history_value"].astype(float).reset_index(drop=True)
            fc = b["forecast"].astype(float).reset_index(drop=True)
            tr = c / c.shift(60) - 1
            tr20 = c / c.shift(20) - 1
            v30 = r1.rolling(30).std()
            agit = v30.expanding(min_periods=40).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            for h in [5, 10]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, us=us[i], ds=ds[i], rank=rank[i], fc=fc[i],
                                     r=c[i+h]/c[i]-1, tr=tr[i], tr20=tr20[i], ag=agit[i],
                                     year=pd.Timestamp(b["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["r"].transform("mean")
    d["sd"] = d.groupby(["coin", "h"])["r"].transform("std")
    d["u"] = (d["r"] - d["drift"]) / d["sd"]
    def summ(g):
        return pd.Series(dict(n=len(g), mean_str=g["u"].mean(), mean_unus=(g["r"]-g["drift"]).mean(),
                              t=g["u"].mean()/(g["u"].std()/np.sqrt(len(g))) if len(g) > 2 else np.nan))
    out = {}
    upd = d[(d.us > 0)].copy()
    upd["rq"] = pd.cut(upd["rank"], [-0.01, 0.5, 0.8, 0.95, 1.01], labels=["<=.5", ".5-.8", ".8-.95", ">.95"])
    out["up-day by rank bin x h (long-dir)"] = upd.groupby(["h", "rq"]).apply(summ)
    u5 = upd[upd.h == 5].copy()
    u5["trend"] = np.where(u5.tr > .1, "rising", np.where(u5.tr < -.1, "falling", "choppy"))
    u5["agi"] = np.where(u5.ag > .5, "agit", "calm")
    out["h5 up-day by trend (60d)"] = u5.dropna(subset=["tr"]).groupby("trend").apply(summ)
    out["h5 up-day by agitation"] = u5.dropna(subset=["ag"]).groupby("agi").apply(summ)
    u5["hi"] = u5["rank"] > 0.8
    out["h5 up-day rank>.8 by trend"] = u5.dropna(subset=["tr"]).groupby(["hi", "trend"]).apply(summ)
    out["h5 up-day rank>.8 by year"] = u5.groupby(["hi", "year"]).apply(summ)
    out["h5 spearman rank vs long strength"] = pd.Series(stats.spearmanr(u5["rank"], u5["u"], nan_policy="omit")[:2], index=["rho", "p"])
    dn5 = d[(d.h == 5) & (d.ds > 0)].copy()
    dn5["dsb"] = dn5["ds"].clip(upper=4)
    out["h5 down streak bins (long-dir)"] = dn5.groupby("dsb").apply(summ)
    return out
