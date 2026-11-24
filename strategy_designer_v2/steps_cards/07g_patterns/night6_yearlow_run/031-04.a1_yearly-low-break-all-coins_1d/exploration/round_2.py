def explore(data):
    import numpy as np, pandas as pd

    def ct(x, days):
        x = np.asarray(x, float); m = x.mean(); e = x - m
        S = pd.Series(e).groupby(np.asarray(days)).sum()
        G = len(S)
        if G < 2: return np.nan
        se = np.sqrt((S ** 2).sum()) / len(x) * np.sqrt(G / (G - 1))
        return m / se

    def build(H, off=0):
        rows = []
        for coin, ws in data["bars"].items():
            for w, df in ws.items():
                df = df.sort_values("timestamp")
                s = pd.Series(df["close"].astype(float).values)
                lo = pd.Series(df["low"].astype(float).values)
                hi = pd.Series(df["high"].astype(float).values)
                n = len(s)
                ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
                r1 = s.pct_change()
                v20 = r1.rolling(20).std().shift(1)
                z1 = r1 / v20
                low_w = s.expanding().min().shift(1)
                f = pd.DataFrame({"ret1": r1, "z1": z1, "ret2": s / s.shift(2) - 1,
                                  "dlowexp": s / low_w - 1,
                                  "dlow120": s / s.rolling(120, min_periods=60).min().shift(1) - 1,
                                  "vol20": v20,
                                  "brk": (df["regime"].values == "mean_reversion").astype(int)})
                for i in range(off, n - H, H):
                    d = f.iloc[i].to_dict()
                    d.update(coin=coin, wn=int(w[1:]), day=ts[i].normalize(), fwd=s[i + H] / s[i] - 1)
                    rows.append(d)
        g = pd.DataFrame(rows)
        st = g.groupby("coin")["fwd"].agg(["mean", "std"])
        g["un"] = g["fwd"] - g["coin"].map(st["mean"])
        g["strg"] = g["un"] / g["coin"].map(st["std"])
        return g

    def bins(g, col, k):
        x = g.dropna(subset=[col]).copy()
        x["q"] = x.groupby("coin")[col].rank(pct=True)
        x["q"] = pd.cut(x["q"], np.linspace(0, 1, k + 1), labels=list(range(1, k + 1)))
        out = []
        for q, y in x.groupby("q", observed=True):
            out.append(dict(q=q, feat=y[col].mean(), un=y.un.mean(), strength=y.strg.mean(),
                            t=ct(y.un, y.day), n=len(y), days=y.day.nunique(),
                            early=y[y.wn <= 12].un.mean(), late=y[y.wn > 12].un.mean()))
        return pd.DataFrame(out)

    res = {}
    g10 = build(10)
    res["dec_ret1_H10"] = bins(g10, "ret1", 10)
    res["quint_z1_H10"] = bins(g10, "z1", 5)
    res["quint_ret2_H10"] = bins(g10, "ret2", 5)
    res["quint_dlowexp_H10"] = bins(g10, "dlowexp", 5)
    res["quint_dlow120_H10"] = bins(g10, "dlow120", 5)
    # grading inside the bottom ret1 quintile: correlation of ret1 with un
    x = g10.dropna(subset=["ret1"]).copy()
    x["pr"] = x.groupby("coin")["ret1"].rank(pct=True)
    b = x[x.pr <= 0.2]
    res["q1_ret1_vs_un_spearman"] = float(b[["ret1", "un"]].corr(method="spearman").iloc[0, 1])
    # bottom ret1 quintile by vol tercile
    b = b.copy(); b["vt"] = pd.qcut(b["vol20"].rank(method="first"), 3, labels=[1, 2, 3])
    res["q1_ret1_by_volterc"] = b.groupby("vt", observed=True).apply(
        lambda y: pd.Series(dict(un=y.un.mean(), t=ct(y.un, y.day), n=len(y))))
    res["q1_ret1_by_coin"] = b.groupby("coin").apply(lambda y: pd.Series(dict(un=y.un.mean(), n=len(y)))).round(4)
    # robustness over grid offsets and horizons
    rob = []
    for H in [3, 5, 10, 20]:
        for off in ([0, 3, 6] if H >= 10 else [0, 1, 2]):
            g = build(H, off)
            y = g.dropna(subset=["ret1"]).copy()
            y["pr"] = y.groupby("coin")["ret1"].rank(pct=True)
            lo = y[y.pr <= 0.2]; rest = y[y.pr > 0.2]
            rob.append(dict(H=H, off=off, un_q1=lo.un.mean(), t_q1=ct(lo.un, lo.day), n=len(lo),
                            strength_q1=lo.strg.mean(), un_rest=rest.un.mean(),
                            corr_ret1_un=y[["ret1", "un"]].corr(method="spearman").iloc[0, 1]))
    res["robust_ret1_q1"] = pd.DataFrame(rob)
    return res
