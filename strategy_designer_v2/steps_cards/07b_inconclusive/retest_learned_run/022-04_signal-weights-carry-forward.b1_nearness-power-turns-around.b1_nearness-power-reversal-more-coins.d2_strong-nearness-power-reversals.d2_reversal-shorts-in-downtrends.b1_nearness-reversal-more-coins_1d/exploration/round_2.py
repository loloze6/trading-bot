import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}; usual = {}
    for coin, wins in bars.items():
        allr = {h: [] for h in (5, 20)}
        for w, df in wins.items():
            c = df["close"].values; n = len(c)
            for h in allr:
                for i in range(0, n - h, h):
                    allr[h].append(c[i+h]/c[i]-1)
        drift[coin] = {h: np.mean(v) for h, v in allr.items()}
        usual[coin] = np.std(allr[5])
        for w, df in wins.items():
            c = df["close"].values; f = df["forecast"].values; n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            s = pd.Series(c)
            r20 = s.pct_change(20).values
            near = (s / s.rolling(60, min_periods=60).max()).values
            for i in range(0, n - 5, 5):
                rec = dict(coin=coin, window=w, year=ts.iloc[i].year, f=f[i], r20=r20[i], near=near[i],
                           u5=-(c[i+5]/c[i]-1 - drift[coin][5]))
                rec["u20"] = -(c[i+20]/c[i]-1 - drift[coin][20]) if i+20 < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    d["grp"] = np.where(d["r20"].isna(), "r20_nan", np.where(d["r20"] < 0, np.where(d["f"] < 0, "down_short", "down_flat"), "up"))
    out["u5_by_group"] = d.groupby("grp")["u5"].apply(tt).unstack()
    out["u20_by_group"] = d.groupby("grp")["u20"].apply(tt).unstack()
    dn = d[d["r20"] < 0].copy()
    a = dn.loc[dn["f"] < 0, "u5"].dropna(); b = dn.loc[dn["f"] == 0, "u5"].dropna()
    out["short_minus_flat_in_down_u5"] = pd.Series({"diff": a.mean()-b.mean(), "welch_t": stats.ttest_ind(a, b, equal_var=False).statistic, "n_a": len(a), "n_b": len(b)})
    dn["rq"] = pd.qcut(dn["r20"], 5, labels=False, duplicates="drop")
    out["down_all_by_r20_q"] = dn.groupby("rq").agg(r20=("r20", "mean")).join(dn.groupby("rq")["u5"].apply(tt).unstack())
    dd = d.dropna(subset=["r20"]).copy()
    dd["rq"] = pd.qcut(dd["r20"], 10, labels=False, duplicates="drop")
    out["all_by_r20_decile_u5"] = dd.groupby("rq").agg(r20=("r20", "mean")).join(dd.groupby("rq")["u5"].apply(tt).unstack())
    dn2 = dn.dropna(subset=["near"]).copy()
    dn2["nq"] = pd.qcut(dn2["near"], 5, labels=False, duplicates="drop")
    out["down_by_near60_q"] = dn2.groupby("nq").agg(near=("near", "mean")).join(dn2.groupby("nq")["u5"].apply(tt).unstack())
    out["down_by_year"] = dn.groupby("year")["u5"].apply(tt).unstack()
    return out
