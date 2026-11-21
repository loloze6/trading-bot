def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    recs = []
    for c in bars:
        fw = {h: [] for h in (24, 48, 120)}
        crecs = []
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True); cl = b["close"]
            r24 = cl/cl.shift(24)-1
            mab = r24.abs().rolling(720, min_periods=300).mean()
            surge = r24/mab
            p7 = cl.shift(24)/cl.shift(192)-1
            vol = cl.pct_change().rolling(720, min_periods=300).std()*np.sqrt(168)
            p7s = p7/vol
            yr = pd.to_datetime(b["timestamp"]).dt.year
            fwds = {h: cl.shift(-h)/cl-1 for h in (24, 48, 120)}
            for h in (24, 48, 120):
                fw[h] += list(fwds[h].iloc[::h].values)
            for g0 in range(0, len(b), 120):
                seg = list(range(g0, min(g0+120, len(b))))
                cond = (surge.iloc[seg] >= 3) & (p7.iloc[seg] < 0)
                if cond.any():
                    i = cond.idxmax()
                    rec = dict(coin=c, w=w, yr=yr[i], surge=surge[i], p7s=p7s[i])
                    for h in (24, 48, 120): rec[f"f{h}"] = fwds[h][i]
                    crecs.append(rec)
        for r in crecs:
            for h in (24, 48, 120): r[f"d{h}"] = np.nanmean(fw[h])
        recs += crecs
    df = pd.DataFrame(recs).dropna(subset=["f120", "p7s", "surge"])
    for h in (24, 48, 120):
        df[f"s{h}"] = -(df[f"f{h}"] - df[f"d{h}"])  # short-direction unusual
        df[f"t{h}"] = -df[f"f{h}"]                   # short-direction total
    def summ(g):
        o = {"n": len(g)}
        for h in (24, 48, 120):
            u = g[f"s{h}"].dropna()
            o[f"unus{h}_pct"] = u.mean()*100
            o[f"t_unus{h}"] = u.mean()/(u.std()/np.sqrt(len(u))) if len(u) > 2 else np.nan
            o[f"tot{h}_pct"] = g[f"t{h}"].mean()*100
        return pd.Series(o)
    df["depth"] = pd.qcut(df["p7s"], 2, labels=["deep", "shallow"])
    df["sz"] = pd.qcut(df["surge"], 2, labels=["bigsurge", "smallsurge"][::-1])
    out["depth_x_surge"] = df.groupby(["depth", "sz"]).apply(summ)
    df["dq"] = pd.qcut(df["p7s"], 4, labels=["deepest", "q2", "q3", "shallow"])
    out["by_depth_horizons"] = df.groupby("dq").apply(summ)
    out["by_year"] = df.groupby("yr").apply(summ)
    df["comb"] = df["p7s"].rank(pct=True) + (1 - df["surge"].rank(pct=True))
    df["cq"] = pd.qcut(df["comb"], 4, labels=["strongest", "q2", "q3", "weakest"])
    out["by_combined_strength"] = df.groupby("cq").apply(summ)
    from scipy import stats
    s = stats.linregress(-df["p7s"], df["s120"]); s2 = stats.linregress(df["surge"], df["s120"])
    out["slopes"] = pd.Series({"slope_depth": s.slope, "t_depth": s.slope/s.stderr,
                               "slope_surge": s2.slope, "t_surge": s2.slope/s2.stderr, "n": len(df)})
    return out
