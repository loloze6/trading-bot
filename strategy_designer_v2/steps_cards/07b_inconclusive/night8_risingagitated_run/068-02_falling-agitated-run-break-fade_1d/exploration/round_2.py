import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        allr = [pd.Series(b["close"].values).pct_change().dropna() for b in wins.values()]
        drift = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float); n = len(c)
            r = np.r_[np.nan, c[1:] / c[:-1] - 1]
            inprof = (b["regime"] != "chop").values
            for t in range(6, n - 1):
                if not (r[t] > 0 and inprof[t]):
                    continue
                k = 0; j = t - 1
                while j >= 1 and r[j] < 0 and k < 30: k += 1; j -= 1
                u = 0; j = t - 1
                while j >= 1 and r[j] > 0 and u < 30: u += 1; j -= 1
                past = r[t-5:t]
                rows.append(dict(coin=coin, win=w, day=str(b["timestamp"].iloc[t])[:10],
                                 run=k, uprun=u, signed=k - u,
                                 downs5=int((past < 0).sum()),
                                 ret5=c[t-1]/c[t-6]-1,
                                 n1=c[t+1]/c[t]-1-drift))
    d = pd.DataFrame(rows)

    def cl_slope(x, y, day):
        x = np.asarray(x, float); y = np.asarray(y, float)
        X = np.c_[np.ones_like(x), x]
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        S = pd.DataFrame(X * e[:, None]).groupby(np.asarray(day)).sum().values
        V = XtXi @ (S.T @ S) @ XtXi
        return pd.Series(dict(slope=beta[1], t_cluster=beta[1] / np.sqrt(V[1, 1]),
                              n=len(y), days=len(set(day))))

    def summ(g):
        s = -g["n1"]; dd = s.groupby(g["day"]).sum()
        return pd.Series(dict(n=len(s), days=len(dd), mean_short=s.mean(),
                              t_day=s.mean() / (dd.std(ddof=1) * np.sqrt(len(dd)) / len(s))))

    act = d[d.run >= 1]
    out = {}
    out["slope_run_active_cluster"] = cl_slope(act.run, act.n1, act.day)
    out["slope_run_capped3_active"] = cl_slope(act.run.clip(upper=3), act.n1, act.day)
    out["slope_run_all_up_cluster"] = cl_slope(d.run, d.n1, d.day)
    out["slope_signed_all_up_cluster"] = cl_slope(d.signed, d.n1, d.day)
    out["slope_downs5_all_up_cluster"] = cl_slope(d.downs5, d.n1, d.day)
    out["slope_ret5_all_up_cluster"] = cl_slope(d.ret5, d.n1, d.day)
    out["by_downs5"] = d.groupby("downs5").apply(summ)
    out["by_uprun_when_run0"] = d[d.run == 0].assign(ub=lambda x: x.uprun.clip(upper=3)).groupby("ub").apply(summ)
    out["slope_downs5_by_coin"] = d.groupby("coin").apply(lambda g: cl_slope(g.downs5, g.n1, g.day))
    return out
