import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    info = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            n = len(c)
            info.append(n)
            if n < 40: continue
            r1 = c.pct_change()
            ret30 = c / c.shift(30) - 1
            ret5 = c / c.shift(5) - 1
            vol10 = r1.rolling(10).std()
            vol30 = r1.rolling(30, min_periods=20).std()
            hi = c.shift(1).rolling(60, min_periods=30).max()
            lo = c.shift(1).rolling(60, min_periods=30).min()
            dist_hi = c / hi - 1
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            fc = df["forecast"].astype(float).reset_index(drop=True)
            for h in (5, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, fwd=c[i+h]/c[i]-1,
                        ret30=ret30[i], ret5=ret5[i], r1=r1[i],
                        volratio=vol10[i]/vol30[i] if (vol30[i] and not np.isnan(vol30[i])) else np.nan,
                        vol30=vol30[i], dist_hi=dist_hi[i],
                        wd=ts[i].weekday(), yr=ts[i].year, active=fc[i] != 0))
    d = pd.DataFrame(rows)
    out = {"window_len": pd.Series(info).describe()}
    def summ(g):
        g = g.dropna(subset=["z"])
        m = len(g)
        return pd.Series(dict(n=m, mean_un=g.un.mean(), z=g.z.mean(),
                              t=g.z.mean()/(g.z.std()/np.sqrt(m)) if m > 2 else np.nan))
    for h in (5, 20):
        x = d[d["h"] == h].copy()
        x["un"] = x["fwd"] - x.groupby("coin")["fwd"].transform("mean")
        x["sd"] = x.groupby("coin")["fwd"].transform("std")
        x["z"] = x["un"] / x["sd"]
        for var in ["ret30", "ret5", "r1", "volratio", "vol30", "dist_hi"]:
            y = x.dropna(subset=[var]).copy()
            y["q"] = y.groupby("coin")[var].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
            out[f"h{h}_by_{var}_q"] = y.groupby("q").apply(summ)
        out[f"h{h}_by_active"] = x.groupby("active").apply(summ)
        if h == 5:
            out["h5_by_weekday"] = x.groupby("wd").apply(summ)
        out[f"h{h}_by_coin"] = x.groupby("coin").apply(summ)
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            dd.append(df.assign(coin=coin, win=w))
    D = pd.concat(dd)
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    out["book_by_year"] = D.groupby("yr").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    tr = []
    for coin, wins in data["trades"].items():
        for w, df in wins.items():
            if len(df): tr.append(df.assign(coin=coin))
    T = pd.concat(tr)
    T["af"] = T["entry_forecast"].abs()
    T["dur_d"] = T["duration_minutes"] / 1440
    out["trades_by_coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "count"), mean=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda s: (s > 0).mean()), dur=("dur_d", "mean"))
    T["qf"] = pd.qcut(T["af"].rank(method="first"), 4, labels=False)
    out["trades_by_forecast_q"] = T.groupby("qf").agg(n=("net_profit_loss_percent", "count"), mean=("net_profit_loss_percent", "mean"), med=("net_profit_loss_percent", "median"), af=("af", "mean"))
    T["yr"] = pd.to_datetime(T["entry_time"]).dt.year
    out["trades_by_year"] = T.groupby("yr").agg(n=("net_profit_loss_percent", "count"), mean=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda s: (s > 0).mean()))
    return out
