import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            vol = r.rolling(30, min_periods=20).std()
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            clv = (b["close"] - b["low"]) / rng
            d = pd.DataFrame({
                "w": w, "pos": np.arange(len(b)), "r": r, "z": r / vol, "clv": clv,
                "upwick": (b["high"] - np.maximum(b["open"], b["close"])) / b["close"] / vol,
                "lowick": (np.minimum(b["open"], b["close"]) - b["low"]) / b["close"] / vol,
                "rngz": (rng / b["close"]) / vol,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "n1": c.shift(-1) / c - 1, "n2": c.shift(-2) / c - 1, "n3": c.shift(-3) / c - 1,
                "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D["r"].mean()
    D["x1"] = D["n1"] - mu1
    D["cs"] = 2 * D["clv"] - 1  # -1 at low, +1 at high
    def tstat(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s)))})
    out = {}
    # regression x1 on z and cs (OLS with t)
    E = D[["x1", "z", "cs", "rngz"]].dropna()
    X = np.column_stack([np.ones(len(E)), E["z"], E["cs"], E["cs"] * E["rngz"]])
    beta, *_ = np.linalg.lstsq(X, E["x1"].values, rcond=None)
    res = E["x1"].values - X @ beta
    s2 = res @ res / (len(E) - X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["ols_x1_on_z_cs_csXrange"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "z", "cs", "cs*rngz"])
    # clv tercile within z tercile
    D["zt"] = pd.qcut(D["z"], 3, labels=False)
    D["ct"] = pd.qcut(D["clv"], 3, labels=False)
    g = D.groupby(["zt", "ct"])["x1"].apply(tstat).unstack()
    out["x1_by_z_tercile_and_clv_tercile"] = g
    # clv effect on bars where book was flat (forecast==0)
    F0 = D[D["fc"] == 0]
    out["flat_bars_x1_by_clv_quintile"] = F0.groupby(pd.qcut(F0["clv"], 5, labels=False))["x1"].apply(tstat).unstack()
    # clv quintile by year: top minus bottom
    yrs = []
    for y, G in D.groupby("yr"):
        q = pd.qcut(G["clv"], 5, labels=False)
        lo = G.loc[q == 0, "x1"]; hi = G.loc[q == 4, "x1"]
        tt = stats.ttest_ind(hi.dropna(), lo.dropna(), equal_var=False)
        yrs.append({"yr": y, "hi_minus_lo": hi.mean() - lo.mean(), "t": tt.statistic, "n": len(G)})
    out["clv_top_minus_bottom_by_year"] = pd.DataFrame(yrs).set_index("yr")
    # 2-day horizon grid 2 by clv quintile
    g2 = D[D["pos"] % 2 == 0].copy()
    g2["x2"] = g2["n2"] - g2["n2"].mean()
    out["grid2_x2_by_clv_quintile"] = g2.groupby(pd.qcut(g2["clv"], 5, labels=False))["x2"].apply(tstat).unstack()
    # clv extremes split by range size tercile
    D["rt"] = pd.qcut(D["rngz"], 3, labels=False)
    D["cq"] = pd.qcut(D["clv"], 5, labels=False)
    sub = D[D["cq"].isin([0, 4])]
    out["x1_clv_extremes_by_range_tercile"] = sub.groupby(["rt", "cq"])["x1"].apply(tstat).unstack()
    # wicks
    out["x1_by_upwick_quintile"] = D.groupby(pd.qcut(D["upwick"], 5, labels=False, duplicates="drop"))["x1"].apply(tstat).unstack()
    out["x1_by_lowick_quintile"] = D.groupby(pd.qcut(D["lowick"], 5, labels=False, duplicates="drop"))["x1"].apply(tstat).unstack()
    return out
