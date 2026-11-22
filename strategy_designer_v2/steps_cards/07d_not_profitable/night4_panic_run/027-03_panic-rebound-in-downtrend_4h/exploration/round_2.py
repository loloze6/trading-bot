import pandas as pd, numpy as np

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            rng = (b["high"] - b["low"]) / c
            rr = rng.rolling(6).mean() / rng.rolling(180).mean()
            prior = c.shift(6) / c.shift(186) - 1
            r6 = c / c.shift(6) - 1
            fallz = r6 / r6.abs().rolling(180).mean()
            r36 = c / c.shift(36) - 1
            fall6d = r36 / r36.abs().rolling(180).mean()
            for h in (42, 84):
                fwd = c.shift(-h) / c - 1
                for off in (0, h // 2):
                    idx = np.arange(off, len(b), h)
                    g = pd.DataFrame({"rr": rr.iloc[idx].values, "prior": prior.iloc[idx].values,
                                      "fallz": fallz.iloc[idx].values, "fall6d": fall6d.iloc[idx].values,
                                      "fwd": fwd.iloc[idx].values})
                    g["coin"] = coin; g["win"] = w; g["h"] = h; g["off"] = off
                    rows.append(g)
    G = pd.concat(rows).dropna()
    G["unus"] = G["fwd"] - G.groupby(["coin", "h", "off"])["fwd"].transform("mean")
    G["panic"] = (-G["fallz"]).clip(lower=0) * G["rr"]
    G["f_b"] = pd.cut(G["fallz"], [-100, -3, -2, -1, 0, 100])
    G["p_b"] = pd.cut(G["panic"], [-1, 0, 1, 2, 4, 8, 1000])
    G["f6_b"] = pd.cut(G["fall6d"], [-100, -3, -2, -1, 0, 100])
    def summ(df, key):
        o = df.groupby(key, observed=True)["unus"].agg(["count", "mean", "std"])
        o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
        o["total"] = df.groupby(key, observed=True)["fwd"].mean()
        return o.round(4)
    res = {}
    g0 = G[G["off"] == 0]
    res["fallz by h"] = summ(g0, ["h", "f_b"])
    res["panic score by h"] = summ(g0, ["h", "p_b"])
    res["6-day fall by h"] = summ(g0, ["h", "f6_b"])
    res["panic score h84 offset half"] = summ(G[(G["off"] == 42) & (G["h"] == 84)], "p_b")
    res["fallz<=-2 h84 by prior_neg"] = summ(g0[(g0["h"] == 84) & (g0["fallz"] <= -2)], g0["prior"] < 0)
    res["fallz<=-2 h84 by coin"] = summ(g0[(g0["h"] == 84) & (g0["fallz"] <= -2)], "coin")
    # book's deepest falls
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; D.append(d)
    D = pd.concat(D)
    res["book daily ret quantiles"] = D["book_return"].describe(percentiles=[0.01, 0.05, 0.5, 0.95, 0.99]).round(5)
    res["worst book days coin_ret mean"] = D.nsmallest(20, "book_return")[["book_return", "coin_return"]].mean()
    return res
