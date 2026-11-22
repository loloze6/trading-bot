def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; rows24 = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); v = df["volume"].astype(float)
            r1 = c.pct_change()
            mabs = r1.abs().rolling(720, min_periods=240).mean()
            vr = v / v.rolling(720, min_periods=240).mean()
            vol = r1.rolling(168, min_periods=100).std()
            ts = pd.to_datetime(df["timestamp"])
            wn = int(w[1:])
            g = pd.DataFrame({"coin": coin, "wn": wn, "yr": ts.dt.year, "sc": r1 / mabs, "vr": vr,
                              "vol": vol, "f4": c.shift(-4) / c - 1, "f2": c.shift(-2) / c - 1,
                              "f6": c.shift(-6) / c - 1, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                              "r24p": (c / c.shift(24) - 1) / (mabs * np.sqrt(24)),
                              "f24": c.shift(-24) / c - 1})
            rows.append(g.iloc[np.arange(0, len(df), 4)])
            rows24.append(g.iloc[np.arange(0, len(df), 24)])
    A = pd.concat(rows).dropna(subset=["f4", "f2", "f6", "sc", "vr", "vol"])
    for h in ["f2", "f4", "f6"]:
        A["u" + h] = A[h] - A.groupby("coin")[h].transform("mean")
    A["dir"] = np.sign(A["sc"])
    A["half"] = np.where(A["wn"] <= 12, "w1-12", "w13-24")
    A["volq"] = A.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 5, labels=False))
    def tab(gb, col):
        t = gb[col].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t.drop(columns="std")
    # reversal of large moves in the high-vol quintile: robustness
    H = A[(A["volq"] == 4) & (A["sc"].abs() > 2)].copy()
    for h in ["uf2", "uf4", "uf6"]:
        H["s" + h] = H[h] * H["dir"]
    out["hivol_big_cont_by_horizon"] = pd.DataFrame({h: [H["s" + h].mean(), H["s" + h].mean() / H["s" + h].std() * np.sqrt(len(H)), len(H)] for h in ["uf2", "uf4", "uf6"]}, index=["mean", "t", "n"])
    out["hivol_big_cont4_by_coin_half"] = tab(H.groupby(["coin", "half"]), "suf4")
    out["hivol_big_cont4_by_dir"] = tab(H.groupby("dir"), "suf4")
    # graded: across all bars, slope of continuation on scaled move, per vol quintile
    rs = []
    for q, g in A.groupby("volq"):
        sl = stats.linregress(g["sc"].clip(-8, 8), g["uf4"])
        rs.append([q, sl.slope, sl.slope / sl.stderr, len(g)])
    out["slope_uf4_on_sc_by_volq"] = pd.DataFrame(rs, columns=["volq", "slope", "t", "n"]).set_index("volq")
    rs = []
    for key, g in A[A["volq"] == 4].groupby(["coin", "half"]):
        sl = stats.linregress(g["sc"].clip(-8, 8), g["uf4"])
        rs.append([str(key), sl.slope, sl.slope / sl.stderr, len(g)])
    out["slope_hivol_by_coin_half"] = pd.DataFrame(rs, columns=["k", "slope", "t", "n"]).set_index("k")
    # heavy-volume down hours
    D = A[(A["dir"] < 0) & (A["sc"].abs() > 2)].copy()
    D["vb"] = pd.cut(D["vr"], [0, 1, 2, 4, 8, 1e9])
    out["down_big_u4_by_vr"] = tab(D.groupby("vb", observed=True), "uf4")
    # daily reversal
    B = pd.concat(rows24).dropna(subset=["f24", "r24p"])
    B["u24"] = B["f24"] - B.groupby("coin")["f24"].transform("mean")
    B["half"] = np.where(B["wn"] <= 12, "w1-12", "w13-24")
    rs = []
    for key, g in B.groupby(["coin", "half"]):
        sl = stats.linregress(g["r24p"].clip(-5, 5), g["u24"])
        rs.append([str(key), sl.slope, sl.slope / sl.stderr, len(g)])
    sl = stats.linregress(B["r24p"].clip(-5, 5), B["u24"])
    rs.append(["all", sl.slope, sl.slope / sl.stderr, len(B)])
    out["slope_u24_on_past24"] = pd.DataFrame(rs, columns=["k", "slope", "t", "n"]).set_index("k")
    # hour 0 and Thursday robustness
    out["hour0_by_coin_half"] = tab(A[A["hour"] == 0].groupby(["coin", "half"]), "uf4")
    out["thu_by_coin_half"] = tab(A[A["wd"] == 3].groupby(["coin", "half"]), "uf4")
    out["thu_by_year"] = tab(A[A["wd"] == 3].groupby("yr"), "uf4")
    return out
