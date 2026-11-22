def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    drift = {}
    for coin in bars:
        for h in (6, 12, 24):
            drift[(coin, h)] = pd.concat([(df["close"].reset_index(drop=True).shift(-h) / df["close"].reset_index(drop=True) - 1).iloc[::h].dropna() for df in bars[coin].values()]).mean()
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"]; v = df["volume"]
            r1 = c.pct_change()
            sd = r1.rolling(720, min_periods=240).std()
            z = r1 / sd
            vr = v / v.rolling(720, min_periods=240).mean()
            r24p = (c / c.shift(24) - 1) / (sd * np.sqrt(24))
            ts = pd.to_datetime(df["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "wn": int(w[1:]), "pos": np.arange(len(df)), "z": z, "vr": vr,
                              "r24p": r24p, "hour": ts.dt.hour, "year": ts.dt.year})
            for h in (6, 12, 24):
                d[f"f{h}"] = (c.shift(-h) / c - 1) - drift[(coin, h)]
            d["r1next"] = c.shift(-1) / c - 1
            rows.append(d)
    A = pd.concat(rows, ignore_index=True).dropna(subset=["z", "vr"])
    def thin(sub, h):
        keep = []
        for (coin, w), g in sub.groupby(["coin", "w"]):
            last = -10**9
            for p, idx in zip(g["pos"].values, g.index.values):
                if p - last >= h:
                    keep.append(idx); last = p
        return sub.loc[keep]
    def st(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"n": n, "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(n)) if n > 2 else np.nan})
    U = A[(A["z"] >= 2.5) & (A["vr"] >= 2)].dropna(subset=["f24"])
    U = thin(U, 24)
    U["s"] = U["z"] * np.log(U["vr"])
    U["sq"] = pd.qcut(U["s"], 4, labels=False)
    out["up_heavy_by_strength_quartile_f24"] = U.groupby("sq")["f24"].apply(st).unstack()
    out["up_heavy_by_coin_f24"] = U.groupby("coin")["f24"].apply(st).unstack()
    out["up_heavy_by_year_f24"] = U.groupby("year")["f24"].apply(st).unstack()
    out["up_heavy_by_windowhalf"] = U.groupby(U["wn"] > 12)["f24"].apply(st).unstack()
    out["up_heavy_f6_f12"] = pd.DataFrame({"f6": st(U["f6"]), "f12": st(U["f12"])})
    sl = np.polyfit(U["s"], U["f24"], 1)[0]
    out["up_heavy_slope_f24_on_s"] = float(sl)
    out["up_heavy_corr_f24_s"] = float(np.corrcoef(U["s"], U["f24"])[0, 1])
    # down heavy comparable
    Dn = thin(A[(A["z"] <= -2.5) & (A["vr"] >= 2)].dropna(subset=["f24"]), 24)
    out["down_heavy_f24_rebound"] = st(Dn["f24"]).to_frame().T
    # past 24h quintile reversal by coin and window half
    G = A[A["pos"] % 24 == 0].dropna(subset=["r24p", "f24"]).copy()
    G["q"] = pd.qcut(G["r24p"], 5, labels=False)
    out["past24_q0_by_coin"] = G[G.q == 0].groupby("coin")["f24"].apply(st).unstack()
    out["past24_q0_by_half"] = G[G.q == 0].groupby(G["wn"] > 12)["f24"].apply(st).unstack()
    out["past24_corr"] = float(np.corrcoef(G["r24p"], G["f24"])[0, 1])
    # hours 20-21 by year and coin
    H = A[A["hour"].isin([20, 21])].dropna(subset=["r1next"])
    out["h20_21_by_year_bp"] = H.groupby("year")["r1next"].apply(lambda x: st(x * 100)).unstack()
    out["h20_21_by_coin"] = H.groupby("coin")["r1next"].apply(lambda x: st(x * 100)).unstack()
    return out
