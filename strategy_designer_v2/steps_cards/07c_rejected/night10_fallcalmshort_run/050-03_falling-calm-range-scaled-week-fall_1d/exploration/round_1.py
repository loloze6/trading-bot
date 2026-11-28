def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in [1, 3, 5, 10]:
            vals = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                vals += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(vals)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            rr = ((df["high"] - df["low"]) / df["close"]).rolling(30).mean()
            r7 = c / c.shift(7) - 1
            sc = r7 / rr
            fc = df["forecast"]
            reg = df["regime"]
            n = len(df)
            for h in [1, 3, 5, 10]:
                for i in range(0, n - h, h):
                    fwd = c.iloc[i + h] / c.iloc[i] - 1
                    rows.append(dict(coin=coin, w=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                     h=h, pos=i, fwd=fwd, unus=fwd - drift[(coin, h)],
                                     sc=sc.iloc[i], r7=r7.iloc[i], fc=fc.iloc[i],
                                     fc_prof=(reg.iloc[i] == "unknown"),
                                     day=str(df["timestamp"].iloc[i])[:10]))
    R = pd.DataFrame(rows)
    out["profile share by coin"] = R[R.h == 1].groupby("coin")["fc_prof"].mean()

    def summ(g):
        s = -g["unus"]  # short direction
        d = g.assign(s=s).groupby("day")["s"].sum()
        t = d.mean() / (d.std(ddof=1) / np.sqrt(len(d))) if len(d) > 2 else np.nan
        return pd.Series(dict(n=len(g), days=len(d), short_unus_mean=s.mean(), t_day=t,
                              short_total=(-g["fwd"]).mean()))

    P = R[R.fc_prof & R.sc.notna()].copy()
    # graded: by quintile of scaled 7d return (falls and rises), per horizon
    res = []
    for h in [1, 3, 5, 10]:
        G = P[P.h == h].copy()
        G["q"] = pd.qcut(G["sc"], 5, labels=False)
        for q, g in G.groupby("q"):
            s = summ(g)
            s["h"] = h; s["q"] = q; s["sc_mean"] = g["sc"].mean()
            res.append(s)
    out["profile: short unusual by scaled-7d quintile and horizon"] = pd.DataFrame(res).round(4)
    # correlations scaled vs fwd per horizon (short direction negative corr = continuation)
    cr = []
    for h in [1, 3, 5, 10]:
        G = P[P.h == h]
        r, p = stats.spearmanr(G["sc"], G["unus"])
        Gf = G[G.sc < 0]
        r2, p2 = stats.spearmanr(Gf["sc"], Gf["unus"]) if len(Gf) > 5 else (np.nan, np.nan)
        cr.append(dict(h=h, n=len(G), rho_all=r, p_all=p, n_falls=len(Gf), rho_falls=r2, p_falls=p2))
    out["profile: spearman scaled vs unusual fwd"] = pd.DataFrame(cr).round(4)
    # forecast<0 cases at h=3 by coin, year, window
    F = P[(P.h == 3) & (P.fc < 0)]
    out["fc<0 h3 by coin"] = F.groupby("coin").apply(summ).round(4)
    out["fc<0 h3 by year"] = F.groupby("year").apply(summ).round(4)
    out["fc<0 by horizon"] = pd.DataFrame({h: summ(P[(P.h == h) & (P.fc < 0)]) for h in [1, 3, 5, 10]}).T.round(4)
    # outside profile: falls
    O = R[(~R.fc_prof) & (R.sc < 0)]
    out["outside profile falls by horizon"] = pd.DataFrame({h: summ(O[O.h == h]) for h in [1, 3, 5, 10]}).T.round(4)
    return out
