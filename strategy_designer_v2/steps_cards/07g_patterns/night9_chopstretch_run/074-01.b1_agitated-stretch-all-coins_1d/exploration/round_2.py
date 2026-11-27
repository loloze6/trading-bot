import pandas as pd, numpy as np
from scipy import stats

def _agg(x):
    x = pd.Series(x).dropna()
    n = len(x)
    if n < 3:
        return pd.Series(dict(n=n, mean=np.nan, t=np.nan))
    return pd.Series(dict(n=n, mean=x.mean(), t=x.mean() / (x.std(ddof=1) / np.sqrt(n))))

def _table(df, keys, col):
    res = {}
    for k, g in df.groupby(keys, observed=True):
        res[k] = _agg(g[col])
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
            ret5 = c / c.shift(5) - 1
            rng = (b["high"] - b["low"]) / c
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            agit = np.where(b["regime"].astype(str) == "chop", "calm", "agit")
            for h in (3, 10):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, n, h)
                rows.append(pd.DataFrame(dict(coin=coin, w=w, h=h, stretch=stretch.values[idx], fwd=fwd.values[idx],
                                              agit=agit[idx], ret60=ret60.values[idx], ret5=ret5.values[idx],
                                              r1=r.values[idx], year=ts.dt.year.values[idx],
                                              fc=b["forecast"].values[idx], rng=rng.values[idx])))
            daily.append(pd.DataFrame(dict(coin=coin, w=w, r=r.values, nxt=r.shift(-1).values,
                                           nxt3=(c.shift(-3) / c - 1).values, agit=agit,
                                           wd=ts.dt.weekday.values, stretch=stretch.values,
                                           ret60=ret60.values, rng=rng.values)))
    df = pd.concat(rows, ignore_index=True).dropna(subset=["fwd", "stretch"])
    dd = pd.concat(daily, ignore_index=True).dropna(subset=["r", "nxt"])
    out = {}
    drift = df.groupby("h")["fwd"].mean()
    out["drift_by_h"] = drift
    df["ex"] = df["fwd"] - df["h"].map(drift)
    df["sbin"] = pd.cut(df["stretch"], [-99, -2, -1, 0, 1, 2, 99]).astype(str)
    df["trend"] = pd.cut(df["ret60"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"]).astype(str)
    for h in (3, 10):
        s = df[df.h == h]
        out[f"h{h}_agit_x_stretchbin"] = _table(s, ["agit", "sbin"], "ex")
        out[f"h{h}_trend_x_agit_x_below"] = _table(s.assign(below=s.stretch < 0), ["trend", "agit", "below"], "ex")
    s = df[df.h == 10]
    rho = {}
    for k, g in s.groupby("agit"):
        rr = stats.spearmanr(g["stretch"], g["ex"])
        rho[k] = dict(rho=rr[0], p=rr[1], n=len(g))
    out["h10_spearman_stretch_ex_by_agit"] = pd.DataFrame(rho).T
    out["h10_agit_below_by_year"] = _table(s[(s.agit == "agit") & (s.stretch < 0)], ["year"], "ex")
    out["h10_trend_x_agit_x_stretchbin"] = _table(s, ["trend", "agit", "sbin"], "ex")
    # daily angles
    dd["rq"] = pd.qcut(dd["r"], 5, labels=False)
    out["nextday_by_agit_x_rquintile"] = _table(dd, ["agit", "rq"], "nxt")
    out["next3_by_agit_x_rquintile"] = _table(dd.dropna(subset=["nxt3"]), ["agit", "rq"], "nxt3")
    out["nextday_by_weekday"] = _table(dd, ["wd"], "nxt")
    dd["rngq"] = dd.groupby("coin")["rng"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["nextday_by_agit_x_rangequintile"] = _table(dd, ["agit", "rngq"], "nxt")
    # book
    days = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            days.append(d.assign(coin=coin, w=w))
    D = pd.concat(days, ignore_index=True).dropna(subset=["book_return"])
    out["book_by_coin"] = _table(D, ["coin"], "book_return")
    out["book_by_window"] = _table(D, ["w"], "book_return")
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                T.append(t.assign(coin=coin, w=w))
    if T:
        T = pd.concat(T, ignore_index=True)
        T["fq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 4, labels=False)
        out["trades_by_entry_forecast_q"] = _table(T, ["fq"], "net_profit_loss_percent")
        out["trades_by_entry_regime"] = _table(T, ["entry_regime"], "net_profit_loss_percent")
    return out
