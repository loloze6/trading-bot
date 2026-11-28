def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].values.astype(float); n = len(c)
            r1 = np.full(n, np.nan); r1[1:] = c[1:] / c[:-1] - 1
            inprof = (df["regime"].astype(str) != "chop").values
            prevrun = np.zeros(n, int); prevcum = np.zeros(n); dr = 0; dc = 0.0
            for i in range(1, n):
                prevrun[i] = dr; prevcum[i] = dc
                if r1[i] < 0: dr += 1; dc += np.log(1 + r1[i])
                else: dr = 0; dc = 0.0
            sd30 = pd.Series(r1).rolling(30, min_periods=20).std().values
            p5 = np.full(n, np.nan); p5[5:] = c[5:] / c[:-5] - 1
            p3 = np.full(n, np.nan); p3[3:] = c[3:] / c[:-3] - 1
            for i in range(n):
                s = sd30[i] if sd30[i] > 0 else np.nan
                d = dict(coin=coin, w=w, pos=i, inprof=inprof[i],
                         first_up=bool(r1[i] > 0 and prevrun[i] >= 1), prun=prevrun[i],
                         upmove=r1[i] / s, depth=-prevcum[i] / s,
                         recov=(np.log(1 + r1[i]) / -prevcum[i]) if prevrun[i] >= 1 and r1[i] > 0 else np.nan,
                         past5=p5[i] / s, past3=p3[i] / s, up=r1[i] / s,
                         year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                         day=str(pd.Timestamp(df["timestamp"].iloc[i]).date()))
                for h in [2, 3, 5]:
                    d[f"f{h}"] = c[i+h] / c[i] - 1 if i + h < n else np.nan
                rows.append(d)
    A = pd.DataFrame(rows)
    for h in [2, 3, 5]:
        g = A[A.pos % h == 0]
        A[f"u{h}"] = A[f"f{h}"] - A.coin.map(g.groupby("coin")[f"f{h}"].mean())
    def cases(mask, h):
        s = A[mask & A[f"u{h}"].notna()].copy(); s["cell"] = s.pos // h
        return s.drop_duplicates(["coin", "w", "cell"])
    def tclust(s, h):
        m = s[f"u{h}"].mean(); dev = (s[f"u{h}"] - m).groupby(s.day).sum()
        nd = len(dev); se = np.sqrt((dev**2).sum()) / len(s) * np.sqrt(nd / max(nd-1, 1))
        return m, m / se, nd
    def slope(s, x, h):
        s = s[[x, f"u{h}", "day"]].dropna()
        X = s[x] - s[x].mean(); b = (X * s[f"u{h}"]).sum() / (X**2).sum()
        res = s[f"u{h}"] - s[f"u{h}"].mean() - b * X
        sc = (X * res).groupby(s.day).sum()
        se = np.sqrt((sc**2).sum()) / (X**2).sum()
        return pd.Series(dict(n=len(s), slope=b, t=b / se, corr=np.corrcoef(s[x], s[f"u{h}"])[0, 1]))
    P = A.inprof; ev = P & A.first_up
    out = {}
    res = {}
    for x in ["upmove", "recov", "depth", "past5", "past3"]:
        for h in [2, 3, 5]:
            res[(x, h)] = slope(cases(ev, h), x, h)
    out["slopes_in_events"] = pd.DataFrame(res).T
    res = {}
    for x in ["past5", "past3", "up"]:
        for h in [2, 3, 5]:
            res[(x, h)] = slope(cases(P, h), x, h)
    out["slopes_all_profile"] = pd.DataFrame(res).T
    # big up day events: by coin / year
    q = A.loc[ev, "upmove"].quantile(2/3)
    s = cases(ev & (A.upmove > q), 3)
    out["bigup_h3_coin"] = s.groupby("coin")["u3"].agg(["count", "mean"])
    out["bigup_h3_year"] = s.groupby("year")["u3"].agg(["count", "mean"])
    out["bigup_h3_overall"] = pd.Series(dict(zip(["mean", "t", "days"], tclust(s, 3))))
    s = cases(ev & (A.upmove <= q), 3)
    out["rest_h3_overall"] = pd.Series(dict(zip(["mean", "t", "days"], tclust(s, 3))))
    # upmove quintile within events, h3
    qq = A.loc[ev, "upmove"].quantile([.25, .5, .75]).values; b = [-np.inf] + list(qq) + [np.inf]
    res = {}
    for j in range(4):
        for h in [2, 3, 5]:
            s = cases(ev & (A.upmove > b[j]) & (A.upmove <= b[j+1]), h)
            m, t, nd = tclust(s, h); res[(f"q{j+1}", h)] = dict(n=len(s), mean=m, t=t)
    out["upmove_quartile_events"] = pd.DataFrame(res).T
    # past5 top quintile by coin/year h2
    q5 = A.loc[P, "past5"].quantile(.8)
    s = cases(P & (A.past5 > q5), 2)
    out["past5top_h2_coin"] = s.groupby("coin")["u2"].agg(["count", "mean"])
    out["past5top_h2_year"] = s.groupby("year")["u2"].agg(["count", "mean"])
    return out
