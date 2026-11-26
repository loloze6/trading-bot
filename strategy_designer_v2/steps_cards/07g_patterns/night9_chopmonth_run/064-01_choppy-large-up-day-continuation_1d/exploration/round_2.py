def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd.shift(1)
            tr = c / c.shift(60) - 1
            fwd = c.shift(-H) / c - 1
            fwd2 = c.shift(-2) / c - 1
            clpos = (b["close"] - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            agit = sd / sd.rolling(90, min_periods=30).median()
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "r": r, "z": z, "tr": tr,
                               "fwd": fwd, "fwd2": fwd2, "clpos": clpos, "day": ts.dt.floor("D"),
                               "yr": ts.dt.year, "agit": agit})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % H == 0)].dropna(subset=["fwd", "z"]).copy()
    G["drift"] = G.groupby("coin")["fwd"].transform("mean")
    G["usual"] = G.groupby("coin")["fwd"].transform("std")
    G["unus"] = G["fwd"] - G["drift"]
    G["str"] = G["unus"] / G["usual"]
    G["unusw"] = G["unus"].clip(-0.3, 0.3)
    def dayt(g, col):
        x = g.dropna(subset=[col])
        if len(x) < 3: return pd.Series({"n": len(x), "days": x["day"].nunique(), "mean": np.nan, "t": np.nan, "median%": np.nan})
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / max(D - 1, 1)) / len(x)
        return pd.Series({"n": len(x), "days": D, "mean": m, "t": m / se if se > 0 else np.nan,
                          "median%": 100 * x["fwd"].median()})
    out = {}
    U = G[G["z"] >= 1.5].copy()
    U["clb"] = pd.cut(U["clpos"], [-0.01, 0.5, 0.8, 1.01])
    out["up z>=1.5 strength by close position (day t)"] = U.groupby("clb").apply(lambda g: dayt(g, "str"))
    out["up z>=1.5 winsorized unusual by close position"] = U.groupby("clb").apply(lambda g: dayt(g, "unusw"))
    U2 = U[U["clpos"] > 0.8]
    U2 = U2.copy(); U2["zb"] = pd.cut(U2["z"], [1.5, 2, 3, 99])
    out["up close-high strength by z"] = U2.groupby("zb").apply(lambda g: dayt(g, "str"))
    out["up close-high strength by year"] = U2.groupby("yr").apply(lambda g: dayt(g, "str"))
    U2 = U2.copy(); U2["ab"] = np.where(U2["agit"] > 1, "agitated", "calm")
    out["up close-high strength by agitation"] = U2.groupby("ab").apply(lambda g: dayt(g, "str"))
    U2["trb"] = np.where(U2["tr"].isna(), "na", np.where(U2["tr"] > 0.1, "rising", np.where(U2["tr"] < -0.1, "falling", "choppy")))
    out["up close-high strength by trend"] = U2.groupby("trb").apply(lambda g: dayt(g, "str"))
    out["up close-high strength by coin"] = U2.groupby("coin").apply(lambda g: dayt(g, "str"))
    # grading: z*clpos as a score among all positive days
    P = G[G["z"] > 0].dropna(subset=["clpos"]).copy()
    P["score"] = P["z"] * (2 * P["clpos"] - 1)
    rho, p = stats.spearmanr(P["score"], P["str"])
    out["spearman score vs strength, up days"] = f"rho {rho:.3f} p {p:.4f} n {len(P)}"
    P["sb"] = pd.qcut(P["score"], 5, duplicates="drop")
    out["up days strength by score quintile"] = P.groupby("sb").apply(lambda g: dayt(g, "str"))
    # down days with close low: fwd strength
    Dn = G[G["z"] <= -1.5].copy(); Dn["clb"] = pd.cut(Dn["clpos"], [-0.01, 0.2, 0.5, 1.01])
    out["down z<=-1.5 strength by close position"] = Dn.groupby("clb").apply(lambda g: dayt(g, "str"))
    return out
