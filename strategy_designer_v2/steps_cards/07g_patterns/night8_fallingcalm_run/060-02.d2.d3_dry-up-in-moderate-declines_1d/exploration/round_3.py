import numpy as np, pandas as pd

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
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c / c.shift(1) - 1
            ts = pd.to_datetime(b["timestamp"])
            m30 = v.rolling(30).mean()
            sd30 = r1.rolling(30).std()
            d = pd.DataFrame({"coin": coin, "w": w,
                "fwd": c.shift(-5) / c - 1,
                "r60": c / c.shift(60) - 1, "r10": c / c.shift(10) - 1,
                "shr": -np.log(m30 / m30.shift(30)),
                "agr": sd30 / sd30.rolling(120, min_periods=60).median(),
                "fc": b["forecast"], "yr": ts.dt.year, "day": ts.dt.floor("D")})
            rows.append(d.iloc[np.arange(0, len(b), 5)])
    D = pd.concat(rows, ignore_index=True)
    D["ex"] = D["fwd"] - D.groupby("coin")["fwd"].transform("mean")
    D["prof"] = np.where(D.r60 > 0.1, "rising", np.where(D.r60 < -0.1, "falling", "choppy"))
    D.loc[D.r60.isna(), "prof"] = "na"
    D["agit"] = np.where(D.agr > 1, "agit", "calm"); D.loc[D.agr.isna(), "agit"] = "na"
    F = D[D.prof == "falling"].copy(); R = D[D.prof == "rising"].copy()
    out = {}
    F["r10q"] = pd.qcut(F.r10, 5, labels=False)
    out["F_r10q5"] = F.groupby("r10q").apply(ctt)
    out["F_r10q5_r10mean"] = F.groupby("r10q")["r10"].mean()
    out["F_r10pos_by_agit"] = F[F.r10 > 0].groupby("agit").apply(ctt)
    out["F_r10pos_by_yr"] = F[F.r10 > 0].groupby("yr").apply(ctt)
    out["F_r10pos_by_coin"] = F[F.r10 > 0].groupby("coin").apply(ctt)
    out["F_r10neg_by_r10q"] = F[F.r10 < 0].groupby(pd.qcut(F[F.r10 < 0].r10, 4, labels=False)).apply(ctt)
    out["F_active_cl"] = F.groupby(F.fc < 0).apply(ctt)
    out["F_active_by_agit"] = F[F.fc < 0].groupby("agit").apply(ctt)
    R["shq"] = pd.qcut(R.shr, 4, labels=False)
    out["R_shq_by_agit"] = R.groupby(["agit", "shq"]).apply(ctt)
    out["R_topshr_by_coin"] = R[R.shq == 3].groupby("coin").apply(ctt)
    return out
