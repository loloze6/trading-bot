import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            r1 = pd.Series(c).pct_change()
            s20 = r1.rolling(20).std()
            sma = pd.Series(c).rolling(20).mean()
            raw = (pd.Series(c) - sma) / sma / s20
            sw30 = r1.rolling(30).std()
            agit = sw30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for h in [1, 3, 5, 10, 20]:
                idx = np.arange(0, len(df) - h, h)
                for i in idx:
                    rows.append(dict(coin=coin, w=w, h=h, i=i, ts=df["timestamp"].iloc[i],
                                     yr=yr.iloc[i], fc=df["forecast"].iloc[i],
                                     chop=df["regime"].iloc[i] != "chop",
                                     raw=raw.iloc[i], agit=agit.iloc[i],
                                     ret=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows)
    drift = d.groupby(["coin", "h"])["ret"].mean().rename("drift")
    d = d.join(drift, on=["coin", "h"])
    d["ex"] = d["ret"] - d["drift"]
    a = d[d.chop & (d.fc != 0) & d.fc.notna()].copy()
    a["dirx"] = np.sign(a.fc) * a.ex

    def tstat(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))

    def slope(g):
        g = g.dropna(subset=["fc", "ex"])
        if len(g) < 10: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        s = stats.linregress(g.fc, g.ex)
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope / s.stderr))

    out = {}
    out["slope by horizon"] = a.groupby("h").apply(slope)
    out["dir excess by horizon and side"] = a.groupby(["h", np.sign(a.fc)])["dirx"].apply(tstat).unstack()
    a10 = a[a.h == 10].copy()
    out["h10 by coin"] = a10.groupby("coin").apply(slope)
    out["h10 by year"] = a10.groupby("yr").apply(slope)
    a10["ag"] = np.where(a10.agit > 0.5, "agitated", np.where(a10.agit.notna(), "calm", "na"))
    out["h10 by agitation"] = a10.groupby("ag").apply(slope)
    a10["q"] = pd.qcut(a10.fc, 5, labels=False)
    out["h10 ex by forecast quintile"] = a10.groupby("q").agg(fc=("fc", "mean"), raw=("raw", "mean"), ex=("ex", "mean"), n=("ex", "size"))
    a10["absq"] = pd.qcut(a10.fc.abs(), 4, labels=False)
    out["h10 dirx by |fc| quartile"] = a10.groupby("absq")["dirx"].apply(tstat).unstack()
    # raw stretch (unstandardised) vs forecast
    b = d[d.chop & d.raw.notna()]
    out["raw stretch slope by horizon (all choppy)"] = b.assign(fc=b.raw).groupby("h").apply(slope)
    out["corr fc raw h10"] = float(a10[["fc", "raw"]].corr().iloc[0, 1])
    return out
