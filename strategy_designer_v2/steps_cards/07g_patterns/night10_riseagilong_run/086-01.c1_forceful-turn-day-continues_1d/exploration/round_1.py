def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        r3all = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            for i in range(0, n - 3, 3):
                r3all.append(c[i+3]/c[i]-1)
        drift[coin] = (np.mean(r3all), np.std(r3all))
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r1 = c.pct_change()
            vol = r1.rolling(30, min_periods=20).std()
            b["z1"] = r1/vol
            b["r5z"] = (c/c.shift(5)-1)/(vol*np.sqrt(5))
            b["r20z"] = (c/c.shift(20)-1)/(vol*np.sqrt(20))
            b["dd20"] = (c/c.rolling(20, min_periods=10).max()-1)/vol
            rng = (b["high"]-b["low"])
            b["clv"] = (b["close"]-b["low"])/rng.replace(0, np.nan)
            b["rngz"] = (rng/b["close"].shift(1))/vol
            b["volz"] = b["volume"]/b["volume"].rolling(30, min_periods=20).mean()
            b["vol_ratio"] = r1.rolling(7).std()/vol
            # down run before
            down = (r1 < 0).astype(int)
            run = np.zeros(len(b)); s = 0
            for i in range(len(b)):
                s = s+1 if down.iloc[i] == 1 else 0
                run[i] = s
            b["downrun"] = run
            b["prevrun"] = pd.Series(run).shift(1).values
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["inprof"] = b["regime"].isin(["trending", "unknown"])
            b["fwd3"] = c.shift(-3)/c-1
            b["fwd1"] = c.shift(-1)/c-1
            b["pos"] = np.arange(len(b))
            b["coin"] = coin; b["win"] = w
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            g = b[(b["pos"] % 3 == 0) & b["fwd3"].notna()]
            rows.append(g)
    df = pd.concat(rows)
    df["unu"] = df.apply(lambda r: r["fwd3"]-drift[r["coin"]][0], axis=1)
    df["unu_s"] = df.apply(lambda r: r["unu"]/drift[r["coin"]][1], axis=1)
    out = {}
    out["profile share of grid bars"] = df["inprof"].mean()
    P = df[df["inprof"]]
    out["in-profile unusual mean/t/n"] = pd.Series({"mean": P["unu"].mean(), "t": stats.ttest_1samp(P["unu"], 0).statistic, "n": len(P)})
    out["out-profile unusual mean/t/n"] = pd.Series({"mean": df[~df["inprof"]]["unu"].mean(), "t": stats.ttest_1samp(df[~df["inprof"]]["unu"], 0).statistic, "n": (~df["inprof"]).sum()})
    def bucket(col, q=5):
        x = P.dropna(subset=[col])
        x = x.assign(b=pd.qcut(x[col].rank(method="first"), q, labels=False))
        g = x.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), mean=("unu", "mean"), strength=("unu_s", "mean"), n=("unu", "size"))
        g["t"] = x.groupby("b")["unu"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s))))
        sl = stats.linregress(x[col], x["unu"])
        g.loc["slope_t"] = [np.nan, np.nan, sl.slope, np.nan, len(x), sl.slope/sl.stderr]
        return g
    for col in ["z1", "r5z", "r20z", "dd20", "clv", "rngz", "volz", "vol_ratio", "downrun"]:
        out["prof by " + col] = bucket(col)
    out["prof by weekday"] = P.groupby("wd")["unu"].agg(["mean", "count"]).assign(t=P.groupby("wd")["unu"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s)))))
    out["prof by year"] = P.groupby(pd.to_datetime(P["timestamp"]).dt.year)["unu"].agg(["mean", "count"])
    out["prof by coin"] = P.groupby("coin")["unu"].agg(["mean", "count"])
    # book days: largest gains/losses
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin))
    D = pd.concat(dd)
    D = D[D["book_return"] != 0].dropna(subset=["book_return"])
    out["book nonzero days: n, mean, share pos"] = pd.Series({"n": len(D), "mean": D["book_return"].mean(), "pos": (D["book_return"] > 0).mean(), "corr coin": D[["book_return", "coin_return"]].corr().iloc[0, 1]})
    return out
