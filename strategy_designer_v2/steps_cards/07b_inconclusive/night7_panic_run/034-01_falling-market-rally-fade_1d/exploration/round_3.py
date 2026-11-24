def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3]
    drift, usual = {}, {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs)
    # coin-level median of 30-day swing across all its windows (proxy for the year's median, which windows are too short for)
    sdmed_coin = {}
    for c, ws in bars.items():
        vals = []
        for w, df in ws.items():
            vals += list(df["close"].pct_change().rolling(30).std().dropna())
        sdmed_coin[c] = np.median(vals)
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"]; r = cl.pct_change()
            sd = r.rolling(30).std(); z = r / sd
            sdexp = sd.expanding(min_periods=30).median()
            tr = (cl / cl.shift(60) - 1) * 100
            falling = np.where(tr.notna(), tr < -10, df["regime"] == "unknown")
            n = len(df)
            for h in H:
                for i in range(0, n - h, h):
                    if not (z.iloc[i] > 0) or not falling[i]: continue
                    fr = cl.iloc[i + h] / cl.iloc[i] - 1
                    rows.append(dict(coin=c, win=w, h=h, day=str(df["timestamp"].iloc[i])[:10],
                                     z=z.iloc[i],
                                     agitC=bool(sd.iloc[i] > sdmed_coin[c]) if pd.notna(sd.iloc[i]) else np.nan,
                                     agitE=bool(sd.iloc[i] > sdexp.iloc[i]) if pd.notna(sdexp.iloc[i]) else np.nan,
                                     su=-(fr - drift[(c, h)]), st=-(fr - drift[(c, h)]) / usual[(c, h)]))
    d = pd.DataFrame(rows)
    def ct(g, col="su"):
        g = g.dropna(subset=[col])
        if len(g) < 5: return pd.Series(dict(n=len(g), days=g["day"].nunique(), mean=np.nan, t=np.nan))
        m = g[col].mean(); dev = (g[col] - m).groupby(g["day"]).sum(); D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / len(g)
        return pd.Series(dict(n=len(g), days=D, mean=m, t=m / se if se > 0 else np.nan))
    def slope(g, x="z"):
        g = g.dropna(subset=[x, "su"])
        if len(g) < 10: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        res = stats.linregress(g[x], g["su"])
        return pd.Series(dict(n=len(g), slope=res.slope, t=res.slope / res.stderr))
    out = {}
    for a in ["agitC", "agitE"]:
        for h in H:
            dh = d[(d.h == h)].dropna(subset=[a]).copy()
            dh["zq"] = pd.qcut(dh.z, 4, labels=False)
            out[f"h{h}_{a}"] = dh.groupby(a).apply(ct)
            out[f"h{h}_{a}_strength"] = dh.groupby(a).apply(lambda g: ct(g, "st"))
            out[f"h{h}_{a}_slope"] = dh.groupby(a).apply(slope)
            out[f"h{h}_{a}_x_zhalf"] = dh.assign(top=dh.zq >= 2).groupby([a, "top"]).apply(ct)
    d3 = d[d.h == 3].dropna(subset=["agitC"])
    out["h3_agitC_by_win"] = d3[d3.agitC == True].groupby("win").apply(ct)
    out["h3_agitC_by_coin"] = d3[d3.agitC == True].groupby("coin").apply(ct)
    out["share_cases_agitC"] = d3.agitC.mean()
    return out
