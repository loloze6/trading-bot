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
            clpos = (b["close"] - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "z": z, "tr": tr,
                               "fwd": fwd, "clpos": clpos, "day": ts.dt.floor("D"), "wd": ts.dt.weekday,
                               "yr": ts.dt.year})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True).dropna(subset=["fwd", "z"])
    A["drift"] = A.groupby("coin")["fwd"].transform("mean")
    A["usual"] = A.groupby("coin")["fwd"].transform("std")
    A["str"] = (A["fwd"] - A["drift"]) / A["usual"]
    def dayt(x, col="str"):
        x = x.dropna(subset=[col])
        if len(x) < 3: return pd.Series({"n": len(x), "days": x["day"].nunique(), "mean": np.nan, "t": np.nan})
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / max(D - 1, 1)) / len(x)
        return pd.Series({"n": len(x), "days": D, "mean": m, "t": m / se if se > 0 else np.nan})
    out = {}
    G = A[A["pos"] % H == 0]
    out["weekday strength, day-grouped t, grid 0"] = G.groupby("wd").apply(dayt)
    res = []
    for off in range(H):
        Go = A[A["pos"] % H == off]
        U = Go[(Go["z"] >= 2) & (Go["clpos"] > 0.8)]
        L = Go[(Go["z"] >= 2) & (Go["clpos"] <= 0.8)]
        Dn = Go[(Go["z"] <= -2)]
        s = dayt(U); s2 = dayt(L); s3 = dayt(Dn)
        P = Go[Go["z"] >= 1].dropna(subset=["clpos"])
        rho = stats.spearmanr(P["z"] * P["clpos"], P["str"])[0] if len(P) > 10 else np.nan
        res.append({"offset": off, "upHigh n": s["n"], "upHigh mean": s["mean"], "upHigh t": s["t"],
                    "upOther n": s2["n"], "upOther mean": s2["mean"], "upOther t": s2["t"],
                    "down n": s3["n"], "down mean": s3["mean"], "down t": s3["t"], "rho z*clpos up>=1": rho})
    out["robustness over grid offsets"] = pd.DataFrame(res).set_index("offset")
    U = A[(A["z"] >= 2) & (A["clpos"] > 0.8)].copy()
    U["trb"] = np.where(U["tr"].isna(), "na", np.where(U["tr"] > 0.1, "rising", np.where(U["tr"] < -0.1, "falling", "choppy")))
    out["all-days z>=2 close-high by trend (overlapping, indicative)"] = U.groupby("trb").apply(dayt)
    out["all-days z>=2 close-high by year (overlapping)"] = U.groupby("yr").apply(dayt)
    return out
