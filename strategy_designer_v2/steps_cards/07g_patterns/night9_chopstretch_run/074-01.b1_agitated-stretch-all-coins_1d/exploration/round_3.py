import pandas as pd, numpy as np
from scipy import stats

def _cl(x, day):
    d = pd.DataFrame(dict(x=x, day=day)).dropna()
    n = len(d)
    if n < 3:
        return pd.Series(dict(n=n, days=d.day.nunique() if n else 0, mean=np.nan, t=np.nan))
    m = d.x.mean()
    s = (d.x - m).groupby(d.day).sum()
    se = np.sqrt((s ** 2).sum()) / n
    return pd.Series(dict(n=n, days=d.day.nunique(), mean=m, t=m / se if se > 0 else np.nan))

def _tab(df, keys, col):
    res = {}
    for k, g in df.groupby(keys, observed=True):
        res[k] = _cl(g[col].values, g["day"].values)
    return pd.DataFrame(res).T

def explore(data):
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sma = c.rolling(20).mean()
            sd = r.rolling(20).std()
            stretch = (c / sma - 1) / sd
            ret60 = c / c.shift(60) - 1
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            agit = np.where(b["regime"].astype(str) == "chop", "calm", "agit")
            fc = b["forecast"].astype(float).values
            for h in (3, 5, 10):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, n, h)
                rows.append(pd.DataFrame(dict(coin=coin, w=w, h=h, stretch=stretch.values[idx], fwd=fwd.values[idx],
                                              agit=agit[idx], ret60=ret60.values[idx], fc=fc[idx],
                                              year=ts.dt.year.values[idx], day=ts.dt.normalize().values[idx])))
            daily.append(pd.DataFrame(dict(coin=coin, w=w, nxt=r.shift(-1).values, agit=agit,
                                           wd=ts.dt.weekday.values, ret60=ret60.values,
                                           year=ts.dt.year.values, day=ts.dt.normalize().values)))
    df = pd.concat(rows, ignore_index=True).dropna(subset=["fwd", "stretch"])
    dd = pd.concat(daily, ignore_index=True).dropna(subset=["nxt"])
    out = {}
    drift = df.groupby("h")["fwd"].mean()
    df["ex"] = df["fwd"] - df["h"].map(drift)
    df["trend"] = pd.cut(df["ret60"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"]).astype(str)
    # 1. forecast quartiles (standardised depth) on the grid, day-clustered
    s = df[(df.h == 10) & (df.fc > 0)].copy()
    s["fq"] = pd.qcut(s["fc"].rank(method="first"), 4, labels=False)
    out["h10_fc_quartile"] = _tab(s, ["fq"], "ex")
    out["h10_fc_quartile_x_trend"] = _tab(s, ["trend", "fq"], "ex")
    s5 = df[(df.h == 5) & (df.fc > 0)].copy()
    s5["fq"] = pd.qcut(s5["fc"].rank(method="first"), 4, labels=False)
    out["h5_fc_quartile"] = _tab(s5, ["fq"], "ex")
    # 2. choppy agitated, below the average: continuation down, graded?
    ca = df[(df.trend == "chop") & (df.agit == "agit")].copy()
    ca["sbin"] = pd.cut(ca["stretch"], [-99, -1.5, 0, 1.5, 99]).astype(str)
    out["chop_agit_by_h_sbin"] = _tab(ca, ["h", "sbin"], "ex")
    cab = ca[(ca.stretch < 0) & (ca.h == 3)]
    out["chop_agit_below_h3_by_year"] = _tab(cab, ["year"], "ex")
    out["chop_agit_below_h3_by_coin"] = _tab(cab, ["coin"], "ex")
    sp = {}
    for h in (3, 5, 10):
        g = ca[ca.h == h]
        rr = stats.spearmanr(g["stretch"], g["ex"])
        sp[h] = dict(rho=rr[0], p=rr[1], n=len(g))
    out["chop_agit_spearman"] = pd.DataFrame(sp).T
    # 3. weekday next-day return, by profile, day-clustered
    dd["trend"] = pd.cut(dd["ret60"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"]).astype(str)
    dd["late"] = dd["wd"].isin([3, 4])
    dd["exn"] = dd["nxt"] - dd["nxt"].mean()
    out["late_week_by_trend_agit"] = _tab(dd, ["trend", "agit", "late"], "exn")
    out["late_week_by_year"] = _tab(dd, ["year", "late"], "exn")
    return out
