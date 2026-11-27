def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","open","high","low","close","regime","postRebalance_current_allocation"]].copy().reset_index(drop=True)
            c = d["close"]
            d["r1"] = c.pct_change()
            d["ret30"] = c / c.shift(30) - 1
            d["ret7p"] = c / c.shift(7) - 1
            d["vol30"] = d["r1"].rolling(30, min_periods=20).std()
            d["z1"] = d["r1"] / d["vol30"].shift(1)
            d["range_pos"] = (d["close"] - d["low"]) / (d["high"] - d["low"]).replace(0, np.nan)
            for h in (1, 3, 7, 21):
                d[f"f{h}"] = c.shift(-h) / c - 1
            d["pos"] = np.arange(len(d))
            d["coin"] = coin; d["win"] = w
            d["wd"] = pd.to_datetime(d["timestamp"]).dt.weekday
            d["year"] = pd.to_datetime(d["timestamp"]).dt.year
            d["choppy"] = (d["regime"] == "mean_reversion")
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def grid(h):
        g = A[A["pos"] % h == 0].dropna(subset=[f"f{h}"]).copy()
        drift = g.groupby("coin")[f"f{h}"].mean()
        g["ex"] = g[f"f{h}"] - g["coin"].map(drift)
        return g
    def tab(g, key, q=5):
        g = g.dropna(subset=[key]).copy()
        g["q"] = pd.qcut(g[key].rank(method="first"), q, labels=False)
        r = g.groupby("q").agg(n=("ex","size"), key_mean=(key,"mean"), ex_mean=("ex","mean"), ex_std=("ex","std"))
        r["t"] = r["ex_mean"] / (r["ex_std"] / np.sqrt(r["n"]))
        return r.round(4)
    for h in (7, 21):
        g = grid(h)
        for reg, sub in (("choppy", g[g.choppy]), ("other", g[~g.choppy])):
            out[f"ret30 quintile -> ex{h}, {reg}"] = tab(sub, "ret30")
        out[f"ret7p quintile -> ex{h}, all"] = tab(g, "ret7p")
        out[f"vol30 quintile -> ex{h}, all"] = tab(g, "vol30")
    g3 = grid(3)
    out["z1 quintile -> ex3, all"] = tab(g3, "z1")
    out["range_pos quintile -> ex3, all"] = tab(g3, "range_pos")
    g1 = grid(1)
    out["z1 decile -> ex1, all"] = tab(g1, "z1", 10)
    wd = A.dropna(subset=["r1"]).groupby("wd")["r1"].agg(["size","mean","std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["size"]))
    out["weekday daily return"] = wd.round(5)
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df[["day","book_return","coin_return"]].copy(); x["coin"]=coin; x["win"]=w; D.append(x)
    D = pd.concat(D, ignore_index=True).dropna()
    bk = D.groupby(["win","day"])[["book_return","coin_return"]].mean().reset_index()
    out["book by window"] = bk.groupby("win")[["book_return","coin_return"]].agg(["mean","size"]).round(5)
    lo, hi = bk["book_return"].quantile([0.02, 0.98])
    out["book extreme days coin return"] = pd.DataFrame({
        "n": [ (bk.book_return<=lo).sum(), (bk.book_return>=hi).sum()],
        "coin_ret_mean": [bk.loc[bk.book_return<=lo,"coin_return"].mean(), bk.loc[bk.book_return>=hi,"coin_return"].mean()],
        "book_ret_mean": [bk.loc[bk.book_return<=lo,"book_return"].mean(), bk.loc[bk.book_return>=hi,"book_return"].mean()]}, index=["worst2%","best2%"]).round(5)
    out["share choppy bars"] = float(A["choppy"].mean())
    return out
