import numpy as np, pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for H in [3, 5, 10]:
            pass
        allf = {H: [] for H in [3, 5, 10]}
        for w, b in wins.items():
            c = b.reset_index(drop=True)["close"]
            for H in allf:
                allf[H].append((c.shift(-H) / c - 1).iloc[::H].dropna())
        drift = {H: pd.concat(allf[H]).mean() for H in allf}
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c, h, l = b["close"], b["high"], b["low"]
            rr = (h - l) / c
            mr = rr.rolling(30, min_periods=10).mean()
            sd = c.pct_change().rolling(30, min_periods=10).std()
            base = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "fc": (b["regime"] == "unknown"),
                "s7": (c / c.shift(7) - 1) / mr,
                "s14": (c / c.shift(14) - 1) / mr,
                "dhi": (c / h.rolling(20, min_periods=10).max() - 1) / mr,
                "dhi10": (c / h.rolling(10, min_periods=7).max() - 1) / mr,
                "r60": c / c.shift(60) - 1,
                "sdrel": sd / sd.rolling(120, min_periods=40).median(),
                "pos": b["postRebalance_current_allocation"],
            })
            for H in [3, 5, 10]:
                d = base.copy()
                d["H"] = H
                d["u"] = (c.shift(-H) / c - 1) - drift[H]
                rows.append(d.iloc[::H])
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    D["year"] = D["ts"].dt.year
    F = D[D["fc"]].dropna(subset=["u"])
    def slope_t(G, x):
        G = G.dropna(subset=[x, "u"])
        if len(G) < 10: return (np.nan, np.nan, len(G))
        X = G[x] - G[x].mean()
        b = (X * G["u"]).sum() / (X ** 2).sum()
        e = G["u"] - G["u"].mean() - b * X
        s = (X * e).groupby(G["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (X ** 2).sum()
        return (b, b / se, len(G))
    out = {}
    res = {}
    for H in [3, 5, 10]:
        G = F[F["H"] == H]
        for x in ["s7", "s14", "dhi", "dhi10", "r60", "sdrel"]:
            b, t, n = slope_t(G, x)
            res[(H, x)] = {"slope": b, "t_day": t, "n": n}
    out["slopes_by_horizon"] = pd.DataFrame(res).T
    G = F[F["H"] == 3].dropna(subset=["s7", "dhi", "u"])
    X = np.column_stack([np.ones(len(G)), G["s7"], G["dhi"]])
    beta = np.linalg.lstsq(X, G["u"], rcond=None)[0]
    e = G["u"] - X @ beta
    XtXi = np.linalg.inv(X.T @ X)
    S = np.zeros((3, 3))
    for _, idx in G.groupby("day").indices.items():
        g = X[idx].T @ e.values[idx]; S += np.outer(g, g)
    se = np.sqrt(np.diag(XtXi @ S @ XtXi))
    out["joint_s7_dhi_h3"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["c", "s7", "dhi"])
    out["corr_s7_dhi"] = float(G[["s7", "dhi"]].corr().iloc[0, 1])
    by = {}
    for key, g in F[F["H"] == 3].groupby("coin"):
        for x in ["s7", "dhi"]:
            b, t, n = slope_t(g, x); by[(key, x)] = {"slope": b, "t": t, "n": n}
    for key, g in F[F["H"] == 3].groupby("year"):
        for x in ["s7", "dhi"]:
            b, t, n = slope_t(g, x); by[(str(key), x)] = {"slope": b, "t": t, "n": n}
    out["s7_dhi_by_coin_year_h3"] = pd.DataFrame(by).T
    G5 = F[F["H"] == 5].dropna(subset=["s7"]).copy()
    G5["bin"] = pd.qcut(G5["s7"], 5, labels=False)
    out["s7_quint_h5"] = G5.groupby("bin")["u"].agg(["count", "mean"])
    G10 = F[F["H"] == 10].dropna(subset=["s7"]).copy()
    G10["bin"] = pd.qcut(G10["s7"], 4, labels=False)
    out["s7_quart_h10"] = G10.groupby("bin")["u"].agg(["count", "mean"])
    Gr = F[F["H"] == 3].dropna(subset=["r60"]).copy()
    Gr["bin"] = pd.qcut(Gr["r60"], 4, labels=False)
    out["r60_quart_h3"] = Gr.groupby("bin").agg(lo=("r60", "min"), hi=("r60", "max"), n=("u", "count"), m=("u", "mean"))
    return out
