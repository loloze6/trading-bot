import numpy as np
import pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            d = pd.DataFrame({"ts": pd.to_datetime(b["timestamp"])})
            d["coin"] = coin; d["w"] = w
            d["r1"] = c.pct_change()
            rr = (h - l) / c
            d["mrr"] = rr.rolling(30, min_periods=20).mean()
            d["sc"] = d["r1"] / d["mrr"]
            d["rng_sc"] = rr / d["mrr"]
            d["hc_sc"] = ((h - c) / c) / d["mrr"]      # drop from the day's high to close, scaled
            d["cl_sc"] = ((c - l) / c) / d["mrr"]      # recovery from low to close, scaled
            d["clv"] = ((c - l) / (h - l)).where(h > l)
            d["f1"] = c.shift(-1) / c - 1
            sd30 = d["r1"].rolling(30, min_periods=20).std()
            d["agit"] = sd30 / sd30.rolling(90, min_periods=40).median()
            d["pos"] = np.arange(len(d))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["r1"].mean()
    D["x1"] = D["f1"] - D["coin"].map(mu)
    D["day"] = D["ts"].dt.floor("D")

    def slope(df, xcol, ycol="x1"):
        g = df.dropna(subset=[xcol, ycol])
        x = g[xcol].values; y = g[ycol].values
        X = np.column_stack([np.ones(len(x)), x])
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        sc = pd.DataFrame(X * e[:, None]).groupby(g["day"].values).sum().values
        G = len(sc)
        V = XtXi @ (sc.T @ sc) @ XtXi * G / (G - 1)
        return {"n": len(g), "days": G, "slope": beta[1], "t": beta[1] / np.sqrt(V[1, 1])}

    def summ(df, by, col="x1"):
        out = {}
        for k, g in df.groupby(by, observed=True):
            g = g.dropna(subset=[col])
            if len(g) < 20:
                continue
            m = g[col].mean()
            s = (g[col] - m).groupby(g["day"]).sum()
            se = np.sqrt((s ** 2).sum()) / len(g)
            out[k] = {"n": len(g), "days": g["day"].nunique(), "mean%": 100 * m, "t_day": m / se}
        return pd.DataFrame(out).T

    res = {}
    A = D.dropna(subset=["sc", "x1", "clv"]).copy()
    Dn = A[A["r1"] < 0].copy()
    Up = A[A["r1"] > 0].copy()
    sl = {}
    sl["down: -sc"] = slope(Dn.assign(v=-Dn["sc"]), "v")
    sl["down: hc_sc"] = slope(Dn, "hc_sc")
    sl["down: 1-clv"] = slope(Dn.assign(v=1 - Dn["clv"]), "v")
    sl["down: -sc*(1-clv)"] = slope(Dn.assign(v=-Dn["sc"] * (1 - Dn["clv"])), "v")
    sl["down: rng_sc"] = slope(Dn, "rng_sc")
    sl["up: rng_sc"] = slope(Up, "rng_sc")
    sl["up: sc"] = slope(Up, "sc")
    sl["up: cl_sc"] = slope(Up, "cl_sc")
    sl["all: hc_sc"] = slope(A, "hc_sc")
    sl["all: cl_sc"] = slope(A, "cl_sc")
    sl["all: hc_sc-cl_sc"] = slope(A.assign(v=A["hc_sc"] - A["cl_sc"]), "v")
    sl["down agit>1: -sc"] = slope(Dn[Dn["agit"] > 1].assign(v=-Dn["sc"]), "v")
    sl["down agit<=1: -sc"] = slope(Dn[Dn["agit"] <= 1].assign(v=-Dn["sc"]), "v")
    sl["down agit>1: hc_sc"] = slope(Dn[Dn["agit"] > 1], "hc_sc")
    sl["down agit<=1: hc_sc"] = slope(Dn[Dn["agit"] <= 1], "hc_sc")
    res["slopes"] = pd.DataFrame(sl).T
    A["hcq"] = pd.qcut(A["hc_sc"], 5, labels=False, duplicates="drop")
    res["all_by_hc_sc_quintile"] = summ(A, "hcq")
    Dn["hcq"] = pd.qcut(Dn["hc_sc"], 5, labels=False, duplicates="drop")
    res["down_by_hc_sc_quintile"] = summ(Dn, "hcq")
    Up["hcq"] = pd.qcut(Up["hc_sc"], 5, labels=False, duplicates="drop")
    res["up_by_hc_sc_quintile"] = summ(Up, "hcq")
    big = Dn[-Dn["sc"] >= (-Dn["sc"]).quantile(0.8)].copy()
    big["clvt"] = pd.qcut(big["clv"], 3, labels=False)
    res["bigfall_by_clv_tercile"] = summ(big, "clvt")
    res["bigfall_by_clvt_coin_mean%"] = big.groupby(["coin", "clvt"])["x1"].mean().unstack() * 100
    res["hc_slope_by_window"] = pd.DataFrame({w: slope(A[A["w"] == w], "hc_sc") for w in sorted(A["w"].unique())}).T
    return res
