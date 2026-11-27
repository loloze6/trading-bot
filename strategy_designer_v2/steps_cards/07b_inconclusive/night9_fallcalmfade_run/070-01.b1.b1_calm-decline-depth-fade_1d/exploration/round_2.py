import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        rets = [pd.Series(b["close"].astype(float).values).pct_change().dropna() for b in wins.values()]
        drift[coin] = pd.concat(rets).mean()
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            f = b["forecast"].astype(float).fillna(0).values
            ts = pd.to_datetime(b["timestamp"])
            r1 = pd.Series(c).pct_change()
            vol = r1.rolling(30, min_periods=15).std().values
            n = len(c)
            for t in range(1, n-2):
                if f[t] < 0 and (f[t] - min(f[t-1], 0)) <= -2:
                    k = t-1; run = 0
                    while k >= 1 and c[k] < c[k-1]:
                        run += 1; k -= 1
                    loss = c[k]/c[t-1]-1 if run > 0 else np.nan
                    tr30 = c[t]/c[t-30]-1 if t >= 30 else np.nan
                    rows.append(dict(coin=coin, day=ts[t].normalize(), f=f[t], run=run, loss=loss,
                                     lossv=loss/vol[t] if vol[t] > 0 else np.nan, tr30=tr30,
                                     u1=-(c[t+1]/c[t]-1-drift[coin]),
                                     u2=-(c[t+2]/c[t]-1-2*drift[coin]),
                                     tot1=-(c[t+1]/c[t]-1)))
    df = pd.DataFrame(rows)
    def tday(s, d):
        x = pd.DataFrame({"v": s, "d": d}).dropna()
        g = x.groupby("d")["v"].sum() - x.groupby("d")["v"].count()*x["v"].mean()
        D = len(g)
        se = np.sqrt((g**2).sum()*D/(D-1))/len(x)
        return dict(mean=x["v"].mean(), t=x["v"].mean()/se, n=len(x), days=D)
    res = {}
    for col in ("lossv", "tr30", "run"):
        q = pd.qcut(df[col].rank(method="first"), 4, labels=False)
        out = []
        for k in range(4):
            g = df[q == k]
            d1 = tday(g["u1"], g["day"]); d2 = tday(g["u2"], g["day"])
            out.append(dict(q=k, mean_x=g[col].mean(), u1=d1["mean"], t1=d1["t"], u2=d2["mean"], t2=d2["t"],
                            tot1=g["tot1"].mean(), n=d1["n"], days=d1["days"]))
        res[f"by_{col}_q"] = pd.DataFrame(out)
    x = df[["lossv", "u1"]].dropna()
    res["spearman_lossv_u1"] = str(stats.spearmanr(x["lossv"], x["u1"]))
    lq = pd.qcut(df["loss"].rank(method="first"), 2, labels=False)
    out = []
    for c_, g in df[lq == 1].groupby("coin"):
        d = tday(g["u1"], g["day"]); d["coin"] = c_; out.append(d)
    res["deep_half_by_coin"] = pd.DataFrame(out)
    return res
