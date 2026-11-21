import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    # 1. weekday effect: per coin, per year, Sat and Fri vs other days; use one value per day averaged across coins for independence
    D = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            D.append(pd.DataFrame(dict(coin=coin, win=w, r=c.pct_change(), wd=ts.dt.weekday, year=ts.dt.year, day=ts.dt.floor("D"))))
    D = pd.concat(D).dropna(subset=["r"])
    D["sat"] = D.wd == 5
    def welch(x):
        a = x[x.sat].r; o = x[~x.sat].r
        t = stats.ttest_ind(a, o, equal_var=False)
        return pd.Series(dict(n_sat=len(a), sat=a.mean(), other=o.mean(), t=t.statistic))
    out["sat_vs_other_by_coin"] = D.groupby("coin").apply(welch).round(5)
    out["sat_vs_other_by_year"] = D.groupby("year").apply(welch).round(5)
    M = D.groupby(["day", "wd"]).r.mean().reset_index()
    wd = M.groupby("wd").r.agg(["size", "mean", "std"]); wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["size"]))
    out["coin_mean_by_weekday_one_per_day"] = wd.round(5)
    # Saturday return graded by Friday's return? and by vol
    # 2. after breaks: forward return at several horizons from case bars (forecast rise from 0)
    rows = []
    for coin, wins in data["bars"].items():
        allg = {h: [] for h in (5, 10, 20)}
        recs = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); fc = b["forecast"].astype(float).fillna(0)
            n = len(c); pos = np.arange(n)
            for h in (5, 10, 20):
                f = c.shift(-h) / c - 1
                allg[h].append(f[(pos % h == 0)].dropna())
            start = (fc > 0) & (fc.shift(1).fillna(0) <= 0)
            for i in np.where(start)[0]:
                d = dict(coin=coin, fc=fc.iloc[i])
                for h in (5, 10, 20):
                    d[f"f{h}"] = c.iloc[i + h] / c.iloc[i] - 1 if i + h < n else np.nan
                d["mad"] = b["debug_info.components.ma_dist.last_history_value"].iloc[i]
                recs.append(d)
        R = pd.DataFrame(recs)
        for h in (5, 10, 20):
            s = pd.concat(allg[h])
            R[f"u{h}"] = R[f"f{h}"] - s.mean()
            R[f"s{h}"] = R[f"u{h}"] / s.std()
        rows.append(R)
    R = pd.concat(rows)
    res = {}
    for h in (5, 10, 20):
        x = R[f"u{h}"].dropna()
        res[h] = dict(n=len(x), un=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))), strength=R[f"s{h}"].mean(),
                      total=R[f"f{h}"].mean())
    out["break_starts_forward_by_horizon"] = pd.DataFrame(res).T.round(4)
    R["mq"] = pd.qcut(R.mad.rank(method="first"), 4, labels=False)
    out["break_starts_u10_by_mad"] = R.groupby("mq").agg(n=("u10", "count"), mad=("mad", "mean"), u5=("u5", "mean"), u10=("u10", "mean"), u20=("u20", "mean")).round(4)
    out["spearman_mad_u20"] = stats.spearmanr(R.mad, R.u20, nan_policy="omit").correlation
    # 3. trades: entry forecast vs pnl
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)])
    out["spearman_entryfc_pnl"] = stats.spearmanr(T.entry_forecast, T.net_profit_loss_percent).correlation
    out["n_trades"] = len(T)
    return out
