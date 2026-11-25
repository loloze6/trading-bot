def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            ts = pd.to_datetime(b["timestamp"])
            d["day"] = ts.dt.floor("D").astype("int64")
            d["year"] = ts.dt.year
            d["r1"] = r1
            d["r7"] = c / c.shift(7) - 1
            d["r30"] = c / c.shift(30) - 1
            d["er"] = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            d["vol30"] = r1.rolling(30).std()
            d["z7"] = d["r7"] / (d["vol30"] * np.sqrt(7))
            d["z1"] = r1 / d["vol30"].shift(1)
            d["f1"] = c.shift(-1) / c - 1
            d["f3"] = c.shift(-3) / c - 1
            d["f7"] = c.shift(-7) / c - 1
            d["f14"] = c.shift(-14) / c - 1
            d["volrank"] = d["vol30"].rolling(180, min_periods=60).rank(pct=True)
            d["agree"] = np.sign(d["r7"]) == np.sign(d["r30"])
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    def daytt(g, col):
        s = g.groupby("day")[col].sum()
        return pd.Series({"cases": g[col].notna().sum(), "days": len(s), "mean_case": g[col].mean(), "t_day": s.mean() / (s.std() / np.sqrt(len(s)))})
    for h, fc in [(3, "f3"), (7, "f7"), (14, "f14")]:
        G = D[D["pos"] % h == 0].dropna(subset=[fc, "z7", "er"]).copy()
        mu = G.groupby("coin")[fc].mean()
        G["x"] = G[fc] - G["coin"].map(mu)
        G["sx"] = np.sign(G["z7"]) * G["x"]
        G["wsx"] = G["z7"] * G["x"]  # graded
        G["lowER"] = np.where(G["er"] < G["er"].median(), "lowER", "highER")
        res = {}
        for k, g in G.groupby("lowER"):
            res[k + "_signed"] = daytt(g, "sx")
            res[k + "_graded"] = daytt(g, "wsx")
        for k, g in G.groupby(["lowER", "agree"]):
            res[f"{k[0]}_agree{k[1]}_graded"] = daytt(g, "wsx")
        out[f"h{h}_z7_continuation"] = pd.DataFrame(res).T
        if h == 7:
            lo = G[G["lowER"] == "lowER"]
            out["h7_lowER_graded_by_year"] = lo.groupby("year").apply(lambda g: daytt(g, "wsx"))
            out["h7_lowER_graded_by_coin"] = lo.groupby("coin").apply(lambda g: daytt(g, "wsx"))
            lo2 = lo.copy(); lo2["zb"] = pd.qcut(lo2["z7"].abs(), 3, labels=["small", "mid", "big"])
            out["h7_lowER_signed_by_absz"] = lo2.groupby("zb").apply(lambda g: daytt(g, "sx"))
            out["h7_strength_lowER"] = pd.Series({"usual_move_sd": G["x"].std(), "mean_signed": lo["sx"].mean(), "strength": (lo["sx"] / G.groupby("coin")[fc].transform("std").loc[lo.index]).mean()})
    # daily reversal after big down days, day-clustered, graded by z1 on down side
    A = D.dropna(subset=["f1", "z1", "volrank"]).copy()
    A["x1"] = A["f1"] - A["coin"].map(A.groupby("coin")["f1"].mean())
    A["neg_z1_x"] = -A["z1"] * A["x1"]
    A["vb"] = pd.cut(A["volrank"], [0, 0.5, 1.0], labels=["lowvol", "highvol"])
    A["dir"] = np.where(A["z1"] > 0, "up", "down")
    out["1d_reversal_graded_by_vol_dir"] = A.groupby(["vb", "dir"]).apply(lambda g: daytt(g, "neg_z1_x"))
    out["1d_reversal_by_year"] = A[A["vb"] == "highvol"].groupby("year").apply(lambda g: daytt(g, "neg_z1_x"))
    A["wdm"] = (pd.to_datetime(A["day"]).dt.weekday)
    out["weekday_by_year_x1"] = A.groupby(["year", "wdm"])["x1"].mean().unstack()
    return out
