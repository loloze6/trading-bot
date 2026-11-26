def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r28 = cl / cl.shift(28) - 1
            hi = cl.rolling(28, min_periods=28).max()
            D = (hi / cl - 1) * 100
            fc = b["forecast"]
            fwd = cl.shift(-5) / cl - 1
            rng = ((b["high"] - b["low"]) / cl)
            rngz = rng / rng.rolling(28, min_periods=20).mean()
            idx = np.arange(0, len(b), 5)
            rows.append(pd.DataFrame({"coin": c, "w": w, "year": pd.to_datetime(b["timestamp"]).dt.year.iloc[idx].values,
                                      "fwd": fwd.iloc[idx].values, "r28": r28.iloc[idx].values, "D": D.iloc[idx].values,
                                      "fc": fc.iloc[idx].values, "rngz": rngz.iloc[idx].values,
                                      "reg": (b["regime"].iloc[idx] == "trending").values}))
    S = pd.concat(rows).dropna(subset=["fwd", "r28", "D"])
    S["ex"] = S["fwd"] - S.groupby("coin")["fwd"].transform("mean")
    S["z"] = S["ex"] / S.groupby("coin")["fwd"].transform("std")
    S["near"] = -np.log1p(S["D"])
    inr = S[S.reg].copy()
    def t(x, y):
        m = x.notna() & y.notna()
        l = stats.linregress(x[m], y[m]); return l.slope / l.stderr
    out["inreg_t"] = pd.Series({"n": len(inr), "t_raw_near_z": t(inr["near"], inr["z"]), "t_raw_near_ex": t(inr["near"], inr["ex"]),
                                "t_forecast_ex": t(inr["fc"], inr["ex"]), "corr_fc_near": inr[["fc", "near"]].corr().iloc[0, 1]})
    out["all_bars_t"] = pd.Series({"n": len(S), "t_near_all_z": t(S["near"], S["z"]),
                                   "t_near_down28_z": t(S[~S.reg]["near"], S[~S.reg]["z"])})
    inr["q"] = pd.qcut(inr["D"].rank(method="first"), 5, labels=["q1_nearest", "q2", "q3", "q4", "q5_farthest"])
    out["inreg_by_D_quintile"] = inr.groupby("q").agg(n=("ex", "size"), D_mean=("D", "mean"), ex_mean=("ex", "mean"), z_mean=("z", "mean"))
    S["q"] = pd.qcut(S["D"].rank(method="first"), 5, labels=["q1_nearest", "q2", "q3", "q4", "q5_farthest"])
    out["all_by_D_quintile"] = S.groupby("q").agg(n=("ex", "size"), D_mean=("D", "mean"), ex_mean=("ex", "mean"))
    out["inreg_t_by_year"] = inr.groupby("year").apply(lambda g: pd.Series({"n": len(g), "t_near": t(g["near"], g["z"]), "ex": g["ex"].mean()}))
    out["inreg_t_by_coin"] = inr.groupby("coin").apply(lambda g: pd.Series({"n": len(g), "t_near": t(g["near"], g["z"])}))
    # calm vs violent range at high
    inr["calm"] = inr["rngz"] < inr["rngz"].median()
    out["inreg_near_by_calm"] = inr.groupby("calm").apply(lambda g: pd.Series({"n": len(g), "t_near": t(g["near"], g["z"]), "ex": g["ex"].mean()}))
    return out
