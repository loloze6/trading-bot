def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    def tclust(vals, days):
        vals = pd.Series(np.asarray(vals, float)); days = pd.Series(np.asarray(days))
        n = len(vals); m = vals.mean()
        dev = (vals - m).groupby(days.values).sum()
        D = len(dev)
        if D < 3: return np.nan
        se = np.sqrt((dev**2).sum() * D/(D-1)) / n
        return m/se
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].values.astype(float); n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            ret1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            r30 = np.full(n, np.nan); r30[30:] = c[30:]/c[:-30]-1
            vol30 = pd.Series(ret1).rolling(30).std().values
            fc = df["forecast"].values.astype(float)
            al = df["postRebalance_current_allocation"].values.astype(float)
            for h in (5, 10):
                for t in range(0, n-h, h):
                    rows.append(dict(coin=coin, w=w, h=h, day=str(ts[t].date()), yr=ts[t].year,
                        fwd=c[t+h]/c[t]-1, r30=r30[t], z=r30[t]/(vol30[t]*np.sqrt(30)) if vol30[t]>0 else np.nan,
                        reg=df["regime"].iloc[t], fc=fc[t], al=al[t]))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby(["coin","h"])["fwd"].transform("mean"); R["un"] = R.fwd - R.drift
    C = R[(R.reg=="unknown")].dropna(subset=["r30"]).copy()
    out = {}
    res = []
    for h in (5,10):
        S = C[C.h==h]
        for yr, g in S.groupby("yr"):
            sp = stats.spearmanr(g.r30, g.un)
            dn = g[g.r30<0]; up = g[g.r30>=0]
            res.append(dict(h=h, yr=yr, n=len(g), rho=sp.correlation, un_dn=dn.un.mean(), t_dn=tclust(dn.un, dn.day),
                            un_up=up.un.mean(), t_up=tclust(up.un, up.day)))
        for w, g in S.groupby("w"):
            pass
    out["choppy by year"] = pd.DataFrame(res)
    res = []
    for h in (5,10):
        S = C[C.h==h]
        for side, g in [("down", S[S.r30<0]), ("up", S[S.r30>=0])]:
            g = g.copy(); g["q"] = pd.qcut(g.r30.abs(), 3, labels=False)
            for q, gg in g.groupby("q"):
                res.append(dict(h=h, side=side, q=q, r30=gg.r30.mean(), n=len(gg), un=gg.un.mean(), t=tclust(gg.un, gg.day)))
            sp = stats.spearmanr(g.r30, g.un)
            res.append(dict(h=h, side=side, q="rho", r30=np.nan, n=len(g), un=sp.correlation, t=sp.pvalue))
    out["choppy graded by side"] = pd.DataFrame(res)
    res = []
    for h in (5,10):
        S = C[C.h==h].dropna(subset=["z"]).copy()
        S["q"] = pd.qcut(S.z, 5, labels=False)
        for q, g in S.groupby("q"):
            res.append(dict(h=h, q=q, z=g.z.mean(), n=len(g), un=g.un.mean(), t=tclust(g.un, g.day)))
        sp = stats.spearmanr(S.z, S.un); res.append(dict(h=h, q="rho", n=len(S), un=sp.correlation, t=sp.pvalue))
    out["choppy vol-scaled r30"] = pd.DataFrame(res)
    S = C[C.h==10].copy()
    out["by coin h10 rho"] = S.groupby("coin").apply(lambda g: pd.Series(dict(n=len(g),
        rho=stats.spearmanr(g.r30, g.un).correlation if len(g)>5 else np.nan)))
    # book: positions vs r30 sign in choppy
    B = R[R.h==5].dropna(subset=["r30"]).copy()
    B["pos"] = np.sign(B.al.fillna(0))
    B["r30s"] = np.where(B.r30<0, "neg", "pos")
    out["book pos by regime and r30 sign"] = B.groupby(["reg","r30s","pos"]).agg(n=("un","count"), fwd=("fwd","mean"), un=("un","mean"))
    return out
