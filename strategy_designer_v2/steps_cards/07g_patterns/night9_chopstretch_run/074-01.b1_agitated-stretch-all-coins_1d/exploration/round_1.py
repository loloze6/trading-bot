import pandas as pd, numpy as np
from scipy import stats

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
            rng = (b["high"] - b["low"]) / c
            n = len(b)
            ts = pd.to_datetime(b["timestamp"])
            for h in (3, 10):
                fwd = c.shift(-h) / c - 1
                for i in range(0, n, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, stretch=stretch[i], fwd=fwd[i],
                                     reg=b["regime"].iloc[i], ret60=ret60[i], r1=r[i],
                                     day=ts[i].normalize(), wd=ts[i].weekday(), year=ts[i].year,
                                     fc=b["forecast"].iloc[i], rng=rng[i]))
            nxt = r.shift(-1)
            daily.append(pd.DataFrame(dict(coin=coin, w=w, r=r, nxt=nxt, reg=b["regime"], wd=ts.dt.weekday,
                                           stretch=stretch, ret60=ret60, rng=rng)))
    df = pd.DataFrame(rows).dropna(subset=["fwd", "stretch"])
    dd = pd.DataFrame(daily).dropna(subset=["r", "nxt"])
    out = {}
    drift = df.groupby("h")["fwd"].mean()
    out["drift_by_h"] = drift
    df["ex"] = df["fwd"] - df["h"].map(drift)
    df["sbin"] = pd.cut(df["stretch"], [-99, -2, -1, 0, 1, 2, 99])
    df["agit"] = np.where(df["reg"] == "chop", "calm", "agit")
    def agg(g):
        x = g["ex"]
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    for h in (3, 10):
        s = df[df.h == h]
        out[f"h{h}_stretchbin_x_agit"] = s.groupby(["agit", "sbin"]).apply(agg)
        s2 = s.dropna(subset=["ret60"]).copy()
        s2["trend"] = pd.cut(s2["ret60"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"])
        out[f"h{h}_trend_x_agit_x_sign"] = s2.groupby(["trend", "agit", s2["stretch"] < 0]).apply(agg)
    s = df[df.h == 10]
    out["h10_corr_stretch_ex_by_agit"] = s.groupby("agit").apply(lambda g: pd.Series(dict(
        rho=stats.spearmanr(g["stretch"], g["ex"])[0], n=len(g))))
    out["h10_by_year_agit_below"] = s[(s.agit == "agit") & (s.stretch < 0)].groupby("year").apply(agg)
    # daily: next-day return after large moves, by regime
    dd["rq"] = pd.qcut(dd["r"], 5, labels=False)
    dd["agit"] = np.where(dd["reg"] == "chop", "calm", "agit")
    out["nextday_by_r_quintile_agit"] = dd.groupby(["agit", "rq"])["nxt"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    out["nextday_by_weekday"] = dd.groupby("wd")["nxt"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    dd["rngq"] = dd.groupby("coin")["rng"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["nextday_by_range_quintile"] = dd.groupby("rngq")["nxt"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    # book
    days = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            days.append(d.assign(coin=coin, w=w))
    D = pd.concat(days).dropna(subset=["book_return"])
    out["book_mean_by_coin"] = D.groupby("coin")["book_return"].agg(["count", "mean"])
    out["book_mean_by_window"] = D.groupby("w")["book_return"].agg(["count", "mean"])
    return out
