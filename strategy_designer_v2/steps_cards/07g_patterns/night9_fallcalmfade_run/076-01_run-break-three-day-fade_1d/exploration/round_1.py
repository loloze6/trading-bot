def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 3
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            o = b["open"].values.astype(float); hi = b["high"].values.astype(float); lo = b["low"].values.astype(float)
            n = len(c)
            r1 = np.full(n, np.nan); r1[1:] = c[1:]/c[:-1]-1
            # down run before (count strict down closes ending at t-1), up run before
            dn = np.zeros(n, int); up = np.zeros(n, int)
            for t in range(1, n):
                if r1[t] < 0: dn[t] = dn[t-1]+1; up[t] = 0
                elif r1[t] > 0: up[t] = up[t-1]+1; dn[t] = 0
            ts = pd.to_datetime(b["timestamp"])
            vol20 = pd.Series(r1).rolling(20, min_periods=15).std().values
            vol60 = pd.Series(r1).rolling(60, min_periods=40).std().values
            ret20 = np.full(n, np.nan); ret20[20:] = c[20:]/c[:-20]-1
            runret = np.full(n, np.nan)
            for t in range(0, n, H):
                if t+H >= n: break
                f = c[t+H]/c[t]-1
                prevdn = dn[t-1] if t >= 1 else 0
                prevup = up[t-1] if t >= 1 else 0
                rr = np.nan
                if t >= 1 and prevdn > 0 and t-1-prevdn >= 0:
                    rr = c[t-1]/c[t-1-prevdn]-1
                rows.append(dict(coin=coin, w=w, day=ts[t].normalize(), f=f, r1=r1[t],
                    prevdn=prevdn, prevup=prevup, dn=dn[t], up=up[t],
                    rng=(hi[t]-lo[t])/c[t], clv=(c[t]-lo[t])/(hi[t]-lo[t]) if hi[t]>lo[t] else np.nan,
                    zr=r1[t]/vol20[t] if vol20[t] else np.nan, vr=vol20[t]/vol60[t] if vol60[t] else np.nan,
                    ret20=ret20[t], runret=rr, wd=ts[t].dayofweek, alloc=b["postRebalance_current_allocation"].iloc[t]))
    d = pd.DataFrame(rows)
    drift = d.groupby("coin")["f"].mean()
    d["u"] = d["f"] - d["coin"].map(drift)
    def tday(x):
        g = x.groupby("day")["u"].sum(); nd = len(g)
        m = x["u"].mean(); se = np.sqrt((g**2).sum())/len(x) if len(x) else np.nan
        return pd.Series(dict(n=len(x), days=nd, mean_u=m, t=m/se if se else np.nan, mean_f=x["f"].mean()))
    out = {}
    d["brk"] = (d["r1"] > 0) & (d["prevdn"] >= 1)
    br = d[d.brk].copy()
    br["runc"] = br["prevdn"].clip(upper=5)
    out["break: raw return (long sign) by run length"] = br.groupby("runc").apply(tday)
    # mirror: down day ending up run
    dd = d[(d["r1"] < 0) & (d["prevup"] >= 1)].copy(); dd["runc"] = dd["prevup"].clip(upper=5)
    out["mirror: down day after up run, raw by run len"] = dd.groupby("runc").apply(tday)
    # ongoing runs: at t, current down run count (still falling)
    on = d[d["dn"] >= 1].copy(); on["runc"] = on["dn"].clip(upper=6)
    out["in down run (close down), raw by run len"] = on.groupby("runc").apply(tday)
    on2 = d[d["up"] >= 1].copy(); on2["runc"] = on2["up"].clip(upper=6)
    out["in up run, raw by run len"] = on2.groupby("runc").apply(tday)
    # break by size of run's fall (quintiles)
    b2 = br.dropna(subset=["runret"]).copy()
    b2["q"] = pd.qcut(b2["runret"], 5, labels=False)
    out["break by run cumulative fall quintile (0=deepest)"] = b2.groupby("q").apply(tday)
    br["zq"] = pd.qcut(br["zr"], 4, labels=False, duplicates="drop")
    out["break by up-day z quartile"] = br.groupby("zq").apply(tday)
    br["cq"] = pd.qcut(br["clv"], 4, labels=False, duplicates="drop")
    out["break by close location quartile"] = br.groupby("cq").apply(tday)
    # trend regime 20d
    d["tr"] = pd.cut(d["ret20"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    br["tr"] = d.loc[br.index, "tr"]
    out["break by 20d trend"] = br.groupby("tr").apply(tday)
    d["vq"] = pd.qcut(d["vr"], 3, labels=False, duplicates="drop")
    out["all bars: by daily z-return quintile"] = d.assign(q=pd.qcut(d["zr"], 5, labels=False)).groupby("q").apply(tday)
    out["all bars by weekday"] = d.groupby("wd").apply(tday)
    out["all bars by vol ratio tercile"] = d.groupby("vq").apply(tday)
    out["break by window"] = br.groupby("w").apply(tday)
    return out
