def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            for h in (1, 2, 3, 5):
                df[f"f{h}"] = c.shift(-h) / c - 1
            df["s1"] = r1 / sd30
            df["s2"] = (c / c.shift(2) - 1) / (sd30 * np.sqrt(2))
            df["s3"] = (c / c.shift(3) - 1) / (sd30 * np.sqrt(3))
            df["s10"] = (c / c.shift(10) - 1) / (sd30 * np.sqrt(10))
            df["t60"] = c / c.shift(60) - 1
            df["coin"] = coin; df["win"] = w
            df["pos"] = np.arange(len(df))
            df["yr"] = pd.to_datetime(df["timestamp"]).dt.year
            df["day"] = pd.to_datetime(df["timestamp"]).dt.floor("D")
            df["fa"] = (df["regime"] == "unknown").astype(int)
            rows.append(df[["coin","win","pos","f1","f2","f3","f5","s1","s2","s3","s10","t60","yr","day","fa"]])
    A = pd.concat(rows, ignore_index=True)
    for h in (1, 2, 3, 5):
        dr = A[A.pos % h == 0].groupby("coin")[f"f{h}"].mean()
        A[f"x{h}"] = A[f"f{h}"] - A["coin"].map(dr)
    def clus(d, x, y):
        d = d.dropna(subset=[x, y])
        if len(d) < 20: return pd.Series({"n": len(d)})
        X = d[x] - d[x].mean()
        b = (X * d[y]).sum() / (X ** 2).sum()
        a = d[y].mean() - b * d[x].mean()
        e = d[y] - a - b * d[x]
        g = (X * e).groupby(d["day"]).sum()
        se = np.sqrt((g ** 2).sum()) / (X ** 2).sum()
        gm = (d[y] - d[y].mean()).groupby(d["day"]).sum()
        tm = d[y].mean() / (np.sqrt((gm ** 2).sum()) / len(d))
        return pd.Series({"n": len(d), "days": d["day"].nunique(), "slope": b, "t_slope": b / se, "mean": d[y].mean(), "t_mean_day": tm})
    out = {}
    res = {}
    for sig in ("s1", "s2", "s3"):
        for h in (1, 2, 3, 5):
            G = A[(A.pos % h == 0) & (A.fa == 1)]
            res[f"fa1_{sig}>0_x{h}"] = clus(G[G[sig] > 0], sig, f"x{h}")
            res[f"fa1_{sig}<0_x{h}"] = clus(G[G[sig] < 0], sig, f"x{h}")
    out["fa1_slopes"] = pd.DataFrame(res).T.round(4)
    # by year, next-day after up day in fa1
    G = A[(A.fa == 1) & (A.s1 > 0)].dropna(subset=["x1"])
    out["fa1_up_day_next_by_year"] = G.groupby("yr").apply(lambda d: pd.Series({"n": len(d), "mean": d.x1.mean(), "corr": d.s1.corr(d.x1)})).round(4)
    G = A[(A.fa == 1) & (A.s1 < 0)].dropna(subset=["x1"])
    out["fa1_down_day_next_by_year"] = G.groupby("yr").apply(lambda d: pd.Series({"n": len(d), "mean": d.x1.mean(), "corr": d.s1.corr(d.x1)})).round(4)
    # outside profile, by trend bucket (60d return computable)
    B = A[(A.fa == 0)].dropna(subset=["t60"]).copy()
    B["tr"] = np.where(B.t60 > 0.10, "rising", np.where(B.t60 < -0.10, "falling", "choppy"))
    res2 = {}
    for tr in ("rising", "choppy", "falling"):
        for sig in ("s3", "s10"):
            G = B[(B.pos % 5 == 0) & (B.tr == tr)]
            res2[f"{tr}_{sig}_all_x5"] = clus(G, sig, "x5")
            res2[f"{tr}_{sig}>0_x5"] = clus(G[G[sig] > 0], sig, "x5")
            res2[f"{tr}_{sig}<0_x5"] = clus(G[G[sig] < 0], sig, "x5")
    out["fa0_by_trend"] = pd.DataFrame(res2).T.round(4)
    return out
