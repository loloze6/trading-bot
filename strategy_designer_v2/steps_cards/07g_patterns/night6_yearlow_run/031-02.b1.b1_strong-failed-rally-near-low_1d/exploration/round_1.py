import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            lr = np.log(c)
            dret = pd.Series(c).pct_change()
            vol20 = dret.rolling(20).std().values
            for h in (5, 20):
                for i in range(0, n - h, h):
                    r = c[i + h] / c[i] - 1
                    past20 = c[i] / c[i - 20] - 1 if i >= 20 else np.nan
                    past5 = c[i] / c[i - 5] - 1 if i >= 5 else np.nan
                    rows.append(dict(coin=coin, win=w, h=h, ret=r,
                        regime=df["regime"].iloc[i],
                        score=df.get("debug_info.regime_scores.mean_reversion", pd.Series([np.nan]*n)).iloc[i],
                        rally=df.get("debug_info.components.rally.last_history_value", pd.Series([np.nan]*n)).iloc[i],
                        fc=df["forecast"].iloc[i], past20=past20, past5=past5, vol20=vol20[i],
                        wd=pd.Timestamp(df["timestamp"].iloc[i]).dayofweek))
    g = pd.DataFrame(rows)
    # drift per coin and h
    g["drift"] = g.groupby(["coin", "h"])["ret"].transform("mean")
    g["ex"] = g["ret"] - g["drift"]
    def summ(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x) > 2 else np.nan))
    out = {}
    g20 = g[g.h == 20]; g5 = g[g.h == 5]
    out["h20 ex by regime"] = g20.groupby("regime")["ex"].apply(summ).unstack()
    out["h5 ex by regime"] = g5.groupby("regime")["ex"].apply(summ).unstack()
    out["score describe"] = g20["score"].describe()
    s = g20.dropna(subset=["score"]).copy()
    s["sq"] = pd.qcut(s["score"].rank(method="first"), 5, labels=False)
    out["h20 ex by score quintile"] = s.groupby("sq")["ex"].apply(summ).unstack()
    s5 = g5.dropna(subset=["score"]).copy()
    s5["sq"] = pd.qcut(s5["score"].rank(method="first"), 5, labels=False)
    out["h5 ex by score quintile"] = s5.groupby("sq")["ex"].apply(summ).unstack()
    r = g20[g20.regime == "mean_reversion"].dropna(subset=["rally"]).copy()
    out["rally describe"] = r["rally"].describe()
    r["rq"] = pd.qcut(r["rally"].rank(method="first"), 3, labels=False)
    out["h20 in-regime ex by rally tercile"] = r.groupby("rq")["ex"].apply(summ).unstack()
    for h, gg in ((20, g20), (5, g5)):
        p = gg.dropna(subset=["past20"]).copy()
        p["pq"] = pd.qcut(p["past20"].rank(method="first"), 5, labels=False)
        out[f"h{h} ex by past20 quintile"] = p.groupby("pq")["ex"].apply(summ).unstack()
        v = gg.dropna(subset=["vol20"]).copy()
        v["vq"] = pd.qcut(v["vol20"].rank(method="first"), 3, labels=False)
        out[f"h{h} ex by vol20 tercile"] = v.groupby("vq")["ex"].apply(summ).unstack()
    p = g5.dropna(subset=["past5"]).copy()
    p["z"] = p["past5"] / (p["vol20"] * np.sqrt(5))
    p["zq"] = pd.qcut(p["z"].rank(method="first"), 5, labels=False)
    out["h5 ex by past5 z quintile"] = p.groupby("zq")["ex"].apply(summ).unstack()
    # daily weekday
    d = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df[["day", "coin_return", "book_return"]].copy(); x["coin"] = coin
            d.append(x)
    d = pd.concat(d).dropna()
    d["wd"] = pd.to_datetime(d["day"]).dt.dayofweek
    d["ex"] = d["coin_return"] - d.groupby("coin")["coin_return"].transform("mean")
    out["daily ex by weekday"] = d.groupby("wd")["ex"].apply(summ).unstack()
    d["yr"] = pd.to_datetime(d["day"]).dt.year
    out["book daily by year"] = d.groupby("yr")["book_return"].apply(summ).unstack()
    return out
