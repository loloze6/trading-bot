import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = 26
    rows = []
    for coin, wins in bars.items():
        # coin mean H-return over all windows on grid
        allret = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                allret.append(c[i + H] / c[i] - 1)
        mu = np.mean(allret)
        for w, b in wins.items():
            c = b["close"].values
            f = b["forecast"].values
            wn = int(str(w).lstrip("w"))
            yr = pd.to_datetime(b["timestamp"].iloc[0]).year
            # trend context: 52-day return before
            for i in range(0, len(c), H):
                if not (f[i] < 0):
                    continue
                r = {}
                for h in (5, 10, 26, 52):
                    r[h] = -(c[i + h] / c[i] - 1) if i + h < len(c) else np.nan
                past = c[i] / c[i - 26] - 1 if i >= 26 else np.nan
                rows.append(dict(coin=coin, w=wn, year=yr, f=f[i], mu=mu,
                                 tot26=r[26], ex26=(r[26] + mu) if not np.isnan(r[26]) else np.nan,
                                 tot5=r[5], tot10=r[10], tot52=r[52], past26=past))
    d = pd.DataFrame(rows)
    def summ(g):
        x = g["ex26"].dropna()
        t = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        y = g["tot26"].dropna()
        return pd.Series(dict(n=len(x), ex_mean=x.mean(), t=t, tot_mean=y.mean(),
                              hit=(x > 0).mean(), med=x.median()))
    out = {}
    out["all"] = summ(d)
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["fq"] = pd.qcut(d["f"].abs(), 4, labels=False, duplicates="drop")
    out["by_absf_quartile"] = d.groupby("fq").apply(summ)
    d["pq"] = pd.qcut(d["past26"], 4, labels=False, duplicates="drop")
    out["by_past26_quartile"] = d.groupby("pq").apply(summ)
    hz = {}
    for h in (5, 10, 26, 52):
        x = d[f"tot{h}"].dropna()
        hz[h] = dict(n=len(x), short_total_mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))))
    out["horizons_total_short"] = pd.DataFrame(hz).T
    out["coin_mu26"] = d.groupby("coin")["mu"].first()
    return out
