import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            raw = df.get("debug_info.components.sma_cross.last_history_value")
            raw = raw.values if raw is not None else np.full(len(df), np.nan)
            ts = pd.to_datetime(df["timestamp"])
            # past 20d return inside window
            for h in [5, 10, 20, 40]:
                for i in range(0, len(df) - h, h):
                    rows.append(dict(coin=coin, w=w, wn=int(w[1:]), year=ts.iloc[i].year, h=h,
                                     f=f[i], raw=raw[i],
                                     past20=(c[i] / c[i-20] - 1) if i >= 20 else np.nan,
                                     r=c[i+h] / c[i] - 1))
    d = pd.DataFrame(rows)
    d["ex"] = d["r"] - d.groupby(["coin", "h"])["r"].transform("mean")
    out = {}
    # slope by horizon
    res = []
    for h, g in d.groupby("h"):
        s = stats.linregress(g["f"], g["ex"])
        on = g[g.f > 0]; off = g[g.f <= 0]
        t = stats.ttest_ind(on["ex"], off["ex"], equal_var=False)
        res.append(dict(h=h, n=len(g), n_on=len(on), slope=s.slope, t_slope=s.slope / s.stderr,
                        ex_on=on["ex"].mean(), ex_off=off["ex"].mean(), t_on_off=t.statistic))
    out["by_horizon"] = pd.DataFrame(res)
    g = d[d.h == 10].copy()
    g["fb"] = pd.cut(g["f"], [-1, 0, 5, 10, 15, 21], labels=["0", "0-5", "5-10", "10-15", "15-20"])
    out["h10_by_forecast_bucket"] = g.groupby("fb")["ex"].agg(["count", "mean", "std", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # raw spread buckets
    g["rawq"] = pd.qcut(g["raw"], 5, duplicates="drop")
    out["h10_by_raw_spread_q"] = g.groupby("rawq")["ex"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    def sl(x):
        if len(x) < 10 or x["f"].std() == 0: return pd.Series(dict(n=len(x), slope=np.nan, t=np.nan))
        s = stats.linregress(x["f"], x["ex"]); return pd.Series(dict(n=len(x), slope=s.slope, t=s.slope/s.stderr, ex_on=x.loc[x.f>0,"ex"].mean(), ex_off=x.loc[x.f<=0,"ex"].mean()))
    out["h10_by_coin"] = g.groupby("coin").apply(sl)
    out["h10_by_year"] = g.groupby("year").apply(sl)
    g20 = d[d.h == 20]
    out["h20_by_coin"] = g20.groupby("coin").apply(sl)
    # regime: past 20d return sign among forecast>0
    on = g[g.f > 0].copy()
    on["p20pos"] = on["past20"] > 0
    out["h10_on_by_past20sign"] = on.groupby("p20pos")["ex"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    return out
