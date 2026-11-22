import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    out = {}
    drift = {}
    for h in (1, 3, 5):
        for coin in bars:
            g = []
            for w, b in bars[coin].items():
                c = b["close"].values
                for i in range(0, len(c) - h, h):
                    g.append(c[i+h]/c[i]-1)
            drift[(coin, h)] = (np.mean(g), np.std(g))
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            sd = r1.rolling(20, min_periods=15).std()
            z = r1 / sd
            r20 = c / c.shift(20) - 1
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for h in (1, 3, 5):
                fwd = c.shift(-h) / c - 1
                m, s = drift[(coin, h)]
                for i in range(0, len(b) - h, h):
                    if np.isnan(z[i]) or np.isnan(fwd[i]):
                        continue
                    rows.append(dict(h=h, coin=coin, w=w, yr=yr[i], z=z[i], r20=r20[i],
                                     reg=b["regime"][i], un=fwd[i]-m, st=(fwd[i]-m)/s))
    df = pd.DataFrame(rows)
    def summ(gr):
        a = gr["st"]
        return pd.Series(dict(n=len(a), mean_st=a.mean(), mean_un=gr["un"].mean(),
                              t=a.mean()/(a.std()/np.sqrt(len(a))) if len(a) > 2 else np.nan))
    # 1. graded slope of fwd on today's z, by regime and horizon
    res = []
    for (h, reg), g in df.groupby(["h", "reg"]):
        x = g["z"].clip(-4, 4)
        lr = stats.linregress(x, g["st"])
        up = g[g["z"] > 0]
        lr2 = stats.linregress(up["z"].clip(0, 4), up["st"])
        res.append(dict(h=h, reg=reg, n=len(g), slope=lr.slope, t=lr.slope/lr.stderr,
                        n_up=len(up), slope_up=lr2.slope, t_up=lr2.slope/lr2.stderr))
    out["slope of fwd on z"] = pd.DataFrame(res)
    d5 = df[df["h"] == 5].copy()
    big = d5[d5["z"] > 1]
    a = big[big["reg"] == "unknown"]["st"]; b_ = big[big["reg"] == "mean_reversion"]["st"]
    out["z>1 rising minus falling (welch)"] = pd.Series(dict(n_rise=len(a), n_fall=len(b_), diff=a.mean()-b_.mean(),
                                                         t=stats.ttest_ind(a, b_, equal_var=False).statistic))
    out["z>1 rising regime by coin"] = big[big["reg"] == "unknown"].groupby("coin").apply(summ)
    out["z>1 rising regime by year"] = big[big["reg"] == "unknown"].groupby("yr").apply(summ)
    out["z>1 falling regime by coin"] = big[big["reg"] == "mean_reversion"].groupby("coin").apply(summ)
    # graded by 20d return among z>1
    big = big.copy()
    big["r20b"] = pd.qcut(big["r20"], 3)
    out["z>1 fwd5 by r20 tercile"] = big.groupby("r20b", observed=True).apply(summ)
    # weekday
    dd = []
    for coin in days:
        for w, d in days[coin].items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; dd.append(d)
    dd = pd.concat(dd).dropna(subset=["coin_return"])
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    dd["yr"] = pd.to_datetime(dd["day"]).dt.year
    def tt(s):
        return s.mean()/(s.std()/np.sqrt(len(s)))
    out["weekday t by coin"] = dd.pivot_table(index="wd", columns="coin", values="coin_return", aggfunc=tt)
    out["weekday mean by year"] = dd.pivot_table(index="wd", columns="yr", values="coin_return", aggfunc="mean")
    out["weekday std"] = dd.groupby("wd")["coin_return"].std()
    # day-of-week mean on coin-averaged days (independent across days)
    cm = dd.groupby(["w", "day", "wd"])["coin_return"].mean().reset_index()
    out["coin-avg ret by weekday"] = cm.groupby("wd")["coin_return"].agg(["count", "mean", tt])
    return out
