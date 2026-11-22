def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]; days = data["days"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy().reset_index(drop=True)
            cl = b["close"]
            a = b["postRebalance_current_allocation"]
            nxt = cl.shift(-1)/cl - 1
            g = a*nxt
            r30 = cl/cl.shift(30)-1
            r10 = cl/cl.shift(10)-1
            r5 = cl/cl.shift(5)-1
            dr = cl.pct_change()
            vol20 = dr.rolling(20).std()
            vol60 = dr.rolling(60).std()
            df = pd.DataFrame({"coin": c, "w": w, "i": np.arange(len(b)), "ts": b["timestamp"],
                               "a": a, "g": g, "nxt": nxt, "fc": b["forecast"],
                               "r30": r30, "r10": r10, "r5": r5, "vr": vol20/vol60,
                               "vol20": vol20})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["wn"] = D["w"].str[1:].astype(int)
    D["side"] = np.sign(D["a"])
    # book daily: mean over coins of book_return
    br = []
    for c in days:
        for w, d in days[c].items():
            x = d[["day", "book_return", "coin_return"]].copy(); x["coin"] = c; x["w"] = w
            br.append(x)
    B = pd.concat(br, ignore_index=True)
    B["wn"] = B["w"].str[1:].astype(int)
    P = B.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wn", "day"])
    P = P.dropna()
    P["val"] = (1+P["book_return"]).cumprod()
    P["peak"] = P["val"].cummax()
    P["dd"] = P["val"]/P["peak"]-1
    out = {}
    out["maxdd"] = float(P["dd"].min())
    out["years"] = float(len(P)/365)
    out["yearly"] = float(P["val"].iloc[-1]**(365/len(P))-1)
    # per window: book return, coin return, worst in-window dd
    def wdd(s):
        v = (1+s).cumprod(); return float((v/v.cummax()-1).min())
    W = P.groupby("wn").agg(book=("book_return", lambda s: (1+s).prod()-1),
                           hold=("coin_return", lambda s: (1+s).prod()-1),
                           dd_end=("dd", "last"), dd_min=("dd", "min"))
    W["in_dd"] = P.groupby("wn")["book_return"].apply(wdd)
    out["windows"] = W.round(3)
    # gains by situation (per coin-bar)
    E = D.dropna(subset=["g", "r30", "r5", "vr"]).copy()
    E = E[E["a"] != 0]
    E["sgn_r5"] = np.sign(E["a"])*E["r5"]  # last 5d move in position direction
    E["sgn_r10"] = np.sign(E["a"])*E["r10"]
    def tab(col, q=5):
        E["_b"] = E.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = E.groupby("_b").agg(n=("g", "size"), mean_g=("g", "mean"), sd=("g", "std"),
                                min_g=("g", "min"), share_long=("side", lambda s: (s > 0).mean()),
                                abs_a=("a", lambda s: s.abs().mean()))
        t["t"] = t["mean_g"]/(t["sd"]/np.sqrt(t["n"]))
        t["p5"] = E.groupby("_b")["g"].quantile(0.05)
        return t.round(5)
    out["by_side"] = E.groupby("side")["g"].agg(["size", "mean", "std", "min"]).round(5)
    out["by_vr"] = tab("vr")
    out["by_sgn_r5"] = tab("sgn_r5")
    out["by_sgn_r10"] = tab("sgn_r10")
    out["by_absfc"] = tab("fc")
    out["by_vol20"] = tab("vol20")
    return out
