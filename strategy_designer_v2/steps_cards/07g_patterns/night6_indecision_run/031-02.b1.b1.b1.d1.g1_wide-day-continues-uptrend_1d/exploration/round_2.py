def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            v = b["volume"].astype(float)
            rng = h - l
            mult = rng / rng.rolling(20).mean()
            vmult = v / v.rolling(20).mean()
            ret20 = c / c.shift(20) - 1
            ret1 = c / c.shift(1) - 1
            hi20 = c / c.rolling(20).max() - 1
            vol20 = ret1.rolling(20).std()
            n = len(b)
            for H in (1, 3, 5):
                idx = np.arange(0, n - H, H)
                fwd = c.shift(-H) / c - 1
                rows.append(pd.DataFrame({"coin": coin, "win": w, "H": H, "ts": b["timestamp"].values[idx],
                    "fwd": fwd.values[idx], "mult": mult.values[idx], "vmult": vmult.values[idx],
                    "ret20": ret20.values[idx], "ret1": ret1.values[idx], "hi20": hi20.values[idx],
                    "r20z": (ret20 / (vol20 * np.sqrt(20))).values[idx]}))
    D = pd.concat(rows, ignore_index=True)
    D["day"] = pd.to_datetime(D["ts"]).dt.floor("D")
    D["year"] = pd.to_datetime(D["ts"]).dt.year
    D["drift"] = D.groupby(["coin", "H"])["fwd"].transform("mean")
    D["un"] = D["fwd"] - D["drift"]

    def ct(s):
        s = s.dropna()
        if len(s) < 10: return pd.Series({"n": len(s), "mean": np.nan, "t": np.nan, "days": 0})
        dd = D.loc[s.index, "day"]; m = s.mean()
        ds = (s - m).groupby(dd).sum()
        se = np.sqrt((ds ** 2).sum()) / len(s)
        return pd.Series({"n": len(s), "mean": m, "t": m / se if se > 0 else np.nan, "days": dd.nunique()})

    out = {}
    D3 = D[D.H == 3].dropna(subset=["mult", "ret20"])
    up = D3[D3.ret20 > 0]
    out["up: vol mult bins"] = up.groupby(pd.cut(up.vmult, [0, 0.7, 1.0, 1.5, 2.5, 99]), observed=True)["un"].apply(ct).unstack()
    out["up: dist from 20d high bins"] = up.groupby(pd.cut(up.hi20, [-1, -0.15, -0.07, -0.02, -1e-9, 0.01]), observed=True)["un"].apply(ct).unstack()
    out["up: ret1 bins"] = up.groupby(pd.cut(up.ret1, [-1, -0.05, -0.01, 0.01, 0.05, 0.10, 5]), observed=True)["un"].apply(ct).unstack()
    out["all: ret1 bins"] = D3.groupby(pd.cut(D3.ret1, [-1, -0.10, -0.05, -0.01, 0.01, 0.05, 0.10, 5]), observed=True)["un"].apply(ct).unstack()
    out["all: trend-z bins"] = D3.groupby(pd.cut(D3.r20z, [-99, -2, -1, 0, 1, 2, 99]), observed=True)["un"].apply(ct).unstack()
    wu = up[up.mult >= 1.5]
    out["wide up by year"] = wu.groupby("year")["un"].apply(ct).unstack()
    out["wide up by ret1 sign"] = wu.groupby(np.sign(wu.ret1))["un"].apply(ct).unstack()
    for H in (1, 5):
        DH = D[(D.H == H)].dropna(subset=["mult", "ret20"])
        DH = DH[(DH.ret20 > 0)]
        out[f"up H{H} rangemult bins"] = DH.groupby(pd.cut(DH.mult, [0, 1.0, 1.5, 2.0, 99]), observed=True)["un"].apply(ct).unstack()
    # book: by year and around biggest days
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bk.append(d.assign(coin=coin, win=w))
    B = pd.concat(bk)
    bd = B.groupby("day").agg(book=("book_return", "mean"), coin=("coin_return", "mean")).dropna()
    bd.index = pd.to_datetime(bd.index)
    out["book by year"] = bd.groupby(bd.index.year).agg(n=("book", "count"), book_mean=("book", "mean"), coin_mean=("coin", "mean"))
    q = bd["book"].quantile([0.01, 0.99])
    out["coin ret on book extreme days"] = pd.DataFrame({"big gains": bd[bd.book >= q[0.99]].mean(), "big losses": bd[bd.book <= q[0.01]].mean()})
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tr.append(t)
    T = pd.concat(tr)
    T["fb"] = pd.cut(T["entry_forecast"].astype(float), [0, 7.5, 10, 13, 16, 21])
    out["trades by entry forecast"] = T.groupby("fb", observed=True)["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
