def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    def build(H):
        rows = []
        for coin, wins in bars.items():
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].values.astype(float); n = len(c)
                r1 = np.full(n, np.nan); r1[1:] = c[1:]/c[:-1]-1
                dn = np.zeros(n, int)
                for t in range(1, n):
                    if r1[t] < 0: dn[t] = dn[t-1]+1
                ts = pd.to_datetime(b["timestamp"])
                vol20 = pd.Series(r1).rolling(20, min_periods=15).std().values
                for t in range(0, n, H):
                    if t+H >= n: break
                    pdn = dn[t-1] if t >= 1 else 0
                    rr = c[t-1]/c[t-1-pdn]-1 if (t >= 1 and pdn > 0 and t-1-pdn >= 0) else np.nan
                    tr60 = c[t]/c[t-60]-1 if t >= 60 else np.nan
                    rows.append(dict(coin=coin, w=w, day=ts[t].normalize(), yr=ts[t].year,
                        f=c[t+H]/c[t]-1, r1=r1[t], prevdn=pdn, runret=rr,
                        sdepth=rr/(vol20[t]) if vol20[t] else np.nan, tr60=tr60))
        d = pd.DataFrame(rows)
        d["u"] = d["f"] - d["coin"].map(d.groupby("coin")["f"].mean())
        return d
    def tday(x):
        g = x.groupby("day")["u"].sum(); m = x["u"].mean()
        se = np.sqrt((g**2).sum())/len(x) if len(x) else np.nan
        return pd.Series(dict(n=len(x), days=len(g), mean_u=m, t=m/se if se else np.nan))
    for H in [1, 3, 5]:
        d = build(H)
        br = d[(d.r1 > 0) & (d.prevdn >= 1)].dropna(subset=["runret"]).copy()
        br["q"] = pd.qcut(br["runret"], 5, labels=False)
        out[f"H{H} break by run fall quintile (0 deepest)"] = br.groupby("q").apply(tday)
        if H == 3:
            br["sq"] = pd.qcut(br["sdepth"], 5, labels=False, duplicates="drop")
            out["H3 break by vol-scaled run depth quintile"] = br.groupby("sq").apply(tday)
            br["cnt"] = br["prevdn"].clip(upper=3)
            br["deep"] = (br["q"] <= 1).astype(int)
            out["H3 break count x deep(q0-1)"] = br.groupby(["cnt", "deep"]).apply(tday)
            out["H3 deepest quintile by year"] = br[br.q == 0].groupby("yr").apply(tday)
            br["tr"] = pd.cut(br["tr60"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
            out["H3 break by 60d trend x deep"] = br.groupby(["tr", "deep"]).apply(tday)
            # cluster-robust regression of u on runret and prevdn
            X = np.column_stack([np.ones(len(br)), br["runret"].values, br["prevdn"].clip(upper=6).values])
            y = br["u"].values
            beta = np.linalg.lstsq(X, y, rcond=None)[0]; e = y - X @ beta
            XtXi = np.linalg.inv(X.T @ X)
            meat = np.zeros((3, 3))
            for _, idx in br.reset_index(drop=True).groupby("day").groups.items():
                s = (X[idx] * e[idx][:, None]).sum(0); meat += np.outer(s, s)
            se = np.sqrt(np.diag(XtXi @ meat @ XtXi))
            out["H3 regression u ~ runret + count (coef, t)"] = pd.DataFrame({"coef": beta, "t": beta/se}, index=["const", "runret", "count"])
            # down-day continuation: deep run still going (not broken)
            on = d[(d.r1 < 0)].copy()
            on["runret_incl"] = np.nan
    return out
