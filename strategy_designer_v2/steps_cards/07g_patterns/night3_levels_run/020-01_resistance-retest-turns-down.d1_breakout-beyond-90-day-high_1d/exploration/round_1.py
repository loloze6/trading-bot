import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float)
            n = len(b)
            dist = b.get("debug_info.components.breakout_dist.last_history_value")
            if dist is None:
                dist = pd.Series(np.nan, index=b.index)
            dist = dist.astype(float)
            r1 = cl.pct_change()
            vol = r1.rolling(30, min_periods=15).std()
            ts = pd.to_datetime(b["timestamp"])
            for h in (5, 10, 20):
                fwd = cl.shift(-h) / cl - 1
                grid = np.arange(0, n, h)
                for i in grid:
                    if i + h < n:
                        rows.append(dict(coin=c, win=w, h=h, fwd=fwd.iloc[i], dist=dist.iloc[i],
                                         r1=r1.iloc[i], r5=cl.iloc[i]/cl.iloc[i-5]-1 if i>=5 else np.nan,
                                         r20=cl.iloc[i]/cl.iloc[i-20]-1 if i>=20 else np.nan,
                                         vol=vol.iloc[i], wd=ts.iloc[i].dayofweek,
                                         fc=float(b["forecast"].iloc[i])))
    df = pd.DataFrame(rows)
    # drift removal per coin per h
    df["drift"] = df.groupby(["coin", "h"])["fwd"].transform("mean")
    df["ex"] = df["fwd"] - df["drift"]
    out = {}
    def summ(g):
        x = g["ex"].dropna()
        return pd.Series({"n": len(x), "mean_ex": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    # distance buckets (incl below high)
    d = df.dropna(subset=["dist"]).copy()
    d["dbin"] = pd.cut(d["dist"], [-1e9, -40, -25, -15, -8, -3, 0, 5, 15, 1e9])
    out["dist_bins_by_h"] = d.groupby(["h", "dbin"]).apply(summ).unstack(0)
    # prior 20-day return buckets (per coin quintile)
    for col in ["r20", "r5", "r1"]:
        e = df[df.h == 5].dropna(subset=[col]).copy()
        e["q"] = e.groupby("coin")[col].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        out[f"{col}_quintile_h5"] = e.groupby("q").apply(summ)
    e = df[df.h == 5].dropna(subset=["vol"]).copy()
    e["q"] = e.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["vol_tercile_h5"] = e.groupby("q").apply(summ)
    # breakout cases by vol tercile at h=10
    e = df[(df.h == 10)].dropna(subset=["vol", "dist"]).copy()
    e["q"] = e.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False))
    e["above"] = e["dist"] > 0
    out["above_x_vol_h10"] = e.groupby(["above", "q"]).apply(summ)
    # weekday daily coin returns
    dd = []
    for c in days:
        for w, t in days[c].items():
            t = t.copy(); t["coin"] = c; dd.append(t)
    dd = pd.concat(dd)
    dd["wd"] = pd.to_datetime(dd["day"]).dt.dayofweek
    dd["ex"] = dd["coin_return"] - dd.groupby("coin")["coin_return"].transform("mean")
    out["weekday_coin"] = dd.groupby("wd").apply(summ)
    # book: per coin by year
    dd["year"] = pd.to_datetime(dd["day"]).dt.year
    out["book_by_coin"] = dd.groupby("coin").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"))
    out["book_by_year"] = dd.groupby("year").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"), n=("book_return", "count"))
    return out
