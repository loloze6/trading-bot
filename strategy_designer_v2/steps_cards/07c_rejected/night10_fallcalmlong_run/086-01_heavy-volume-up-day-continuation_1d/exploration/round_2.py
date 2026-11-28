def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].astype(float); v = df["volume"].astype(float)
            df["vr"] = v / v.shift(1).rolling(20, min_periods=20).mean()
            df["r1"] = c.pct_change()
            df["r5past"] = c / c.shift(5) - 1
            df["r20past"] = c / c.shift(20) - 1
            df["clv"] = (df["close"] - df["low"]) / (df["high"] - df["low"]).replace(0, np.nan)
            df["pos"] = np.arange(len(df))
            for h in [1, 3, 5, 10, 20]:
                df[f"f{h}"] = c.shift(-h) / c - 1
            df["inprof"] = df["regime"].isin(["trending", "unknown"])
            df["coin"] = coin; df["win"] = w
            df["day"] = pd.to_datetime(df["timestamp"]).dt.floor("D")
            df["year"] = pd.to_datetime(df["timestamp"]).dt.year
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    for h in [1, 3, 5, 10, 20]:
        g = A[A["pos"] % h == 0].groupby("coin")[f"f{h}"].mean()
        A[f"u{h}"] = A[f"f{h}"] - A["coin"].map(g)
    P = A[A["inprof"] & A["vr"].notna() & A["r1"].notna()].copy()
    def cases(mask, h):
        S = P[mask].copy()
        S["cell"] = S["pos"] // h
        S = S.sort_values("pos").groupby(["coin", "win", "cell"]).head(1)
        return S.dropna(subset=[f"u{h}"])
    def clt(S, h):
        if len(S) < 5: return pd.Series({"n": len(S)})
        d = S.groupby("day")[f"u{h}"].sum()
        m = S[f"u{h}"].mean()
        dev = S.groupby("day")[f"u{h}"].apply(lambda x: (x - m).sum())
        G = len(dev); se = np.sqrt((dev**2).sum() * G / (G - 1)) / len(S)
        return pd.Series({"n": len(S), "days": G, "mean": m, "t": m / se,
                          "rho_vr": stats.spearmanr(S["vr"], S[f"u{h}"])[0]})
    out = {}
    t = []
    for side in ["up", "down"]:
        for lab, lo, hi in [("light<1", 0, 1), ("1-1.5", 1, 1.5), ("heavy1.5-2", 1.5, 2), ("vheavy>=2", 2, 99)]:
            for h in [1, 3, 5, 10, 20]:
                m = (P["r1"] > 0 if side == "up" else P["r1"] < 0) & (P["vr"] >= lo) & (P["vr"] < hi)
                r = clt(cases(m, h), h); r["side"] = side; r["vol"] = lab; r["h"] = h; t.append(r)
    out["by_side_vol_h"] = pd.DataFrame(t)
    t = []
    for h in [3, 5, 10]:
        m = (P["r1"] < 0) & (P["vr"] >= 1.5)
        S = cases(m, h)
        for coin, sub in S.groupby("coin"):
            r = clt(sub, h); r["coin"] = coin; r["h"] = h; t.append(r)
        for y, sub in S.groupby("year"):
            r = clt(sub, h); r["year"] = y; r["h"] = h; t.append(r)
    out["heavy_down_by_coin_year"] = pd.DataFrame(t)
    t = []
    for h in [5, 10]:
        m = (P["r1"] > 0) & (P["vr"] >= 1.5)
        S = cases(m, h)
        S["past5"] = np.where(S["r5past"] < 0, "after_fall5", "after_rise5")
        for k, sub in S.groupby("past5"):
            r = clt(sub, h); r["grp"] = k; r["h"] = h; t.append(r)
        S["clvb"] = np.where(S["clv"] > 0.66, "highclose", "notHigh")
        for k, sub in S.groupby("clvb"):
            r = clt(sub, h); r["grp"] = k; r["h"] = h; t.append(r)
    out["heavy_up_split"] = pd.DataFrame(t)
    t = []
    for h in [5, 10]:
        m = (P["r1"] < 0) & (P["vr"] >= 1.5)
        S = cases(m, h)
        S["clvb"] = np.where(S["clv"] < 0.33, "lowclose", "notLow")
        for k, sub in S.groupby("clvb"):
            r = clt(sub, h); r["grp"] = k; r["h"] = h; t.append(r)
        S["d"] = pd.qcut(S["r1"], 2, labels=["bigfall", "smallfall"])
        for k, sub in S.groupby("d", observed=True):
            r = clt(sub, h); r["grp"] = str(k); r["h"] = h; t.append(r)
    out["heavy_down_split"] = pd.DataFrame(t)
    return out
