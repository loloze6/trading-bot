import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        rets = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            rets.append(pd.Series(c).pct_change().dropna())
        drift[coin] = pd.concat(rets).mean() if rets else np.nan
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            f = b["forecast"].astype(float).fillna(0).values
            ts = pd.to_datetime(b["timestamp"])
            n = len(c)
            for t in range(1, n):
                prevf = f[t-1]
                if f[t] < 0 and (f[t] - min(prevf, 0)) <= -2:
                    # run length & loss
                    k = t - 1; run = 0
                    while k >= 1 and c[k] < c[k-1]:
                        run += 1; k -= 1
                    start = c[k]; low = c[t-1]
                    loss = (start/low - 1) if run > 0 else np.nan
                    bounce = c[t]/c[t-1]-1
                    r = {}
                    for h in (1, 2, 3, 5):
                        r[h] = -(c[t+h]/c[t]-1 - h*drift[coin]) if t+h < n else np.nan
                    rows.append(dict(coin=coin, w=w, year=ts[t].year, wd=ts[t].weekday(),
                                     day=ts[t].normalize(), f=f[t], run=run, loss=loss,
                                     bounce=bounce, u1=r[1], u2=r[2], u3=r[3], u5=r[5]))
    df = pd.DataFrame(rows)
    def tday(s, d):
        x = pd.DataFrame({"v": s, "d": d}).dropna()
        g = x.groupby("d")["v"].sum() - x.groupby("d")["v"].count()*x["v"].mean()
        D = len(g)
        se = np.sqrt((g**2).sum()*D/(D-1))/len(x) if D > 1 else np.nan
        return x["v"].mean(), x["v"].mean()/se, len(x), D
    def summ(gcol):
        out = []
        for k, g in df.groupby(gcol):
            m, t, n, D = tday(g["u1"], g["day"])
            out.append(dict(key=k, mean=m, t=t, n=n, days=D))
        return pd.DataFrame(out)
    res = {}
    allr = []
    for h in ("u1", "u2", "u3", "u5"):
        m, t, n, D = tday(df[h], df["day"])
        allr.append(dict(h=h, mean=m, t=t, n=n, days=D))
    res["horizons"] = pd.DataFrame(allr)
    res["by_coin"] = summ("coin")
    res["by_year"] = summ("year")
    res["by_window"] = summ("w")
    df["runb"] = df["run"].clip(upper=5)
    res["by_run"] = summ("runb")
    df["lossq"] = pd.qcut(df["loss"], 4, labels=False, duplicates="drop")
    res["by_lossq"] = summ("lossq")
    res["lossq_mean_loss"] = df.groupby("lossq")["loss"].mean()
    df["bq"] = pd.qcut(df["bounce"], 4, labels=False, duplicates="drop")
    res["by_bounceq"] = summ("bq")
    df["fq"] = pd.qcut(df["f"].abs(), 4, labels=False, duplicates="drop")
    res["by_fq"] = summ("fq")
    res["by_weekday"] = summ("wd")
    for h in ("u1","u3"):
        x = df[["loss",h]].dropna()
        res[f"spearman_loss_{h}"] = str(stats.spearmanr(x["loss"], x[h]))
    return res
