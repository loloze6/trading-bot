import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            mad = r.abs().rolling(60, min_periods=20).mean().shift(1)
            rng = (b["high"]-b["low"]).astype(float)
            df = pd.DataFrame({
                "coin": coin, "w": w, "r": r, "z": r/mad,
                "nx1": c.shift(-1)/c - 1,
                "nx2": c.shift(-2)/c - 1,
                "clv": ((c-b["low"])/rng.replace(0,np.nan)).values,
                "wick_up": ((b["high"]-np.maximum(b["open"],c))/rng.replace(0,np.nan)).values,
                "regime": b["regime"].values,
                "yr": pd.to_datetime(b["timestamp"]).dt.year.values,
                "pos_in_w": np.arange(len(b)),
            })
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    mc = D.groupby("coin")["nx1"].mean()
    D["ex1"] = D["nx1"] - D["coin"].map(mc)
    M = D[D["regime"] == "mean_reversion"].dropna(subset=["ex1","z","clv"]).copy()
    U = D[D["regime"] != "mean_reversion"].dropna(subset=["ex1","z","clv"]).copy()

    def ols(df):
        X = np.column_stack([np.ones(len(df)), df["z"].clip(-4,4), df["clv"]-0.5])
        y = df["ex1"].values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        res = y - X @ beta
        s2 = res @ res / (len(y)-3)
        se = np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
        return pd.Series({"n": len(y), "b_z": beta[1], "t_z": beta[1]/se[1], "b_clv": beta[2], "t_clv": beta[2]/se[2]})
    out["ols_mr_all"] = ols(M).round(4)
    out["ols_unknown_all"] = ols(U).round(4)
    out["ols_mr_by_coin"] = M.groupby("coin").apply(ols).round(4)
    M["half"] = np.where(M["yr"] <= 2021, "2018-21", "2022-25")
    out["ols_mr_by_half"] = M.groupby("half").apply(ols).round(4)
    # clv grade within up and down days in mr
    M["up"] = M["r"] > 0
    M["clvb"] = pd.cut(M["clv"], [0,1/3,2/3,1], include_lowest=True)
    def agg(g, col="ex1"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x)))})
    out["mr_clv_by_updown"] = M.groupby(["up","clvb"], observed=True).apply(agg).round(4)
    # large up moves in mr: by coin and half
    M["zq"] = pd.cut(M["z"], [-np.inf,-1.2,0,1.2,np.inf])
    out["mr_up_z_by_coin"] = M[M["z"]>0].groupby(["coin","zq"], observed=True).apply(agg).round(4)
    out["mr_up_z_by_half"] = M[M["z"]>0].groupby(["half","zq"], observed=True).apply(agg).round(4)
    # rank corr z vs ex1 on up days in mr
    up = M[M["z"]>0]
    rho, p = stats.spearmanr(up["z"], up["ex1"])
    out["mr_up_spearman"] = pd.Series({"n": len(up), "rho": rho, "p": p})
    # 2-day horizon, non-overlapping grid (even positions) for clv in mr
    G = M[M["pos_in_w"] % 2 == 0].dropna(subset=["nx2"]).copy()
    G["ex2"] = G["nx2"] - G["coin"].map(D.groupby("coin")["nx2"].mean())
    out["mr_clv_2day_grid"] = G.groupby("clvb", observed=True).apply(lambda g: agg(g,"ex2")).round(4)
    lo = M.loc[M["clv"]<=0.2,"ex1"]; hi = M.loc[M["clv"]>0.8,"ex1"]
    out["mr_clv_low_minus_high_welch"] = pd.Series({"diff": lo.mean()-hi.mean(), "t": stats.ttest_ind(lo,hi,equal_var=False).statistic})
    return out
