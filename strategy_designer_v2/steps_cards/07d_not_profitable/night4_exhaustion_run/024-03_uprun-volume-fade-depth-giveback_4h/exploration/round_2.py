import numpy as np, pandas as pd

def explore(data):
    H = 18
    rows = []; barstat = []
    for coin, wins in data["bars"].items():
        g = []
        for w, b in wins.items():
            c = b["close"].values; idx = np.arange(0, len(c) - H, H)
            g += list(c[idx + H] / c[idx] - 1)
        drift = np.mean(g)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(c)
            f = b["forecast"].fillna(0).values
            a = b["postRebalance_current_allocation"].values
            s = pd.Series(c)
            r60 = s.pct_change(360).values
            r30 = s.pct_change(180).values
            ma = s.rolling(180).mean().values
            dev = c / ma - 1
            fr = np.full(n, np.nan); fr[:n-H] = c[H:] / c[:n-H] - 1
            g1 = np.r_[c[1:] / c[:-1] - 1, np.nan]
            barstat.append(pd.DataFrame(dict(coin=coin, f_neg=f < 0, f_zero=f == 0, a_neg=a < -0.01, a=a,
                                             gain=a * g1, dev=dev, r60=r60)))
            seen = set()
            for i in range(n):
                cl = i // H
                if f[i] <= -2 and cl not in seen and not np.isnan(fr[i]):
                    seen.add(cl)
                    rows.append(dict(un=-(fr[i] - drift), r60=r60[i], r30=r30[i], dev=dev[i]))
    R = pd.DataFrame(rows); S = pd.concat(barstat)
    def summ(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), un18=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x)))))
    out = {}
    out["bars_state"] = pd.Series(dict(share_forecast_neg=S.f_neg.mean(), share_forecast_zero=S.f_zero.mean(),
                                       share_alloc_short=S.a_neg.mean(),
                                       share_alloc_short_when_f0=S.loc[S.f_zero, "a_neg"].mean(),
                                       mean_alloc_when_f0=S.loc[S.f_zero, "a"].mean(),
                                       mean_bar_gain_f0=S.loc[S.f_zero, "gain"].mean(),
                                       mean_bar_gain_fneg=S.loc[S.f_neg, "gain"].mean()))
    for k in ("r60", "r30", "dev"):
        q = pd.qcut(R[k], 5, labels=False)
        out["cases_by_" + k] = R.groupby(q)["un"].apply(summ).unstack()
    S2 = S.dropna(subset=["dev", "gain"])
    out["book_bar_gain_by_dev_quintile"] = S2.groupby(pd.qcut(S2.dev, 5, labels=False))["gain"].agg(["mean", "count"])
    return out
