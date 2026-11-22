def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    H = 5
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            if n < 40: continue
            lr = pd.Series(c)
            r1 = lr.pct_change()
            ret30 = lr / lr.shift(30) - 1
            ret5p = lr / lr.shift(5) - 1
            ret1 = r1
            vol20 = r1.rolling(20).std()
            hi30 = lr.rolling(30).max(); lo30 = lr.rolling(30).min()
            pos = (lr - (hi30 + lo30) / 2) / (hi30 - lo30)  # -0.5..0.5
            eff = (lr - lr.shift(30)).abs() / (lr.diff().abs().rolling(30).sum())
            ts = pd.to_datetime(df["timestamp"])
            for t in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, fc=df["forecast"].iloc[t],
                                 fwd=c[t + H] / c[t] - 1, ret30=ret30.iloc[t], ret5p=ret5p.iloc[t],
                                 ret1=ret1.iloc[t], vol20=vol20.iloc[t], pos=pos.iloc[t], eff=eff.iloc[t],
                                 wd=ts.iloc[t].dayofweek, yr=ts.iloc[t].year,
                                 alloc=df["postRebalance_current_allocation"].iloc[t]))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["z1"] = g["ret1"] / g["vol20"]
    out = {}
    def tab(col, q=5):
        d = g.dropna(subset=[col, "ex"]).copy()
        d["b"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        a = d.groupby("b")["ex"].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.round(5)
    out["fc quintile -> ex5"] = tab("fc")
    out["ret5p quintile -> ex5"] = tab("ret5p")
    out["z1 (last day move/vol) quintile -> ex5"] = tab("z1")
    out["vol20 quintile -> ex5"] = tab("vol20")
    out["range pos quintile -> ex5"] = tab("pos")
    out["efficiency quintile -> ex5"] = tab("eff")
    # range pos slope within flat vs trending (efficiency halves)
    d = g.dropna(subset=["pos", "eff", "ex"]).copy()
    d["flat"] = d["eff"] < d.groupby("coin")["eff"].transform("median")
    res = {}
    for k, s in d.groupby("flat"):
        sl = stats.linregress(s["pos"], s["ex"]); res[f"flat={k}"] = [sl.slope, sl.slope / sl.stderr, len(s)]
    out["pos slope by flat"] = pd.DataFrame(res, index=["slope", "t", "n"]).T.round(4)
    # momentum slope by vol tercile
    d = g.dropna(subset=["fc", "vol20", "ex"]).copy()
    d["vb"] = d.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    res = {}
    for k, s in d.groupby("vb"):
        sl = stats.linregress(s["fc"], s["ex"]); res[k] = [sl.slope, sl.slope / sl.stderr, len(s)]
    out["fc slope by vol tercile"] = pd.DataFrame(res, index=["slope", "t", "n"]).T.round(5)
    res = {}
    for k, s in g.dropna(subset=["fc", "ex"]).groupby("coin"):
        sl = stats.linregress(s["fc"], s["ex"]); res[k] = [sl.slope, sl.slope / sl.stderr, len(s)]
    out["fc slope by coin"] = pd.DataFrame(res, index=["slope", "t", "n"]).T.round(5)
    res = {}
    for k, s in g.dropna(subset=["fc", "ex"]).groupby("yr"):
        if len(s) > 30:
            sl = stats.linregress(s["fc"], s["ex"]); res[k] = [sl.slope, sl.slope / sl.stderr, len(s)]
    out["fc slope by year"] = pd.DataFrame(res, index=["slope", "t", "n"]).T.round(5)
    # daily book
    dd = []
    for coin, ws in days.items():
        for w, df in ws.items():
            x = df[["day", "book_return", "coin_return"]].copy(); x["coin"] = coin; x["w"] = w
            x["wd"] = pd.to_datetime(x["day"]).dt.dayofweek
            x["prev_coin"] = x["coin_return"].shift(1)
            dd.append(x)
    dd = pd.concat(dd).dropna(subset=["book_return", "coin_return"])
    a = dd.groupby("wd")[["book_return", "coin_return"]].agg(["mean", "count"])
    out["weekday daily returns"] = a.round(5)
    # next day return after large daily move (z of previous day)
    dd["absz"] = dd.groupby("coin")["prev_coin"].transform(lambda s: s / s.std())
    dd["zb"] = pd.cut(dd["absz"], [-99, -2, -1, 0, 1, 2, 99])
    a = dd.groupby("zb")["coin_return"].agg(["mean", "count", "std"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["next-day coin return by prev-day z"] = a.round(5)
    # book by window
    bw = dd.groupby("w")[["book_return", "coin_return"]].mean()
    out["book mean by window (top/bottom)"] = pd.concat([bw.sort_values("book_return").head(5), bw.sort_values("book_return").tail(5)]).round(5)
    return out
