def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    H = [1, 3, 5, 10]
    rows = []
    coinmean = {}
    for coin, wins in bars.items():
        allr = {h: [] for h in H}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            for h in H:
                idx = np.arange(0, n - h, h)
                allr[h].extend(list(c[idx + h] / c[idx] - 1))
        coinmean[coin] = {h: np.mean(allr[h]) if allr[h] else np.nan for h in H}
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            dr = c.pct_change()
            r7 = c / c.shift(7) - 1
            sd = dr.rolling(30, min_periods=20).std()
            sc = r7 / (sd * np.sqrt(7))
            r1 = dr
            n = len(df)
            for i in range(0, n - 10, 5):
                rec = dict(coin=coin, win=w, day=str(df["timestamp"].iloc[i])[:10],
                           year=str(df["timestamp"].iloc[i])[:4],
                           inprof=df["regime"].iloc[i] == "unknown",
                           fc=df["forecast"].iloc[i], sc=sc.iloc[i], r7=r7.iloc[i], r1=r1.iloc[i])
                for h in H:
                    rec[f"x{h}"] = c.iloc[i + h] / c.iloc[i] - 1 - coinmean[coin][h]
                    rec[f"t{h}"] = c.iloc[i + h] / c.iloc[i] - 1
                rows.append(rec)
    d = pd.DataFrame(rows).dropna(subset=["sc"])
    p = d[d.inprof].copy()
    out["n in profile / all"] = f"{len(p)} / {len(d)}"
    def ct(s, days):
        g = pd.DataFrame({"v": s.values, "d": days.values}).groupby("d")["v"].sum()
        n = len(s)
        if n < 3: return np.nan
        se = np.sqrt((g - g.mean() * 0 - s.mean() * pd.DataFrame({"d": days.values}).groupby("d").size()).pow(2).sum()) / n
        return s.mean() / se if se > 0 else np.nan
    p["q"] = pd.qcut(p["sc"], 5, labels=False)
    tab = []
    for q, g in p.groupby("q"):
        r = dict(q=q, n=len(g), sc_mean=g.sc.mean())
        for h in H:
            r[f"x{h}"] = g[f"x{h}"].mean(); r[f"t{h}"] = ct(g[f"x{h}"], g["day"])
        tab.append(r)
    out["profile: scaled 7d quintile -> excess fwd"] = pd.DataFrame(tab).round(4)
    tab = []
    for h in H:
        tab.append(dict(h=h, rho=stats.spearmanr(p.sc, p[f"x{h}"])[0],
                        slope=np.polyfit(p.sc, p[f"x{h}"], 1)[0],
                        rho_neg_only=stats.spearmanr(p[p.sc < 0].sc, p[p.sc < 0][f"x{h}"])[0],
                        rho_pos_only=stats.spearmanr(p[p.sc > 0].sc, p[p.sc > 0][f"x{h}"])[0]))
    out["profile: rank corr scaled vs excess"] = pd.DataFrame(tab).round(4)
    tab = []
    for (cn, s), g in p.groupby(["coin", p.sc > 0]):
        r = dict(coin=cn, rise=s, n=len(g))
        for h in [3, 5, 10]:
            r[f"x{h}"] = g[f"x{h}"].mean(); r[f"t{h}"] = ct(g[f"x{h}"], g["day"])
        tab.append(r)
    out["profile: by coin and sign"] = pd.DataFrame(tab).round(4)
    tab = []
    for (y, s), g in p.groupby(["year", p.sc > 0]):
        tab.append(dict(year=y, rise=s, n=len(g), x5=g.x5.mean(), x10=g.x10.mean()))
    out["profile: by year and sign"] = pd.DataFrame(tab).round(4)
    o = d[~d.inprof].copy()
    o["q"] = pd.qcut(o["sc"], 5, labels=False)
    tab = []
    for q, g in o.groupby("q"):
        tab.append(dict(q=q, n=len(g), sc=g.sc.mean(), x5=g.x5.mean(), t5=ct(g.x5, g.day), x10=g.x10.mean()))
    out["out of profile: quintile -> excess"] = pd.DataFrame(tab).round(4)
    # 1-day fall within profile
    p["q1"] = pd.qcut(p["r1"], 5, labels=False)
    tab = []
    for q, g in p.groupby("q1"):
        tab.append(dict(q=q, n=len(g), r1=g.r1.mean(), x3=g.x3.mean(), t3=ct(g.x3, g.day), x5=g.x5.mean(), t5=ct(g.x5, g.day)))
    out["profile: last-day return quintile -> excess"] = pd.DataFrame(tab).round(4)
    return out
