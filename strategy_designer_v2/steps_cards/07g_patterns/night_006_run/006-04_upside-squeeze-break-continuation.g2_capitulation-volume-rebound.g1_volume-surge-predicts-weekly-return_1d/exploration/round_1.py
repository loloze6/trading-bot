import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; v = b["volume"].values
            h = b["high"].values; l = b["low"].values
            n = len(b)
            s = pd.Series(c)
            r1 = s.pct_change()
            ret5 = s / s.shift(5) - 1
            ret20 = s / s.shift(20) - 1
            rng = pd.Series((h - l) / c)
            rngratio = np.log(rng.rolling(5).mean() / rng.rolling(30).mean())
            vol20 = r1.rolling(20).std()
            vr = np.log(pd.Series(v).rolling(5).mean() / pd.Series(v).rolling(30).mean())
            for t in range(0, n - 7, 7):
                rows.append(dict(coin=coin, w=w, t=t,
                    fwd=c[t+7]/c[t]-1, fc=b["forecast"].iloc[t],
                    ret5=ret5.iloc[t], ret20=ret20.iloc[t], rr=rngratio.iloc[t],
                    vol20=vol20.iloc[t], vr=vr.iloc[t],
                    wd=pd.Timestamp(b["timestamp"].iloc[t]).weekday(),
                    yr=pd.Timestamp(b["timestamp"].iloc[t]).year))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    d["absex"] = d["fwd"].abs() - d.groupby("coin")["fwd"].transform(lambda x: x.abs().mean())
    out = {}
    def qtab(col, target="ex", q=5):
        x = d.dropna(subset=[col, target]).copy()
        x["q"] = pd.qcut(x[col], q, labels=False, duplicates="drop")
        g = x.groupby("q")[target].agg(["mean", "count"])
        g["t"] = x.groupby("q")[target].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s))))
        return g
    def slope(col, target="ex", by=None):
        x = d.dropna(subset=[col, target])
        if by is None:
            r = stats.linregress(x[col], x[target]); return pd.Series({"slope": r.slope, "t": r.slope/r.stderr, "n": len(x)})
        res = {}
        for k, g in x.groupby(by):
            r = stats.linregress(g[col], g[target]); res[k] = {"slope": r.slope, "t": r.slope/r.stderr, "n": len(g)}
        return pd.DataFrame(res).T
    out["fc quintile -> ex7"] = qtab("fc")
    out["fc slope by coin"] = slope("fc", by="coin")
    out["fc slope by year"] = slope("fc", by="yr")
    out["ret5 quintile -> ex7"] = qtab("ret5")
    out["ret20 quintile -> ex7"] = qtab("ret20")
    out["vol20 quintile -> ex7"] = qtab("vol20")
    out["range ratio q -> ex7"] = qtab("rr")
    out["range ratio q -> abs ex7"] = qtab("rr", "absex")
    out["volratio q -> abs ex7"] = qtab("vr", "absex")
    out["ret5 slope by coin"] = slope("ret5", by="coin")
    out["ret20 slope by coin"] = slope("ret20", by="coin")
    # book decomposition and weekday
    dd = []
    for coin, wins in days.items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    D = pd.concat(dd)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    g = D.groupby("wd")["coin_return"].agg(["mean", "count", "std"])
    g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["coin daily ret by weekday"] = g
    bk = D.groupby("w")[["book_return", "coin_return"]].mean()
    out["book vs coin mean by window"] = bk
    return out
