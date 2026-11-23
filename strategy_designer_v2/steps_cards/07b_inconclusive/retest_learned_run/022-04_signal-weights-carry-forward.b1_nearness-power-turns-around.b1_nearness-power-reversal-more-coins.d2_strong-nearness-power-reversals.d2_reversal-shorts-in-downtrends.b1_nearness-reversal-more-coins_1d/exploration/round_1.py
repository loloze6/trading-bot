import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        allr = {h: [] for h in (1, 3, 5, 10, 20)}
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            for h in allr:
                for i in range(0, n - h, h):
                    allr[h].append(c[i+h]/c[i]-1)
        drift[coin] = {h: np.mean(v) if v else np.nan for h, v in allr.items()}
        usual[coin] = np.std(allr[5]) if allr[5] else np.nan
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            r20 = pd.Series(c).pct_change(20).values
            raw = df.get("debug_info.components.excess_power.last_history_value")
            raw = raw.values if raw is not None else np.full(n, np.nan)
            for i in range(0, n - 5, 5):
                if f[i] < 0:
                    rec = dict(coin=coin, window=w, year=ts.iloc[i].year,
                               af=abs(f[i]), r20=r20[i], raw=raw[i])
                    for h in (1, 3, 5, 10, 20):
                        if i + h < n:
                            rec[f"u{h}"] = -(c[i+h]/c[i]-1 - drift[coin][h])
                            rec[f"t{h}"] = -(c[i+h]/c[i]-1)
                        else:
                            rec[f"u{h}"] = np.nan; rec[f"t{h}"] = np.nan
                    rec["str"] = rec["u5"]/usual[coin]
                    rows.append(rec)
    d = pd.DataFrame(rows)
    d["wt"] = d["af"]/d["af"].mean()
    d["wu5"] = d["u5"]*d["wt"]
    def tt(x):
        x = x.dropna(); 
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out = {}
    out["overall_weighted"] = tt(d["wu5"])
    out["overall_unweighted"] = tt(d["u5"])
    out["overall_total"] = tt(d["t5"])
    out["by_horizon_unusual"] = pd.DataFrame({h: tt(d[f"u{h}"]) for h in (1,3,5,10,20)}).T
    out["by_coin"] = d.groupby("coin")["u5"].apply(tt).unstack()
    out["by_year"] = d.groupby("year")["u5"].apply(tt).unstack()
    d["fq"] = pd.qcut(d["af"], 5, labels=False, duplicates="drop")
    out["by_forecast_quintile"] = d.groupby("fq").agg(af=("af","mean")).join(d.groupby("fq")["u5"].apply(tt).unstack())
    d["rq"] = pd.qcut(d["r20"], 5, labels=False, duplicates="drop")
    out["by_r20_quintile"] = d.groupby("rq").agg(r20=("r20","mean")).join(d.groupby("rq")["u5"].apply(tt).unstack())
    out["strength_mean"] = d["str"].mean()
    out["corr_af_u5"] = d[["af","u5"]].corr().iloc[0,1]
    out["corr_r20_u5"] = d[["r20","u5"]].corr().iloc[0,1]
    return out
