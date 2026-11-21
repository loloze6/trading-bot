def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for c, wins in data["bars"].items():
        cm5 = []
        for w, b in wins.items():
            cl = b["close"].values
            for i in range(0, len(cl) - 5, 5):
                cm5.append(cl[i + 5] / cl[i] - 1)
        cm5 = np.mean(cm5)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            pos = b["postRebalance_current_allocation"].fillna(0)
            r1 = b["close"].shift(-1) / b["close"] - 1
            r5 = b["close"].shift(-5) / b["close"] - 1
            ret28 = b["close"] / b["close"].shift(28) - 1
            ret90 = b["close"] / b["close"].shift(90) - 1
            lr = np.log(b["close"]).diff()
            vol30 = lr.rolling(30).std() * np.sqrt(365)
            hi90 = b["close"] / b["close"].rolling(90, min_periods=30).max() - 1
            grid = (np.arange(len(b)) % 5 == 0)
            df = pd.DataFrame({"coin": c, "wn": int(w[1:]), "pos": pos, "g": pos * r1, "r5": r5,
                               "t5": np.sign(pos) * (r5 - cm5), "ret28": ret28, "ret90": ret90,
                               "vol30": vol30, "hi90": hi90, "grid": grid, "side": np.sign(pos)})
            rows.append(df)
    B = pd.concat(rows).dropna(subset=["g"])
    B["stretch"] = np.where(B["wn"].between(14, 18), "w14-18", np.where(B["wn"] >= 19, "w19-24", "w1-13"))
    out["by_stretch_side"] = B.groupby(["stretch", "side"]).agg(n=("g", "size"), gain=("g", "mean"),
                                                                 sum_gain=("g", "sum")).unstack()
    B["up28"] = np.sign(B["ret28"])
    out["side_by_trend28"] = B.groupby(["up28", "side"])["g"].agg(["size", "mean"]).unstack()
    B["up90"] = np.sign(B["ret90"])
    out["side_by_trend90"] = B.groupby(["up90", "side"])["g"].agg(["size", "mean"]).unstack()
    G = B[B["grid"] & (B["side"] != 0)].dropna(subset=["t5", "ret28"])
    def tstat(x):
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out["t5_by_trend28_side"] = G.groupby(["up28", "side"])["t5"].apply(tstat).unstack()
    G["aligned"] = (np.sign(G["ret28"]) == G["side"]).astype(int)
    out["t5_aligned"] = G.groupby("aligned")["t5"].apply(tstat).unstack()
    G["q28"] = pd.qcut(G["ret28"] * G["side"], 5, labels=False)
    out["t5_by_signed_trend_q"] = G.groupby("q28")["t5"].apply(tstat).unstack()
    G["hq"] = pd.qcut(G["hi90"], 4, labels=False)
    out["t5_by_hi90_side"] = G.groupby(["hq", "side"])["t5"].mean().unstack()
    out["share_short_stretch"] = B.groupby("stretch")["side"].apply(lambda s: (s < 0).mean())
    return out
