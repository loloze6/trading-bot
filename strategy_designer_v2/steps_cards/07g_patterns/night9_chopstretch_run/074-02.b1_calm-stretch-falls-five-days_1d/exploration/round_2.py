def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    def gm(coin, h):
        v = []
        for w, b in bars[coin].items():
            c = b["close"].values
            for i in range(0, len(c) - h, h):
                v.append(c[i + h] / c[i] - 1)
        return np.mean(v)
    def clus_t(x, y, d):
        X = np.column_stack([np.ones(len(x)), x])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        e = y - X @ beta
        XtX = np.linalg.inv(X.T @ X)
        df = pd.DataFrame({"d": d, "a": e, "b": e * x})
        S = df.groupby("d")[["a", "b"]].sum().values
        V = XtX @ (S.T @ S) @ XtX
        return beta[1], beta[1] / np.sqrt(V[1, 1]), len(np.unique(d))
    def mean_t(y, d):
        df = pd.DataFrame({"d": d, "y": y - y.mean()})
        s = df.groupby("d")["y"].sum().values
        se = np.sqrt((s ** 2).sum()) / len(y)
        return y.mean(), y.mean() / se
    recs = []
    for h in (1, 2, 5, 10):
        for coin in bars:
            g = gm(coin, h)
            for w, b in bars[coin].items():
                b = b.reset_index(drop=True)
                c = b["close"]; r = c.pct_change()
                sma = c.rolling(20).mean(); sd = r.rolling(20).std()
                st = (c - sma) / (sma * sd)
                z1 = r / sd
                tr = c / c.shift(60) - 1
                ag = (b["regime"] == "chop").astype(int)
                fc = b["forecast"]
                day = pd.to_datetime(b["timestamp"]).dt.floor("D").astype("int64")
                cv = c.values
                for i in range(0, len(cv) - h, h):
                    recs.append(dict(coin=coin, w=w, h=h, st=st.iloc[i], z1=z1.iloc[i], tr=tr.iloc[i],
                                     ag=ag.iloc[i], fc=fc.iloc[i], day=day.iloc[i],
                                     y=cv[i + h] / cv[i] - 1 - g))
    D = pd.DataFrame(recs)
    D["trend"] = np.where(D.tr > 0.1, "rising", np.where(D.tr < -0.1, "falling", np.where(D.tr.notna(), "choppy", "na")))
    out = {}
    res = []
    for h in (1, 2, 5, 10):
        for ag in (0, 1):
            for var, side in [("st", "below"), ("st", "above"), ("st", "all"), ("z1", "down"), ("z1", "up"), ("z1", "all")]:
                g = D[(D.h == h) & (D.ag == ag)].dropna(subset=[var])
                g = g[np.isfinite(g[var])]
                if side in ("below", "down"): g = g[g[var] < 0]
                if side in ("above", "up"): g = g[g[var] > 0]
                if len(g) < 60: continue
                s, t, nd = clus_t(g[var].values, g.y.values, g.day.values)
                res.append(dict(h=h, ag=ag, var=var, side=side, n=len(g), days=nd, slope=round(s, 5), t_clu=round(t, 2)))
    out["clustered_slopes"] = pd.DataFrame(res)
    # agitated, up-day z1 next 1-2 days, by trend
    res = []
    for h in (1, 2):
        for trd in ["rising", "choppy", "falling"]:
            for side in ["up", "down"]:
                g = D[(D.h == h) & (D.ag == 1) & (D.trend == trd)].dropna(subset=["z1"])
                g = g[g.z1 > 0] if side == "up" else g[g.z1 < 0]
                if len(g) < 40: continue
                s, t, nd = clus_t(g.z1.values, g.y.values, g.day.values)
                m, mt = mean_t(g.y.values, g.day.values)
                res.append(dict(h=h, trend=trd, side=side, n=len(g), slope=round(s, 5), t_clu=round(t, 2), mean=round(m, 4), mean_t=round(mt, 2)))
    out["agit_z1_by_trend"] = pd.DataFrame(res)
    # agitated up-day z1 h=1 by window: slope sign
    g = D[(D.h == 1) & (D.ag == 1) & (D.z1 > 0)].dropna(subset=["z1"])
    out["agit_up_by_window"] = g.groupby("w").apply(lambda x: pd.Series({"n": len(x), "rho": stats.spearmanr(x.z1, x.y)[0]})).round(3)
    # calm stretch below, h5, by window, and forecast vs raw
    g = D[(D.h == 5) & (D.ag == 0)].dropna(subset=["st"])
    out["calm_st_by_window_h5"] = g.groupby("w").apply(lambda x: pd.Series({"n": len(x), "rho": stats.spearmanr(x.st, x.y)[0]})).round(3)
    gf = g[g.fc < 0]
    if len(gf) > 50:
        s, t, nd = clus_t(-gf.fc.values, gf.y.values, gf.day.values)
        s2, t2, _ = clus_t(gf.st.values, gf.y.values, gf.day.values)
        out["calm_short_cases_fc_vs_raw"] = pd.Series({"n": len(gf), "slope_depth_fc": s, "t_fc": t, "slope_raw_st": s2, "t_raw_st": t2}).round(4)
    # calm stretch by trend, h5, all sides
    res = []
    for trd in ["rising", "choppy", "falling"]:
        gg = g[g.trend == trd]
        if len(gg) < 50: continue
        s, t, nd = clus_t(gg.st.values, gg.y.values, gg.day.values)
        res.append(dict(trend=trd, n=len(gg), slope=round(s, 5), t_clu=round(t, 2)))
    out["calm_st_by_trend_h5"] = pd.DataFrame(res)
    return out
