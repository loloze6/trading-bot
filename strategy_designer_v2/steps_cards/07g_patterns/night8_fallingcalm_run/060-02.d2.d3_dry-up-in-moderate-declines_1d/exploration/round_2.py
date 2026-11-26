import numpy as np, pandas as pd
from scipy import stats

def ctt(g, col="ex"):
    x = g[[col, "day"]].dropna()
    if len(x) < 5:
        return pd.Series({"n": len(x), "days": x["day"].nunique() if len(x) else 0, "mean": np.nan, "t_cl": np.nan})
    m = x[col].mean()
    dev = (x[col] - m).groupby(x["day"]).sum()
    se = np.sqrt((dev ** 2).sum()) / len(x)
    return pd.Series({"n": len(x), "days": x["day"].nunique(), "mean": m, "t_cl": m / se if se > 0 else np.nan})

def explore(data):
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            v = b["volume"].astype(float)
            r1 = c / c.shift(1) - 1
            ts = pd.to_datetime(b["timestamp"])
            sd30 = r1.rolling(30).std()
            m30 = v.rolling(30).mean()
            d = pd.DataFrame({
                "coin": coin, "w": w,
                "fwd": c.shift(-5) / c - 1,
                "fwd2": c.shift(-2) / c - 1,
                "r60": c / c.shift(60) - 1,
                "r10": c / c.shift(10) - 1,
                "r1": r1,
                "shr": -np.log(m30 / m30.shift(30)),
                "loc": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "rng": (b["high"] - b["low"]) / c,
                "rngz": ((b["high"] - b["low"]) / c) / (sd30 + 1e-12),
                "vrel": v / v.rolling(30).mean(),
                "fc": b["forecast"],
                "yr": ts.dt.year,
                "day": ts.dt.floor("D"),
            })
            idx = np.arange(0, len(b), 5)
            rows.append(d.iloc[idx])
    D = pd.concat(rows, ignore_index=True)
    D["ex"] = D["fwd"] - D.groupby("coin")["fwd"].transform("mean")
    D["ex2"] = D["fwd2"] - D.groupby("coin")["fwd2"].transform("mean")
    D["prof"] = np.where(D.r60 > 0.1, "rising", np.where(D.r60 < -0.1, "falling", "choppy"))
    D.loc[D.r60.isna(), "prof"] = "na"
    F = D[D.prof == "falling"].copy()
    R = D[D.prof == "rising"].copy()
    out = {}

    # falling: close location, graded, clustered
    F["locq"] = pd.qcut(F["loc"], 5, labels=False)
    out["F_locq5"] = F.groupby("locq").apply(ctt)
    out["F_locq5_ex2"] = F.groupby("locq").apply(lambda g: ctt(g, "ex2"))
    out["F_lowclose_by_yr"] = F[F.locq <= 1].groupby("yr").apply(ctt)
    out["F_lowclose_by_shrink_half"] = F.assign(sh=F.shr > F.shr.median()).groupby(["sh", F.locq <= 1]).apply(ctt)
    out["F_lowclose_by_fc"] = F.groupby([F.fc < 0, F.locq <= 1]).apply(ctt)

    # regression of ex on loc, shr, r10 in falling (pooled OLS, plain t)
    G = F.dropna(subset=["ex", "loc", "shr", "r10"])
    X = np.column_stack([np.ones(len(G)), G["loc"], G["shr"], G["r10"]])
    beta, *_ = np.linalg.lstsq(X, G["ex"].values, rcond=None)
    res = G["ex"].values - X @ beta
    s2 = res @ res / (len(G) - 4)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["F_ols"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "loc", "shr", "r10"])

    # falling: loc x range size
    F["rq"] = pd.qcut(F["rngz"], 3, labels=False)
    out["F_lowclose_x_range"] = F.groupby(["rq", F.locq <= 1]).apply(ctt)

    # rising: shrink graded, clustered, by year
    R["shq"] = pd.qcut(R["shr"], 4, labels=False)
    out["R_shq"] = R.groupby("shq").apply(ctt)
    out["R_topshr_by_yr"] = R[R.shq == 3].groupby("yr").apply(ctt)
    out["R_locq"] = R.groupby(pd.qcut(R["loc"], 3, labels=False)).apply(ctt)

    # all-profile low close (to see whether it's falling-specific)
    D["locq"] = pd.qcut(D["loc"], 5, labels=False)
    out["All_locq_by_prof_low"] = D[D.locq == 0].groupby("prof").apply(ctt)
    return out
