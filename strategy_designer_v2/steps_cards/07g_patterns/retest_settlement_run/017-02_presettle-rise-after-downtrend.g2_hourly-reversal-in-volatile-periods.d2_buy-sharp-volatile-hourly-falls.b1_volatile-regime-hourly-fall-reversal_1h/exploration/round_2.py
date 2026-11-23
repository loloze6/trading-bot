def explore(data):
    import numpy as np, pandas as pd
    out = {}
    hourly = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol24 = r1.rolling(24).std()
            usual = vol24.rolling(720, min_periods=240).mean()
            vr = vol24 / usual
            p24z = (c / c.shift(24) - 1) / (usual * np.sqrt(24))
            p72z = (c / c.shift(72) - 1) / (usual * np.sqrt(72))
            f24 = c.shift(-24) / c - 1
            f1 = c.shift(-1) / c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "hour": ts.dt.hour.values, "year": ts.dt.year.values,
                               "vr": vr.values, "p24z": p24z.values, "p72z": p72z.values,
                               "f24": f24.values, "f1": f1.values})
            df["pos"] = np.arange(len(df))
            df["wn"] = int(w[1:])
            hourly.append(df)
    H = pd.concat(hourly, ignore_index=True)
    G = H[H["pos"] % 24 == 0].dropna(subset=["f24"])
    cm = G.groupby("coin")["f24"].mean()
    G = G.assign(x24=G["f24"] - G["coin"].map(cm)).dropna(subset=["p24z", "vr"])
    def tt(g):
        r = g.agg(["mean", "std", "count"]); r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"])); return r[["mean", "t", "count"]]
    hi = G[G["vr"] >= 1].copy()
    hi["sx"] = -np.sign(hi["p24z"]) * hi["x24"]
    hi["pb"] = pd.qcut(hi["p24z"], 10)
    out["hi_p24z_decile"] = tt(hi.groupby("pb", observed=True)["x24"])
    hi["vrb"] = pd.cut(hi["vr"], [1, 1.3, 1.7, 2.5, np.inf])
    hi["big"] = np.where(hi["p24z"].abs() > 0.7, "big", "small")
    out["hi_reversal_by_vr_and_size"] = tt(hi.groupby(["vrb", "big"], observed=True)["sx"])
    out["hi_reversal_by_coin"] = tt(hi[hi["p24z"].abs() > 0.7].groupby("coin")["sx"])
    hi["half"] = np.where(hi["wn"] <= 12, "w1-w12", "w13-w24")
    out["hi_reversal_by_half"] = tt(hi[hi["p24z"].abs() > 0.7].groupby(["half", np.where(hi["p24z"] > 0, "up", "down")[hi["p24z"].abs() > 0.7]])["sx"])
    out["hi_reversal_by_year"] = tt(hi[hi["p24z"].abs() > 0.7].groupby("year")["sx"])
    hi["p72b"] = pd.qcut(hi["p72z"], 5)
    out["hi_p72z_quintile"] = tt(hi.dropna(subset=["p72b"]).groupby("p72b", observed=True)["x24"])
    # hour effect robustness: row hours 20,21 (returns 21-23 UTC)
    E = H.dropna(subset=["f1"]).copy()
    E["late"] = E["hour"].isin([20, 21])
    out["late_by_coin"] = tt(E[E["late"]].groupby("coin")["f1"])
    E["half"] = np.where(E["wn"] <= 12, "w1-w12", "w13-w24")
    out["late_by_half"] = tt(E[E["late"]].groupby("half")["f1"])
    out["late_by_year"] = tt(E[E["late"]].groupby("year")["f1"])
    return out
