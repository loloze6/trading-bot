def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; a = b["postRebalance_current_allocation"]
            nxt = cl.shift(-1)/cl - 1
            dr = cl.pct_change()
            df = pd.DataFrame({"coin": c, "w": w, "a": a, "g": a*nxt, "fc": b["forecast"],
                               "r30": cl/cl.shift(30)-1, "r90": cl/cl.shift(90)-1,
                               "r5": cl/cl.shift(5)-1,
                               "vol20": dr.rolling(20).std(),
                               "dd60": cl/cl.rolling(60).max()-1})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["wn"] = D["w"].str[1:].astype(int)
    D = D.dropna(subset=["g"])
    D = D[D["a"] != 0]
    D["side"] = np.where(D["a"] > 0, "long", "short")
    D["era"] = np.where(D["wn"] <= 9, "w1-w9", "w10-w24")
    out = {}
    # gain per side per era, per coin-bar mean and summed per coin-day mean
    out["side_era"] = D.groupby(["era", "side"])["g"].agg(["size", "mean", "std", "min"]).round(5)
    # per window summed gain by side (divided by 6 coins ~ book contribution)
    S = D.groupby(["wn", "side"])["g"].sum().unstack().div(6).round(3)
    out["window_side_sum"] = S
    # shorts: by forecast strength quintile and by the 90-day return
    Sh = D[D["side"] == "short"].copy()
    Lo = D[D["side"] == "long"].copy()
    def tab(X, col, q=5):
        X = X.dropna(subset=[col]).copy()
        X["_b"] = pd.qcut(X[col].rank(method="first"), q, labels=False)
        t = X.groupby("_b").agg(n=("g", "size"), mean_g=("g", "mean"), sd=("g", "std"),
                                lo=(col, "min"), hi=(col, "max"), abs_a=("a", lambda s: s.abs().mean()))
        t["t"] = t["mean_g"]/(t["sd"]/np.sqrt(t["n"]))
        return t.round(5)
    out["short_by_r90"] = tab(Sh, "r90")
    out["short_by_dd60"] = tab(Sh, "dd60")
    out["short_by_vol20"] = tab(Sh, "vol20")
    out["long_by_r90"] = tab(Lo, "r90")
    out["long_by_dd60"] = tab(Lo, "dd60")
    # shorts after a large 5-day rise against them (squeeze)
    out["short_by_r5"] = tab(Sh, "r5")
    return out
