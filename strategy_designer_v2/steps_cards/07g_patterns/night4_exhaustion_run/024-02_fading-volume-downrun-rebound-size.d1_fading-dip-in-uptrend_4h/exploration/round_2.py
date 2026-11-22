def explore(data):
    import numpy as np, pandas as pd
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(180, min_periods=60).std()
            n = len(b)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w,
                               "r6_sd": (c / c.shift(6) - 1) / (sd * np.sqrt(6)),
                               "r1_sd": r1 / sd,
                               "r180": c / c.shift(180) - 1,
                               "fwd": c.shift(-H) / c - 1, "fwd6": c.shift(-6) / c - 1,
                               "nxt": c.shift(-1) / c - 1,
                               "hour": ts.dt.hour, "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "grid": (np.arange(n) % H == 0), "grid6": (np.arange(n) % 6 == 0)})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def s1(g, col="nxt"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean_bp": 1e4 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    # hour effect robustness
    out["h16_by_coin"] = A[A.hour == 16].groupby("coin").apply(s1)
    out["h16_by_year"] = A[A.hour == 16].groupby("yr").apply(s1)
    out["h20_by_coin"] = A[A.hour == 20].groupby("coin").apply(s1)
    out["h20_by_year"] = A[A.hour == 20].groupby("yr").apply(s1)
    out["fri_by_coin"] = A[A.wd == 4].groupby("coin").apply(s1)
    out["fri_by_year"] = A[A.wd == 4].groupby("yr").apply(s1)
    out["fri_by_hour"] = A[A.wd == 4].groupby("hour").apply(s1)
    out["nonfri_by_hour"] = A[A.wd != 4].groupby("hour").apply(s1)
    # demeaned hour-16 bar: excess over coin mean bar return
    mb = A.groupby("coin")["nxt"].mean()
    A["nx_ex"] = A["nxt"] - A["coin"].map(mb)
    # graded: does the previous bar's (12-16) move predict the 16-20 bar?
    H16 = A[A.hour == 16].dropna(subset=["r1_sd", "nxt"])
    out["h16_by_prevbar_quint"] = H16.groupby(pd.qcut(H16.r1_sd, 5, labels=False)).apply(s1)
    # U-shape of 6-bar move
    G = A[A.grid].dropna(subset=["fwd", "r6_sd"]).copy()
    drift = A[A.grid].groupby("coin")["fwd"].mean(); usual = A[A.grid].groupby("coin")["fwd"].std()
    G["exs"] = (G["fwd"] - G["coin"].map(drift)) / G["coin"].map(usual)
    def sm(g):
        x = g["exs"].dropna()
        return pd.Series({"n": len(x), "strength": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    G["absq"] = pd.qcut(G.r6_sd.abs(), 10, labels=False)
    out["abs_r6_decile"] = G.groupby("absq").apply(sm)
    G["ext"] = np.where(G.r6_sd <= G.r6_sd.quantile(0.1), "bigfall", np.where(G.r6_sd >= G.r6_sd.quantile(0.9), "bigrise", "mid"))
    out["ext_by_coin"] = G[G.ext != "mid"].groupby(["ext", "coin"]).apply(sm)
    out["ext_by_year"] = G[G.ext != "mid"].groupby(["ext", "yr"]).apply(sm)
    F = G[G.ext == "bigfall"]
    out["bigfall_depth_tercile"] = F.groupby(pd.qcut(F.r6_sd, 3, labels=False)).apply(sm)
    R = G[G.ext == "bigrise"]
    out["bigrise_size_tercile"] = R.groupby(pd.qcut(R.r6_sd, 3, labels=False)).apply(sm)
    # book days by weekday
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d.copy(); dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday; D.append(dd)
    D = pd.concat(D)
    out["book_by_weekday"] = D.groupby("wd")["book_return"].agg(["count", "mean"]).assign(mean=lambda x: 1e4 * x["mean"])
    return out
