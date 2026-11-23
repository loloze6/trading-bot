def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    def grid_rows(h):
        rows = []
        for coin, wins in bars.items():
            allr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                allr.extend(list(c[idx + h] / c[idx] - 1))
            mu = np.mean(allr)
            for w, df in wins.items():
                c = df["close"].values
                f = df["forecast"].values
                for i in range(0, len(c) - h, h):
                    r20 = c[i] / c[i - 20] - 1 if i >= 20 else np.nan
                    r60 = c[i] / c[i - 60] - 1 if i >= 60 else np.nan
                    r90 = c[i] / c[i - 90] - 1 if i >= 90 else np.nan
                    hi90 = c[max(0, i - 89):i + 1].max() if i >= 89 else np.nan
                    rows.append(dict(coin=coin, w=w, f=f[i], ret=c[i + h] / c[i] - 1, mu=mu,
                                     r20=r20, r60=r60, r90=r90, near=c[i] / hi90 if hi90 == hi90 else np.nan))
        d = pd.DataFrame(rows)
        d["ex"] = d["ret"] - d["mu"]
        d["fx"] = d["f"] * d["ex"]
        return d
    def tt(x):
        x = pd.Series(x).dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    d = grid_rows(5)
    a = d[d.f > 0].dropna(subset=["r60"]).copy()
    a["r60q"] = pd.qcut(a.r60.rank(method="first"), 4, labels=False)
    out["fpos_by_r60_quartile"] = a.groupby("r60q").apply(lambda g: pd.Series({"r60": g.r60.mean(), **tt(g.ex).to_dict(), "fx_t": tt(g.fx)["t"]}))
    p = a[a.r60 > 0]
    out["fpos_r60pos_corr_f_ex"] = pd.Series({"n": len(p), "rho": stats.spearmanr(p.f, p.ex)[0]})
    out["fpos_r60pos_fx"] = tt(p.fx).to_frame().T
    # all bars with r20>0: r60 grading regardless of forecast
    b = d[(d.r20 > 0)].dropna(subset=["r60"]).copy()
    b["r60q"] = pd.qcut(b.r60.rank(method="first"), 4, labels=False)
    out["r20pos_all_by_r60q"] = b.groupby("r60q").apply(lambda g: pd.Series({"r60": g.r60.mean(), **tt(g.ex).to_dict()}))
    out["r20pos_all_by_r60q_fflag"] = b.groupby(["r60q", b.f > 0]).ex.agg(["count", "mean"])
    return out
