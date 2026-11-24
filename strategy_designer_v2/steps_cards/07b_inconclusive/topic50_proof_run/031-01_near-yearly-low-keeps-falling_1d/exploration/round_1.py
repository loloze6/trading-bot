import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H_list = [5, 10, 20, 40]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            raw = df.get("debug_info.components.low_prox.last_history_value", pd.Series(np.nan, index=df.index)).values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for H in H_list:
                for i in range(0, n - H, H):
                    r = c[i + H] / c[i] - 1
                    r60 = c[i] / c[i - 60] - 1 if i >= 60 else np.nan
                    r20p = c[i] / c[i - 20] - 1 if i >= 20 else np.nan
                    rows.append(dict(coin=coin, w=w, H=H, i=i, ret=r, af=abs(f[i]), raw=raw[i],
                                     r60=r60, r20p=r20p, year=yr[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "H"])["ret"].transform("mean")
    d["sg"] = -(d["ret"] - d["drift"])
    out = {}

    def slope(g):
        g = g.dropna(subset=["af", "sg"])
        if len(g) < 8 or g["af"].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan, mean_sg=g["sg"].mean()))
        r = stats.linregress(g["af"], g["sg"])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope / r.stderr, mean_sg=g["sg"].mean()))

    out["by_horizon"] = d.groupby("H").apply(slope)
    d20 = d[d.H == 20].copy()
    out["by_coin_20"] = d20.groupby("coin").apply(slope)
    out["by_window_20"] = d20.groupby("w").apply(slope)
    out["by_year_20"] = d20.groupby("year").apply(slope)
    d20["q"] = pd.qcut(d20["af"].rank(method="first"), 5, labels=False)
    out["quintile_20"] = d20.groupby("q").agg(n=("sg", "size"), af=("af", "mean"), mean_sg=("sg", "mean"),
                                              raw_ret=("ret", "mean"),
                                              t=("sg", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    d20["trend"] = pd.cut(d20["r60"], [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])
    out["by_trend_20"] = d20.groupby("trend").apply(slope)
    d20["prior20"] = np.where(d20["r20p"] < 0, "prior20_down", "prior20_up")
    out["by_prior20_20"] = d20.dropna(subset=["r20p"]).groupby("prior20").apply(slope)
    out["raw_desc"] = d20["raw"].describe()
    out["af_desc"] = d20["af"].describe()
    return out
