import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    raw_col = "debug_info.components.below_age.last_history_value"
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            r30 = pd.Series(c).pct_change(30).values
            for h in (7, 14, 28):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=yr[i],
                                     fc=df["forecast"].iloc[i], raw=df[raw_col].iloc[i],
                                     r30=r30[i], ret=c[i + h] / c[i] - 1))
    g = pd.DataFrame(rows)
    g["ex"] = g["ret"] - g.groupby(["coin", "h"])["ret"].transform("mean")
    out = {}
    res = []
    for h in (7, 14, 28):
        d = g[(g.h == h) & (g.fc > 0)]
        lng = d[d.raw <= -30].ex; sht = d[d.raw > -30].ex
        tt = stats.ttest_ind(lng, sht, equal_var=False)
        t1 = stats.ttest_1samp(lng, 0)
        res.append(dict(h=h, n_long=len(lng), mean_long=lng.mean(), t_long_vs0=t1.statistic,
                        n_short=len(sht), mean_short=sht.mean(), diff=lng.mean() - sht.mean(), welch_t=tt.statistic))
        dd = d[d.raw > -30]
        r = stats.linregress(dd.fc, dd.ex)
        res.append(dict(h=h, n_long=np.nan, mean_long=np.nan, t_long_vs0=np.nan, n_short=len(dd),
                        mean_short=r.slope, diff=np.nan, welch_t=r.slope / r.stderr))
    out["longest_runs_vs_rest (2nd row per h: slope,t excl raw<=-30)"] = pd.DataFrame(res)
    d14 = g[(g.h == 14) & (g.fc > 0)].copy()
    out["corr_fc_raw_h14"] = d14[["fc", "raw"]].corr().iloc[0, 1]
    d14["r30bin"] = pd.qcut(d14.r30, 3, labels=["fell_most", "mid", "fell_least"])
    tab = []
    for b, db in d14.groupby("r30bin", observed=True):
        r = stats.linregress(db.fc, db.ex)
        tab.append(dict(r30bin=b, n=len(db), mean_r30=db.r30.mean(), mean_ex=db.ex.mean(), slope=r.slope, t=r.slope / r.stderr))
    out["by_30d_return_h14"] = pd.DataFrame(tab)
    lr = d14[d14.raw <= -30]
    out["longest_runs_by_coin_h14"] = lr.groupby("coin")["ex"].agg(["count", "mean", "std"])
    out["longest_runs_by_year_h14"] = lr.groupby("year")["ex"].agg(["count", "mean"])
    return out
