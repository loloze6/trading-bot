def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 72
    rows = []
    hourrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol20 = r.rolling(20).std()
            vol120 = r.rolling(120).std()
            rng42 = (b["high"].rolling(42).max() - b["low"].rolling(42).min()) / c
            rng_rel = rng42 / (r.rolling(180).std() * np.sqrt(42))
            ret42 = c / c.shift(42) - 1
            ret6 = c / c.shift(6) - 1
            ret1 = r
            fwd = c.shift(-H) / c - 1
            fwd6 = c.shift(-6) / c - 1
            fwd18 = c.shift(-18) / c - 1
            idx = np.arange(0, len(b), H)
            g = pd.DataFrame({
                "coin": coin, "w": w,
                "fc": b["forecast"].values[idx],
                "fwd": fwd.values[idx],
                "volratio": (vol20 / vol120).values[idx],
                "rngrel": rng_rel.values[idx],
                "ret42s": (ret42 / (vol20 * np.sqrt(42))).values[idx],
                "ret6s": (ret6 / (vol20 * np.sqrt(6))).values[idx],
                "absfwd": np.abs(fwd.values[idx]),
            })
            rows.append(g)
            # 6-bar grid for short-horizon patterns
            idx6 = np.arange(0, len(b), 6)
            ts = pd.to_datetime(b["timestamp"])
            hourrows.append(pd.DataFrame({
                "coin": coin, "w": w,
                "ret6s": (ret6 / (vol20 * np.sqrt(6))).values[idx6],
                "ret1s": (ret1 / vol20).values[idx6],
                "fwd6": fwd6.values[idx6],
                "fwd6s": (fwd6 / (vol20 * np.sqrt(6))).values[idx6],
                "volratio": (vol20 / vol120).values[idx6],
                "wd": ts.dt.weekday.values[idx6],
            }))
    G = pd.concat(rows, ignore_index=True)
    drift = G.groupby("coin")["fwd"].transform("mean")
    G["ex"] = G["fwd"] - drift
    G = G.dropna(subset=["ex", "fc"])
    G["dirx"] = np.sign(G["fc"]) * G["ex"]

    def tab(df, col, q=5):
        d = df.dropna(subset=[col]).copy()
        d["q"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        o = d.groupby("q").agg(n=("ex", "size"), lo=(col, "min"), hi=(col, "max"),
                               ex_mean=("ex", "mean"), absfwd=("absfwd", "mean"),
                               dirx=("dirx", "mean"))
        o["t_ex"] = d.groupby("q")["ex"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))))
        o["t_dirx"] = d.groupby("q")["dirx"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))))
        return o.round(4)

    out = {}
    out["fc_quintiles"] = tab(G, "fc")
    out["rangecompression_quintiles"] = tab(G, "rngrel")
    out["volratio_quintiles"] = tab(G, "volratio")
    # direction capture by side
    side = G.assign(side=np.where(G.fc > 0, "long", "short")).groupby("side")["dirx"].agg(["size", "mean", "std"])
    side["t"] = side["mean"] / (side["std"] / np.sqrt(side["size"]))
    out["by_side"] = side.round(4)
    # slope of ex on fc by volratio tercile
    d = G.dropna(subset=["volratio"]).copy()
    d["vq"] = pd.qcut(d["volratio"], 3, labels=False)
    sl = []
    for q, x in d.groupby("vq"):
        s = stats.linregress(x["fc"], x["ex"])
        sl.append({"vq": q, "n": len(x), "slope": s.slope, "t": s.slope / s.stderr})
    out["slope_by_volratio_tercile"] = pd.DataFrame(sl).round(5)
    # per window-year? per coin slope
    pc = []
    for coin, x in G.groupby("coin"):
        s = stats.linregress(x["fc"], x["ex"])
        pc.append({"coin": coin, "n": len(x), "slope": s.slope, "t": s.slope / s.stderr, "dirx": x["dirx"].mean()})
    out["per_coin"] = pd.DataFrame(pc).round(5)
    # short horizon: 1-day after large 1-day moves
    Hd = pd.concat(hourrows, ignore_index=True).dropna()
    Hd["q"] = pd.qcut(Hd["ret6s"], 5, labels=False)
    o = Hd.groupby("q").agg(n=("fwd6", "size"), fwd6=("fwd6", "mean"), fwd6s=("fwd6s", "mean"))
    o["t"] = Hd.groupby("q")["fwd6s"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))))
    out["next1d_after_1d_move"] = o.round(5)
    o = Hd.groupby("wd").agg(n=("fwd6", "size"), fwd6=("fwd6", "mean"), fwd6s=("fwd6s", "mean"))
    o["t"] = Hd.groupby("wd")["fwd6s"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))))
    out["next1d_by_weekday"] = o.round(5)
    # book: daily returns, holding, by window-ish aggregate per coin
    bk = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            bk.append(pd.DataFrame({"coin": coin, "w": w, "br": dd["book_return"], "cr": dd["coin_return"]}))
    B = pd.concat(bk).dropna()
    out["book_by_coin"] = B.groupby("coin").agg(book=("br", "mean"), hold=("cr", "mean"),
                                                  bsd=("br", "std"), hsd=("cr", "std")).round(5)
    return out
