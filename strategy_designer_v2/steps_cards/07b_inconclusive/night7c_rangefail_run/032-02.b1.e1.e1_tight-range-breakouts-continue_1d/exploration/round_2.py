import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = 20
    rows = []
    drift = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                allr.append(c[i + H] / c[i] - 1)
        drift[coin] = (np.mean(allr), np.std(allr, ddof=1))
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            fc = df["forecast"].values
            reg = df["regime"].values
            raw = df["debug_info.components.tight.last_history_value"].values if "debug_info.components.tight.last_history_value" in df else np.full(n, np.nan)
            post = df["debug_info.components.tight.post_pipeline_value"].values if "debug_info.components.tight.post_pipeline_value" in df else np.full(n, np.nan)
            for s in range(0, n, H):
                for i in range(s, min(s + H, n)):
                    if reg[i] == "trending" and fc[i] > 0:
                        if i + H >= n:
                            break
                        r = c[i + H] / c[i] - 1
                        d = dict(coin=coin, w=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                 day=str(pd.Timestamp(df["timestamp"].iloc[i]).floor("D")),
                                 fc=fc[i], raw=raw[i], post=post[i], ret=r, unus=r - drift[coin][0],
                                 strength=(r - drift[coin][0]) / drift[coin][1])
                        if i >= 20:
                            d["ret20"] = c[i] / c[i - 20] - 1
                        if i >= 1:
                            d["ret1"] = c[i] / c[i - 1] - 1
                        rows.append(d)
                        break
    X = pd.DataFrame(rows)
    out = {}
    out["raw_describe"] = X["raw"].describe()
    out["corr_raw_fc_spearman"] = stats.spearmanr(X["raw"], X["fc"], nan_policy="omit")[0]
    out["corr_raw_post_spearman"] = stats.spearmanr(X["raw"], X["post"], nan_policy="omit")[0]

    def clustered_slope_t(sub, f):
        x = sub[f].values; y = sub["unus"].values
        Xm = np.column_stack([np.ones(len(x)), x])
        b = np.linalg.lstsq(Xm, y, rcond=None)[0]
        e = y - Xm @ b
        XtXi = np.linalg.inv(Xm.T @ Xm)
        meat = np.zeros((2, 2))
        for _, idx in sub.reset_index(drop=True).groupby("day").groups.items():
            g = (Xm[idx] * e[idx][:, None]).sum(0)
            meat += np.outer(g, g)
        V = XtXi @ meat @ XtXi
        return b[1], b[1] / np.sqrt(V[1, 1]), len(sub), sub["day"].nunique()

    res = {}
    for f in ["fc", "raw", "post", "ret20", "ret1"]:
        sub = X.dropna(subset=[f, "unus"])
        if len(sub) > 10:
            sl, t, nn, nd = clustered_slope_t(sub, f)
            res[f] = {"slope": sl, "t_clust": t, "n": nn, "days": nd,
                      "spearman": stats.spearmanr(sub[f], sub["unus"])[0]}
    out["clustered_slopes"] = pd.DataFrame(res).T

    def summ(g):
        return pd.Series({"n": len(g), "unus_mean": g.unus.mean(),
                          "t": g.unus.mean() / (g.unus.std(ddof=1) / np.sqrt(len(g))),
                          "strength": g.strength.mean(), "hit": (g.ret > 0).mean(),
                          "raw_mean": g.raw.mean()})
    for f in ["raw", "ret20"]:
        sub = X.dropna(subset=[f])
        sub = sub.assign(q=pd.qcut(sub[f].rank(method="first"), 3, labels=["lo", "mid", "hi"]))
        out["tercile_" + f] = sub.groupby("q").apply(summ)
    sub = X.dropna(subset=["raw"])
    sub = sub.assign(q=pd.qcut(sub["raw"].rank(method="first"), 3, labels=["lo", "mid", "hi"]))
    out["raw_tercile_by_year"] = sub.groupby(["year", "q"]).unus.mean().unstack()
    out["raw_slope_by_year"] = sub.groupby("year").apply(lambda g: pd.Series({"n": len(g), "spearman": stats.spearmanr(g.raw, g.unus)[0] if len(g) > 5 else np.nan}))
    out["raw_slope_by_coin"] = sub.groupby("coin").apply(lambda g: pd.Series({"n": len(g), "spearman": stats.spearmanr(g.raw, g.unus)[0]}))
    return out
