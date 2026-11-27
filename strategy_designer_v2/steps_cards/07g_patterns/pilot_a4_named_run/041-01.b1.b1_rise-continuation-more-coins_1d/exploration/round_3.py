def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(c[1:]/c[:-1]-1)
        mu = np.nanmean(np.concatenate(allr))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            up = (r > 0).astype(int)
            streak = up.groupby((up != up.shift()).cumsum()).cumsum() * up
            run_ret = pd.Series(np.nan, index=b.index)
            # scaled return over the current up streak
            for i in range(len(b)):
                k = int(streak.iloc[i])
                if k > 0 and i - k >= 0:
                    run_ret.iloc[i] = (c.iloc[i]/c.iloc[i-k]-1)/(sd30.iloc[i]*np.sqrt(k)) if sd30.iloc[i] else np.nan
                elif k == 0:
                    run_ret.iloc[i] = 0.0
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for h in (1, 2, 3):
                fwd = c.shift(-h)/c - 1
                for i in range(0, len(b), h):
                    rows.append(dict(coin=coin, w=w, h=h, inprof=b["regime"].iloc[i] == "unknown",
                                     streak=streak.iloc[i], run=run_ret.iloc[i], yr=yr.iloc[i],
                                     day=pd.to_datetime(b["timestamp"].iloc[i]).normalize(),
                                     ex=fwd.iloc[i] - ((1+mu)**h - 1)))
    df = pd.DataFrame(rows).dropna(subset=["ex"])
    out = {}
    def summ(g):
        d = g.groupby("day")["ex"].sum()
        m = g["ex"].mean()
        se = np.sqrt((( (g["ex"]-m).groupby(g["day"]).sum())**2).sum())/len(g)
        return pd.Series(dict(n=len(g), days=g["day"].nunique(), mean=m, t_day=m/se if se > 0 else np.nan))
    for name, S in (("in", df[df.inprof]), ("out", df[~df.inprof])):
        for h in (1, 2, 3):
            s = S[S.h == h].copy()
            s["sb"] = s["streak"].clip(upper=4)
            out[f"streak bucket {name} h{h}"] = s.groupby("sb").apply(summ)
            ss = s.dropna(subset=["run"])
            rho, p = stats.spearmanr(ss["run"], ss["ex"])
            out[f"run spearman {name} h{h}"] = f"rho {rho:.3f} p {p:.3f} n {len(ss)}"
    s = df[(df.inprof) & (df.h == 1) & (df.streak >= 2)]
    out["streak>=2 in, by coin h1"] = s.groupby("coin").apply(summ)
    out["streak>=2 in, by year h1"] = s.groupby("yr").apply(summ)
    return out
