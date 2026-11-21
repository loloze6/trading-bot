def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    H = [48, 96, 168]
    gridmean = {}
    for coin, wins in data["bars"].items():
        # coin's usual move / drift per horizon from non-overlapping grid
        g = {h: [] for h in H}
        for w, b in wins.items():
            c = b["close"].values
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                g[h].extend(list(c[idx + h] / c[idx] - 1))
        gridmean[coin] = {h: (np.mean(g[h]), np.std(g[h])) for h in H}
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            v = b["volume"].astype(float)
            lr = np.log(c).diff()
            r24 = c / c.shift(24) - 1
            absum = lr.abs().rolling(24).sum()
            eff = (np.log(c / c.shift(24))).abs() / absum
            jump = lr.abs().rolling(24).max() / absum
            vcon = v.rolling(24).max() / v.rolling(24).sum()
            r7d = c / c.shift(168) - 1
            vol24 = lr.rolling(24).std()
            vol30 = lr.rolling(720, min_periods=200).std()
            act = b.index[b["regime"] == "mean_reversion"]
            for k, i in enumerate(act):
                d = {"coin": coin, "w": w, "k": k, "fc": b.loc[i, "forecast"],
                     "r24": r24[i], "eff": eff[i], "jump": jump[i], "vcon": vcon[i],
                     "r7d": r7d[i], "volr": vol24[i] / vol30[i] if vol30[i] else np.nan,
                     "year": pd.Timestamp(b.loc[i, "timestamp"]).year}
                for h in H:
                    if i + h < len(c):
                        m, s = gridmean[coin][h]
                        d[f"x{h}"] = (c[i + h] / c[i] - 1) - m
                        d[f"t{h}"] = c[i + h] / c[i] - 1
                        d[f"s{h}"] = ((c[i + h] / c[i] - 1) - m) / s
                rows.append(d)
    df = pd.DataFrame(rows)
    # non-overlap for 48h: every other case per window
    df["nov48"] = (df["k"] % 2 == 0)
    df["nov168"] = (df["k"] % 7 == 0)
    falls = df[(df["fc"] > 0)].copy()
    f48 = falls[falls["nov48"]].dropna(subset=["x48"])

    def summ(gdf, col):
        x = gdf[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    f48["fc_t"] = pd.qcut(f48["fc"], 3, labels=["low", "mid", "high"])
    out["48h excess by forecast tercile"] = f48.groupby("fc_t").apply(lambda g: summ(g, "x48"))
    for col in ["eff", "jump", "vcon", "volr", "r7d"]:
        f48[col + "_t"] = pd.qcut(f48[col], 3, labels=["low", "mid", "high"])
        out[f"48h excess by {col} tercile"] = f48.groupby(col + "_t").apply(lambda g: summ(g, "x48"))
    out["48h excess by coin"] = f48.groupby("coin").apply(lambda g: summ(g, "x48"))
    out["48h excess by year"] = f48.groupby("year").apply(lambda g: summ(g, "x48"))
    # interaction: forecast high x jump
    f48["deep"] = f48["fc"] >= f48["fc"].median()
    out["48h excess deep x jump"] = f48.groupby(["deep", "jump_t"]).apply(lambda g: summ(g, "x48"))
    out["48h excess deep x r7d"] = f48.groupby(["deep", "r7d_t"]).apply(lambda g: summ(g, "x48"))
    # longer horizon
    f168 = falls[falls["nov168"]]
    out["168h excess, falls"] = summ(f168, "x168")
    f96 = falls[falls["k"] % 4 == 0]
    out["96h excess, falls"] = summ(f96, "x96")
    # rises (fc==0) for comparison
    rises = df[(df["fc"] == 0) & df["nov48"]]
    out["48h excess, non-fall evenings"] = summ(rises, "x48")
    # regression on combos
    z = f48.dropna(subset=["x48", "fc", "jump", "r7d", "eff"])
    for col in ["fc", "jump", "eff", "r7d"]:
        sl = stats.linregress(z[col], z["s48"])
        out[f"slope strength48 on {col}"] = f"slope {sl.slope:.4g} t {sl.slope/sl.stderr:.2f} n {len(z)}"
    # book: daily pooled
    drows = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d[["book_return", "coin_return"]].copy()
            dd["coin"] = coin; dd["w"] = w; dd["year"] = pd.to_datetime(d["day"]).dt.year
            dd["di"] = np.arange(len(dd))
            drows.append(dd)
    D = pd.concat(drows)
    B = D.groupby(["w", "di"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean"), year=("year", "first")).reset_index()
    B["wn"] = B["w"].str[1:].astype(int)
    B = B.sort_values(["wn", "di"]).dropna()
    eq = (1 + B["book"]).cumprod()
    dd = eq / eq.cummax() - 1
    out["book deepest fall"] = float(dd.min())
    B["dd"] = dd.values
    trough = B.iloc[int(np.argmin(dd.values))]
    out["deepest fall trough window"] = trough["w"]
    out["book & coin by year"] = B.groupby("year").agg(book=("book", "mean"), coin=("coin", "mean"), n=("book", "size"))
    out["book & coin by window"] = B.groupby("wn").agg(book=("book", "mean"), coin=("coin", "mean"), mindd=("dd", "min"))
    return out
