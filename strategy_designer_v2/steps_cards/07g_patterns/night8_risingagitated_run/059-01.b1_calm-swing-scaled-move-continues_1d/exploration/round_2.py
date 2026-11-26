def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20).std()
            sd5 = r1.rolling(5).std()
            ret20 = c / c.shift(20) - 1
            ret10 = c / c.shift(10) - 1
            ret5p = c / c.shift(5) - 1
            ret60 = c / c.shift(60) - 1
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "sc20": ret20 / (sd20 * np.sqrt(20)),
                "sc10": ret10 / (sd20 * np.sqrt(10)),
                "sc5": ret5p / (sd20 * np.sqrt(5)),
                "ret5p": ret5p, "ret60": ret60,
                "fwd5": c.shift(-5) / c - 1,
                "fwd10": c.shift(-10) / c - 1,
                "calm": (b["regime"] != "chop").values,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    for h in (5, 10):
        dr = A.groupby("coin").apply(lambda d: d[d.pos % h == 0][f"fwd{h}"].mean())
        sd = A.groupby("coin").apply(lambda d: d[d.pos % h == 0][f"fwd{h}"].std())
        A[f"ex{h}"] = A[f"fwd{h}"] - A.coin.map(dr)
        A[f"sd{h}"] = A.coin.map(sd)
    A["trend"] = np.where(A.ret60 > 0.10, "rising", np.where(A.ret60 < -0.10, "falling", np.where(A.ret60.isna(), "na", "choppy")))
    A["agit"] = np.where(A.calm, "calm", "agit")

    def clus_slope(d, x, y):
        d = d.dropna(subset=[x, y])
        if len(d) < 30: return pd.Series({"n": len(d), "days": np.nan, "slope": np.nan, "t_cl": np.nan, "size%": np.nan, "size_t": np.nan, "strength": np.nan})
        X = d[x].values; Y = d[y].values
        xm = X - X.mean(); b = (xm * (Y - Y.mean())).sum() / (xm ** 2).sum()
        a = Y.mean() - b * X.mean(); e = Y - a - b * X
        g = pd.Series(xm * e).groupby(d["day"].values).sum()
        se = np.sqrt((g ** 2).sum()) / (xm ** 2).sum()
        dirr = Y * np.sign(X)
        gd = pd.Series(dirr - dirr.mean()).groupby(d["day"].values).sum()
        st = dirr.mean() / (np.sqrt((gd ** 2).sum()) / len(dirr))
        strength = np.mean(dirr / d[y.replace("ex", "sd")].values)
        return pd.Series({"n": len(d), "days": d.day.nunique(), "slope": b, "t_cl": b / se, "size%": 100 * dirr.mean(), "size_t": st, "strength": strength})

    out = {}
    G5 = A[A.pos % 5 == 0]
    G10 = A[A.pos % 10 == 0]
    for x in ("sc20", "sc10", "sc5"):
        out[f"{x}_fwd5_by_profile"] = G5.groupby(["trend", "agit"]).apply(lambda d: clus_slope(d, x, "ex5"))
    out["sc20_fwd10_by_profile"] = G10.groupby(["trend", "agit"]).apply(lambda d: clus_slope(d, "sc20", "ex10"))
    CC = G5[(G5.trend == "choppy") & G5.calm]
    out["choppycalm_sc20_by_year"] = CC.groupby("year").apply(lambda d: clus_slope(d, "sc20", "ex5"))
    out["choppycalm_sc20_by_coin"] = CC.groupby("coin").apply(lambda d: clus_slope(d, "sc20", "ex5"))
    CC2 = CC.dropna(subset=["sc20", "ex5"]).copy()
    CC2["q"] = pd.qcut(CC2.sc20, 4, labels=False)
    out["choppycalm_ex5_by_sc20_quart"] = CC2.groupby("q")["ex5"].agg(["count", "mean"]).assign(mean=lambda d: d["mean"] * 100)
    CA = G5[G5.calm].dropna(subset=["sc5", "ex5"]).copy()
    out["calm_sc5_by_year"] = CA.groupby("year").apply(lambda d: clus_slope(d, "sc5", "ex5"))
    out["calm_sc5_by_coin"] = CA.groupby("coin").apply(lambda d: clus_slope(d, "sc5", "ex5"))
    CA["q"] = pd.qcut(CA.sc5, 5, labels=False)
    out["calm_ex5_by_sc5_quint"] = CA.groupby("q")["ex5"].agg(["count", "mean"]).assign(mean=lambda d: d["mean"] * 100)
    out["all_sc20_fwd5"] = clus_slope(G5, "sc20", "ex5").to_frame("all").T
    return out
