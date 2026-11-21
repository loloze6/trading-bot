import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; out = {}
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            ts = pd.to_datetime(df["timestamp"])
            f = pd.DataFrame({
                "mom14": c / c.shift(14) - 1,
                "mom28": c / c.shift(28) - 1,
                "z1": r1 / r1.rolling(14).std().shift(1),
                "z7": (c / c.shift(7) - 1) / (r1.rolling(28).std() * np.sqrt(7)),
                "yr": ts.dt.year,
                "fc": df["forecast"].astype(float),
            })
            for H in (7, 14):
                fwd = c.shift(-H) / c - 1
                idx = np.arange(0, len(df), H)
                sub = f.iloc[idx].copy(); sub["fwd"] = fwd.iloc[idx].values
                sub["H"] = H; sub["coin"] = coin; sub["win"] = int(w[1:])
                rows.append(sub)
    A = pd.concat(rows).dropna(subset=["fwd"])
    A["drift"] = A.groupby(["coin", "H"])["fwd"].transform("mean")
    A["usual"] = A.groupby(["coin", "H"])["fwd"].transform("std")
    A["un"] = (A["fwd"] - A["drift"]) / A["usual"]
    A["unp"] = A["fwd"] - A["drift"]
    res = []; byc = []; byy = []
    for H in (7, 14):
        B = A[A.H == H]
        for feat in ["mom14", "mom28", "z1", "z7"]:
            C = B.dropna(subset=[feat]).copy()
            C["rk"] = C.groupby("coin")[feat].rank(pct=True) - 0.5
            C["sgn"] = np.sign(C["rk"])
            C["str"] = C["sgn"] * C["un"]; C["mv"] = C["sgn"] * C["unp"]; C["tot"] = C["sgn"] * C["fwd"]
            sl, ic, rr, p, se = stats.linregress(C["rk"], C["un"])
            top = C[C.rk > 0.3]
            res.append({"H": H, "feat": feat, "n": len(C), "slope_t": sl / se,
                        "signed_strength": C["str"].mean(), "t_signed": C["str"].mean() / (C["str"].std() / np.sqrt(len(C))),
                        "signed_unusual_pct": 100 * C["mv"].mean(), "top20_unusual_pct": 100 * top["unp"].mean(),
                        "early_half_t": stats.linregress(C[C.win <= 12]["rk"], C[C.win <= 12]["un"]).slope / stats.linregress(C[C.win <= 12]["rk"], C[C.win <= 12]["un"]).stderr,
                        "late_half_t": stats.linregress(C[C.win > 12]["rk"], C[C.win > 12]["un"]).slope / stats.linregress(C[C.win > 12]["rk"], C[C.win > 12]["un"]).stderr})
            if H == 7 and feat in ("mom14", "z7"):
                for coin, g in C.groupby("coin"):
                    s = stats.linregress(g["rk"], g["un"])
                    byc.append({"feat": feat, "coin": coin, "n": len(g), "slope_t": s.slope / s.stderr, "signed_unusual_pct": 100 * g["mv"].mean()})
                for y, g in C.groupby("yr"):
                    s = stats.linregress(g["rk"], g["un"])
                    byy.append({"feat": feat, "yr": y, "n": len(g), "slope_t": s.slope / s.stderr})
    out["momentum"] = pd.DataFrame(res).round(3)
    out["by_coin_7d"] = pd.DataFrame(byc).round(3)
    out["by_year_7d"] = pd.DataFrame(byy).round(2)
    # weekday robustness
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, win=int(w[1:])))
    D = pd.concat(D).dropna(subset=["coin_return"])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    D["cr"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    sat = D[D.wd == 5]; thu = D[D.wd == 3]
    out["sat_by_coin"] = sat.groupby("coin")["cr"].agg(["mean", "size"]).round(5)
    out["sat_by_year"] = sat.groupby("yr")["cr"].agg(["mean", "size"]).round(5)
    out["thu_by_year"] = thu.groupby("yr")["cr"].agg(["mean", "size"]).round(5)
    return out
