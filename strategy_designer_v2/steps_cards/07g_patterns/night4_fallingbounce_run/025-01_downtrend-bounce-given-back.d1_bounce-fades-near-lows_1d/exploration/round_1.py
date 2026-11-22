import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    rows = []
    drift = {}
    for coin in bars:
        g = []
        for w, b in bars[coin].items():
            c = b["close"].values
            for i in range(0, len(c) - 5, 5):
                g.append(c[i+5]/c[i]-1)
        drift[coin] = (np.mean(g), np.std(g))
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            sd = r1.rolling(20, min_periods=15).std()
            z = r1 / sd
            r5p = c / c.shift(5) - 1
            r20p = c / c.shift(20) - 1
            low = c.rolling(60, min_periods=30).min()
            dist = c / low - 1
            fwd = c.shift(-5) / c - 1
            hl = (b["high"] - b["low"]) / c
            wd = pd.to_datetime(b["timestamp"]).dt.weekday
            for i in range(0, len(b) - 5, 5):
                rows.append(dict(coin=coin, w=w, z=z[i], r5p=r5p[i] / (sd[i]*np.sqrt(5)) if sd[i] else np.nan,
                                 r20p=r20p[i], dist=dist[i], sd=sd[i], hl=hl[i], wd=wd[i],
                                 reg=b["regime"][i], fwd=fwd[i],
                                 un=fwd[i]-drift[coin][0], st=(fwd[i]-drift[coin][0])/drift[coin][1],
                                 fc=b["forecast"][i], alloc=b["postRebalance_current_allocation"][i]))
    df = pd.DataFrame(rows).dropna(subset=["fwd"])
    def summ(gr, col="st"):
        a = gr[col].dropna()
        return pd.Series(dict(n=len(a), mean_st=a.mean(), mean_un=gr["un"].mean(),
                              t=a.mean()/(a.std()/np.sqrt(len(a))) if len(a) > 2 else np.nan))
    out = {}
    df["zb"] = pd.cut(df["z"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["fwd5 by 1d z and regime"] = df.groupby(["reg", "zb"], observed=True).apply(summ)
    df["r5b"] = pd.cut(df["r5p"], [-np.inf, -1.5, -0.5, 0.5, 1.5, np.inf])
    out["fwd5 by past5d z and regime"] = df.groupby(["reg", "r5b"], observed=True).apply(summ)
    df["r20b"] = pd.qcut(df["r20p"], 5)
    out["fwd5 by past20d ret quintile"] = df.groupby("r20b", observed=True).apply(summ)
    df["sdq"] = df.groupby("coin")["sd"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["fwd5 by vol tercile"] = df.groupby("sdq").apply(summ)
    df["dq"] = pd.qcut(df["dist"], 5)
    out["fwd5 by dist above 60d low"] = df.groupby("dq", observed=True).apply(summ)
    df["hlz"] = df.groupby("coin")["hl"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out["fwd5 by range quartile"] = df.groupby("hlz").apply(summ)
    out["fwd5 by coin"] = df.groupby("coin").apply(summ)
    # daily: weekday
    dd = []
    for coin in days:
        for w, d in days[coin].items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; dd.append(d)
    dd = pd.concat(dd)
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    out["coin ret by weekday"] = dd.groupby("wd")["coin_return"].agg(["count", "mean", lambda s: s.mean()/(s.std()/np.sqrt(len(s.dropna())))])
    out["book ret by weekday"] = dd.groupby("wd")["book_return"].agg(["count", "mean"])
    # book daily, mean over coins
    bk = dd.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book by window sum"] = bk.groupby(level=0)["book_return"].agg(["count", "mean"]).sort_values("mean")
    # trades
    tr = []
    for coin in trades:
        for w, t in trades[coin].items():
            t = t.copy(); t["coin"] = coin; tr.append(t)
    tr = pd.concat(tr)
    tr["fq"] = pd.qcut(tr["entry_forecast"].abs(), 4, duplicates="drop")
    out["trades by |entry fc|"] = tr.groupby(["side", "fq"], observed=True)["profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades by dur days"] = tr.assign(dur=(tr["duration_minutes"]/1440).round()).groupby("dur")["profit_loss_percent"].agg(["count", "mean"]).head(15)
    return out
