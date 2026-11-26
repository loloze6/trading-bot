import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            allr.append(pd.Series(b["close"].values).pct_change().dropna())
        drift = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            n = len(c)
            r = np.r_[np.nan, c[1:] / c[:-1] - 1]
            inprof = (b["regime"] != "chop").values
            for t in range(1, n - 3):
                if not (r[t] > 0 and inprof[t]):
                    continue
                k = 0; j = t - 1
                while j >= 1 and r[j] < 0 and k < 30:
                    k += 1; j -= 1
                u = 0; j = t - 1
                while j >= 1 and r[j] > 0 and u < 30:
                    u += 1; j -= 1
                rows.append(dict(coin=coin, win=w,
                                 year=pd.Timestamp(b["timestamp"].iloc[t]).year,
                                 day=str(b["timestamp"].iloc[t])[:10],
                                 run=k, uprun=u, r0=r[t],
                                 n1=c[t+1]/c[t]-1-drift,
                                 n2=c[t+2]/c[t]-1-2*drift,
                                 n3=c[t+3]/c[t]-1-3*drift))
    d = pd.DataFrame(rows)

    def summ(g, col="n1"):
        s = -g[col]
        dd = s.groupby(g["day"]).sum()
        t = s.mean() / (dd.std(ddof=1) * np.sqrt(len(dd)) / len(s)) if len(dd) > 2 else np.nan
        return pd.Series(dict(n=len(s), days=len(dd), mean_short=s.mean(), t_day=t))

    d["runb"] = d["run"].clip(upper=4)
    out = {}
    out["by_run_n1"] = d.groupby("runb").apply(summ)
    out["by_run_n2"] = d.groupby("runb").apply(lambda g: summ(g, "n2"))
    out["by_run_n3"] = d.groupby("runb").apply(lambda g: summ(g, "n3"))
    act = d[d.run >= 1].copy()
    out["active_by_coin"] = act.groupby("coin").apply(summ)
    out["active_by_win"] = act.groupby("win").apply(summ)
    out["active_by_year"] = act.groupby("year").apply(summ)
    act["r0q"] = pd.qcut(act["r0"], 3, labels=["small", "mid", "large"])
    out["active_by_upsize"] = act.groupby("r0q").apply(summ)
    sl = stats.linregress(act["run"], act["n1"])
    out["slope_run_n1_active"] = pd.Series(dict(slope=sl.slope, t=sl.slope / sl.stderr, n=len(act)))
    sl0 = stats.linregress(d["run"], d["n1"])
    out["slope_run_n1_all_updays"] = pd.Series(dict(slope=sl0.slope, t=sl0.slope / sl0.stderr, n=len(d)))
    a1 = -d[d.run >= 1].n1; a0 = -d[d.run == 0].n1
    out["afterfall_minus_afterrise"] = pd.Series(dict(
        diff=a1.mean() - a0.mean(),
        t=stats.ttest_ind(a1, a0, equal_var=False).statistic,
        n_fall=len(a1), n_rise=len(a0)))
    return out
