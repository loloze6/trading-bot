import numpy as np, pandas as pd
from scipy import stats

def ctt(df, col="fwd", cl="day"):
    # day-clustered t of the mean: per-day sums of deviations
    x = df[col].dropna(); d = df.loc[x.index, cl]
    m = x.mean(); s = (x - m).groupby(d).sum()
    G = len(s); n = len(x)
    if G < 3: return pd.Series(dict(n=n, days=G, mean=m, t=np.nan))
    se = np.sqrt((s**2).sum() * G/(G-1)) / n
    return pd.Series(dict(n=n, days=G, mean=m, t=m/se))

def explore(data):
    bars = data["bars"]
    drift = {}
    for coin, wins in bars.items():
        for h in (7, 14, 30):
            f = []
            for w, df in wins.items():
                c = df["close"].reset_index(drop=True)
                for p in range(0, len(c) - h, h):
                    f.append(c[p+h]/c[p]-1)
            drift[(coin, h)] = np.mean(f)
    rows = {7: [], 14: [], 30: []}
    rows1 = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True); c = d["close"]
            ts = pd.to_datetime(d["timestamp"]); day = ts.dt.floor("D")
            lr = np.log(c).diff(); vol30 = lr.rolling(30).std()
            vol90 = lr.rolling(90).std()
            r30 = c/c.shift(30)-1; r14 = c/c.shift(14)-1; r7 = c/c.shift(7)-1
            for h in (7, 14, 30):
                for p in range(0, len(c)-h, h):
                    v = vol30[p]
                    rows[h].append(dict(coin=coin, day=day[p], year=ts[p].year,
                        fwd=c[p+h]/c[p]-1-drift[(coin, h)],
                        z30=r30[p]/(v*np.sqrt(30)) if v > 0 else np.nan,
                        z14=r14[p]/(v*np.sqrt(14)) if v > 0 else np.nan,
                        z7=r7[p]/(v*np.sqrt(7)) if v > 0 else np.nan,
                        vr=vol30[p]/vol90[p] if vol90[p] > 0 else np.nan))
            r1 = c.pct_change()
            for p in range(1, len(c)):
                rows1.append(dict(day=day[p], wd=ts[p].dayofweek, r=r1[p]))
    out = {}
    for h in (7, 14):
        A = pd.DataFrame(rows[h]).dropna(subset=["z30"])
        A["q"] = pd.qcut(A["z30"], 5, labels=False)
        out[f"fwd{h} by past30 z quintile, day-clustered"] = A.groupby("q").apply(ctt)
        A["sz"] = A["z30"].clip(-3, 3)
        A["prod"] = (A["sz"] - A["sz"].mean()) * A["fwd"]
        out[f"fwd{h}: z30*fwd covariance, clustered"] = ctt(A, "prod")
        # per coin spearman
        sc = A.groupby("coin").apply(lambda g: stats.spearmanr(g["z30"], g["fwd"])[0])
        out[f"fwd{h} per-coin spearman z30 (n pos/total)"] = f"{(sc>0).sum()}/{len(sc)}, median {sc.median():.3f}"
        out[f"fwd{h} top-minus-bottom z30 quintile by year"] = A.groupby("year").apply(
            lambda g: g.loc[g.q == 4, "fwd"].mean() - g.loc[g.q == 0, "fwd"].mean())
    A7 = pd.DataFrame(rows[7]).dropna(subset=["z7"])
    A7["q"] = pd.qcut(A7["z7"], 5, labels=False)
    out["fwd7 by past7 z quintile, day-clustered"] = A7.groupby("q").apply(ctt)
    A30 = pd.DataFrame(rows[30]).dropna(subset=["z30"])
    A30["q"] = pd.qcut(A30["z30"], 5, labels=False)
    out["fwd30 by past30 z quintile, day-clustered"] = A30.groupby("q").apply(ctt)
    V = pd.DataFrame(rows[30]).dropna(subset=["vr"])
    V["q"] = pd.qcut(V["vr"], 3, labels=False)
    out["fwd30 by vol30/vol90 tercile, clustered"] = V.groupby("q").apply(ctt)
    C = pd.DataFrame(rows1).dropna()
    Cd = C.groupby(["day", "wd"])["r"].mean().reset_index()
    out["weekday: per-day cross-coin mean, t over days"] = Cd.groupby("wd")["r"].agg(
        ["count", "mean", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    return out
