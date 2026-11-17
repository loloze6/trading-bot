def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 14
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            d = c.diff()
            up = d.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
            dn = (-d).clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
            rsi = 100 - 100/(1+up/dn)
            above = (rsi > 50).astype(int)
            # streak signed
            streak = np.zeros(len(b))
            for i in range(len(b)):
                s = 1 if above[i] else -1
                if i > 0 and np.sign(streak[i-1]) == s:
                    streak[i] = streak[i-1] + s
                else:
                    streak[i] = s
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            vol_ratio = vol20 / r1.rolling(60, min_periods=40).std()
            ret7 = c / c.shift(7) - 1
            ret14 = c / c.shift(14) - 1
            ret28 = c / c.shift(28) - 1
            hi = c.rolling(28).max(); lo = c.rolling(28).min()
            pos28 = (c - lo) / (hi - lo)
            fwd = c.shift(-H) / c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(b)), "rsi": rsi.values,
                               "streak": streak, "fc": b["forecast"].values, "alloc": b["postRebalance_current_allocation"].values,
                               "vol20": vol20.values, "volr": vol_ratio.values, "ret7": ret7.values, "ret14": ret14.values,
                               "ret28": ret28.values, "pos28": pos28.values, "fwd": fwd.values,
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values, "year": pd.to_datetime(b["timestamp"]).dt.year.values,
                               "r1": r1.values})
            rows.append(df)
    A = pd.concat(rows)
    A = A[A["i"] >= 20]  # rsi warm-up inside window
    G = A[(A["i"] % H == 0)].dropna(subset=["fwd"]).copy()
    G["ex"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    out["n_grid"] = len(G)
    def slope(x):
        g = G.dropna(subset=[x, "ex"])
        r = stats.linregress(g[x], g["ex"])
        return (round(r.slope, 5), round(r.slope / r.stderr, 2), len(g))
    out["slopes (slope,t,n)"] = pd.DataFrame({x: slope(x) for x in ["rsi","streak","ret7","ret14","ret28","pos28","vol20","volr","fc"]}, index=["slope","t","n"]).T
    out["by coin slopes ret28,rsi"] = pd.DataFrame({c: [stats.linregress(g["ret28"].values, g["ex"].values).rvalue for g in [G[(G.coin==c)].dropna(subset=["ret28"])]] + [stats.linregress(G[G.coin==c].dropna(subset=["rsi"])["rsi"], G[G.coin==c].dropna(subset=["rsi"])["ex"]).rvalue] for c in G.coin.unique()}, index=["corr_ret28","corr_rsi"]).T
    G["sb"] = pd.cut(G["streak"], [-200,-20,-10,-1,0,10,20,200])
    out["streak buckets"] = G.groupby("sb")["ex"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    G["rq"] = pd.qcut(G["rsi"], 5)
    out["rsi quintiles"] = G.groupby("rq")["ex"].agg(["mean","count"])
    G["vq"] = pd.qcut(G["vol20"], 3)
    out["vol terciles"] = G.groupby("vq")["ex"].agg(["mean","count"])
    G["r28q"] = pd.qcut(G["ret28"], 5)
    out["ret28 quintiles"] = G.groupby("r28q")["ex"].agg(["mean","count"])
    # daily: weekday effect on 1-day returns (non-overlapping by nature)
    D = A.dropna(subset=["r1"])
    out["weekday r1"] = D.groupby("wd")["r1"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    # after large daily moves
    D = D.copy(); D["nxt"] = D.groupby(["coin","w"])["r1"].shift(-1)
    D["z"] = D["r1"]/D["vol20"]
    D["zb"] = pd.cut(D["z"], [-99,-2,-1,0,1,2,99])
    out["next day after z move"] = D.groupby("zb")["nxt"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    out["year mean fwd"] = G.groupby("year")["fwd"].agg(["mean","count"])
    # book
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bd.append(d.assign(coin=coin, w=w))
    B = pd.concat(bd).dropna(subset=["book_return"])
    out["book vs coin"] = pd.DataFrame({"mean_book": B.groupby("coin")["book_return"].mean(), "mean_coin": B.groupby("coin")["coin_return"].mean(), "n": B.groupby("coin").size()})
    out["share in market"] = (A["alloc"].abs() > 0.01).mean()
    return out
