import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    out = {}
    rows = []
    for H in [3, 7, 14, 21]:
        for coin, wins in bars.items():
            # coin mean H-return on grid over all windows
            allr = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - H, H):
                    allr.append(c[i+H]/c[i]-1)
            mu = np.mean(allr) if allr else np.nan
            for w, df in wins.items():
                c = df["close"].values; f = df["forecast"].values
                yr = pd.to_datetime(df["timestamp"]).dt.year.values
                day = pd.to_datetime(df["timestamp"]).dt.floor("D").values
                for i in range(0, len(c) - H, H):
                    if f[i] > 0:
                        rows.append(dict(H=H, coin=coin, w=w, yr=yr[i], day=day[i], f=f[i],
                                         ex=c[i+H]/c[i]-1-mu, tot=c[i+H]/c[i]-1))
    d = pd.DataFrame(rows)
    def summ(g):
        dd = g.groupby("day")["ex"].sum()
        n = g["day"].nunique()
        m = g["ex"].mean()
        se = np.sqrt((dd - dd.index.map(lambda x: 0)).pow(2).sum()) if False else None
        dev = (g["ex"] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev**2).sum())/len(g)
        return pd.Series(dict(n=len(g), days=n, mean=m, t=m/se if se>0 else np.nan,
                              share_pos=(g["ex"]>0).mean(), median=g["ex"].median()))
    out["by_horizon"] = d.groupby("H").apply(summ)
    d7 = d[d.H == 7].copy()
    out["h7_by_coin"] = d7.groupby("coin").apply(summ)
    out["h7_by_window"] = d7.groupby("w").apply(summ)
    out["h7_by_year"] = d7.groupby("yr").apply(summ)
    d7["fq"] = pd.qcut(d7["f"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["h7_by_forecast_tercile"] = d7.groupby("fq").apply(summ)
    out["h7_forecast_range"] = d7.groupby("fq")["f"].agg(["min", "max", "mean"])
    # outlier influence
    s = d7["ex"].sort_values()
    out["h7_mean_drop_top3"] = float(s.iloc[:-3].mean())
    out["h7_top5_ex"] = pd.Series(s.iloc[-5:].values)
    out["h7_spearman_f_ex"] = pd.Series(stats.spearmanr(d7["f"], d7["ex"]), index=["rho", "p"])
    return out
