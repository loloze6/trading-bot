def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    H = 3
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); hi = df["high"].astype(float); v = df["volume"].astype(float)
            r1 = c.pct_change()
            r30 = c / c.shift(30) - 1
            r7 = c / c.shift(7) - 1
            near = c / hi.rolling(30, min_periods=10).max() - 1
            vol20 = r1.rolling(20, min_periods=10).std()
            vrel = v / v.rolling(30, min_periods=10).mean()
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, len(df), H):
                if pd.isna(fwd.iloc[i]): continue
                rows.append(dict(coin=coin, win=w, fwd=fwd.iloc[i], r1=r1.iloc[i], r7=r7.iloc[i], r30=r30.iloc[i],
                                 near=near.iloc[i], vol=vol20.iloc[i], vrel=vrel.iloc[i], wd=ts.iloc[i].weekday(),
                                 yr=ts.iloc[i].year, fc=df["forecast"].iloc[i]))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    def tab(col, q=5):
        d = g.dropna(subset=[col]).copy()
        d["b"] = d.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        t = d.groupby("b")["ex"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t.drop(columns="std")
    out = {}
    for col in ["r1", "r7", "r30", "near", "vol", "vrel"]:
        out["quintile_" + col] = tab(col)
    # spearman per coin
    sp = {}
    for col in ["r1", "r7", "r30", "near", "vrel"]:
        for coin, d in g.dropna(subset=[col]).groupby("coin"):
            sp[(col, coin)] = stats.spearmanr(d[col], d["ex"])[0]
    out["spearman_by_coin"] = pd.Series(sp).unstack()
    wdt = g.groupby("wd")["ex"].agg(["mean", "count"]); out["weekday"] = wdt
    out["year"] = g.groupby("yr")["ex"].agg(["mean", "count"])
    # interaction: near high x volume
    d = g.dropna(subset=["near", "vrel"]).copy()
    d["nb"] = pd.qcut(d["near"].rank(method="first"), 3, labels=False)
    d["vb"] = pd.qcut(d["vrel"].rank(method="first"), 3, labels=False)
    out["near_x_vrel_mean"] = d.pivot_table(index="nb", columns="vb", values="ex", aggfunc="mean")
    # vol-scaled r1
    g2 = g.dropna(subset=["r1", "vol"]).copy(); g2["z"] = g2["r1"] / g2["vol"]
    g2["zb"] = pd.cut(g2["z"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["z1_bins"] = g2.groupby("zb")["ex"].agg(["mean", "count"])
    # book daily
    br = []
    for coin, ws in days.items():
        for w, df in ws.items():
            br.append(df[["book_return", "coin_return"]].assign(coin=coin, win=w))
    b = pd.concat(br).dropna()
    bd = b.groupby(["win"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    out["book_by_window"] = bd
    return out
