def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            rng = (h - l) / c.shift(1)
            mr = rng.rolling(20, min_periods=20).mean()
            r0 = c / c.shift(1) - 1
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "r0": r0, "ratio": rng / mr,
                "n1": c.shift(-1) / c - 1,
                "n2": c.shift(-2) / c.shift(-1) - 1,
                "ret10": c / c.shift(10) - 1,
                "ret20": c / c.shift(20) - 1,
                "ret40": c / c.shift(40) - 1,
                "ret60": c / c.shift(60) - 1,
                "vol20": r0.rolling(20).std(),
                "vol60": r0.rolling(60).std(),
                "regime": b["regime"].astype(str),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["u1"] = d["n1"] - d.groupby("coin")["n1"].transform("mean")
    d["u2"] = d["n2"] - d.groupby("coin")["n2"].transform("mean")
    d["day"] = d["ts"].dt.floor("D")
    d["year"] = d["ts"].dt.year
    d["inprof"] = d["regime"] != "chop"

    def tp(sub, col="u1"):
        sub = sub.dropna(subset=[col])
        n = len(sub)
        if n < 5: return [n, np.nan, np.nan, 0]
        s = sub.groupby("day")[col].sum()
        m = sub[col].mean()
        se = s.std(ddof=1) * np.sqrt(len(s)) / n
        return [n, m, m / se if se > 0 else np.nan, len(s)]

    out = {}
    up = d[(d["r0"] > 0) & d["ratio"].notna() & d["ret20"].notna()].copy()
    out_ = up[~up["inprof"]]
    # A. all up days outside profile, by ret20 quintile and wide/narrow
    out_ = out_.copy()
    out_["r20q"] = pd.qcut(out_["ret20"], 5, labels=False)
    res = []
    for (q, wd), g in out_.groupby(["r20q", out_["ratio"] > 1]):
        res.append([q, wd, g["ret20"].mean()] + tp(g) + tp(g, "u2")[1:3])
    out["outside_up_by_ret20q_wide"] = pd.DataFrame(res, columns=["r20q", "wide", "ret20", "n", "u1", "t1", "days", "u2", "t2"])
    # B. outside, ret20<-10: grading by ratio
    f = out_[out_["ret20"] < -0.1].copy()
    f["rq"] = pd.qcut(f["ratio"], 3, labels=["lo", "mid", "hi"])
    res = []
    for q, g in f.groupby("rq", observed=True):
        res.append([q, g["ratio"].mean()] + tp(g))
    out["outside_ret20neg_up_by_ratio"] = pd.DataFrame(res, columns=["rq", "ratio", "n", "u1", "t1", "days"])
    # C. same set: correlation of u1 with ratio and ret20
    out["corr_u1_ratio_f"] = float(f[["u1", "ratio"]].corr().iloc[0, 1])
    out["corr_u1_ret20_f"] = float(f[["u1", "ret20"]].corr().iloc[0, 1])
    # D. wide up days with ret20<-10 outside profile: by ret60 sign and vol ratio
    fw = f[f["ratio"] > 1].copy()
    fw["t60"] = pd.cut(fw["ret60"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    res = []
    for q, g in fw.groupby(fw["t60"].astype(str)):
        res.append([q] + tp(g))
    out["outside_wide_ret20neg_by_ret60"] = pd.DataFrame(res, columns=["t60", "n", "u1", "t1", "days"])
    fw["calm"] = (fw["vol20"] / fw["vol60"]) <= 1
    res = []
    for q, g in fw.groupby("calm"):
        res.append([q] + tp(g))
    out["outside_wide_ret20neg_by_volratio_le1"] = pd.DataFrame(res, columns=["vol20_le_vol60", "n", "u1", "t1", "days"])
    # E. by year and by coin
    res = []
    for q, g in fw.groupby("year"):
        res.append([q] + tp(g))
    out["outside_wide_ret20neg_by_year"] = pd.DataFrame(res, columns=["year", "n", "u1", "t1", "days"])
    res = []
    for q, g in fw.groupby("coin"):
        res.append([q] + tp(g))
    out["outside_wide_ret20neg_by_coin"] = pd.DataFrame(res, columns=["coin", "n", "u1", "t1", "days"])
    # F. all up days (any profile) graded by ret20 among ret20<0: correlation and terciles
    allf = up[up["ret20"] < 0].copy()
    allf["sc"] = -allf["ret20"] * allf["ratio"]
    allf["sq"] = pd.qcut(allf["sc"], 4, labels=False)
    res = []
    for q, g in allf.groupby("sq"):
        res.append([q, g["sc"].mean()] + tp(g))
    out["all_up_ret20neg_by_fall_x_width"] = pd.DataFrame(res, columns=["q", "score", "n", "u1", "t1", "days"])
    # G. 10d and 40d variants of the fall, wide up days, all profiles
    for col in ["ret10", "ret40"]:
        x = up[(up["ratio"] > 1) & up[col].notna()].copy()
        x["q"] = pd.qcut(x[col], 4, labels=False)
        res = []
        for q, g in x.groupby("q"):
            res.append([q, g[col].mean()] + tp(g))
        out["wide_up_by_" + col] = pd.DataFrame(res, columns=["q", col, "n", "u1", "t1", "days"])
    return out
