def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = {"1d":6, "3d":18, "7d":42, "14d":84}
    rows = []
    hourrows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float); hi = df["high"].astype(float); lo = df["low"].astype(float)
            r6 = c / c.shift(6) - 1
            mabs = r6.abs().rolling(180, min_periods=90).mean()
            z6 = r6 / mabs
            rng = (hi - lo) / c
            rr = rng.rolling(6).mean() / rng.rolling(180, min_periods=90).mean()
            r180 = c / c.shift(180) - 1
            vol = (c.pct_change()).rolling(180, min_periods=90).std()
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for hn, h in H.items():
                idx = np.arange(0, n - h, h)
                f = (c.shift(-h) / c - 1).values
                for i in idx:
                    rows.append((coin, w, hn, z6.iat[i], rr.iat[i], r180.iat[i], vol.iat[i], f[i]))
            nr = (c.shift(-1) / c - 1).values
            for i in range(n - 1):
                hourrows.append((coin, ts.iat[i].hour, ts.iat[i].dayofweek, nr[i]))
    D = pd.DataFrame(rows, columns=["coin","w","h","z6","rr","r180","vol","f"])
    D["ex"] = D["f"] - D.groupby(["coin","h"])["f"].transform("mean")
    D = D.dropna()
    out = {}
    def tab(col, q=5):
        res = []
        for hn in H:
            s = D[D.h == hn].copy()
            s["q"] = s.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
            g = s.groupby("q")["ex"].agg(["mean","std","count"])
            g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
            g["h"] = hn
            res.append(g.reset_index()[["h","q","mean","t","count"]])
        return pd.concat(res).round(4)
    out["by z6 quintile (0=largest fall)"] = tab("z6")
    out["by range ratio quintile"] = tab("rr")
    out["by 30d return quintile"] = tab("r180")
    out["by vol quintile"] = tab("vol")
    # interaction: falls with high range vs rises with high range at 14d and 3d
    res = []
    for hn in ["3d","14d"]:
        s = D[D.h == hn]
        for zs, zm in [("fall", s.z6 < -1), ("rise", s.z6 > 1), ("mid", s.z6.abs() <= 1)]:
            for rs, rm in [("wide", s.rr > 1.3), ("norm", s.rr <= 1.3)]:
                x = s[zm & rm]["ex"]
                res.append((hn, zs, rs, x.mean(), x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, len(x)))
    out["z6 x range"] = pd.DataFrame(res, columns=["h","z6","rr","mean","t","n"]).round(4)
    Hr = pd.DataFrame(hourrows, columns=["coin","hour","wd","r"]).dropna()
    Hr["ex"] = Hr["r"] - Hr.groupby("coin")["r"].transform("mean")
    g = Hr.groupby("hour")["ex"].agg(["mean","std","count"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["next bar by hour"] = g[["mean","t","count"]].round(5)
    g = Hr.groupby("wd")["ex"].agg(["mean","std","count"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["next bar by weekday"] = g[["mean","t","count"]].round(5)
    # book by coin
    br = []
    for coin, wins in data["days"].items():
        b = pd.concat([d[["book_return","coin_return"]] for d in wins.values()]).dropna()
        br.append((coin, b.book_return.mean(), b.book_return.mean()/b.book_return.std()*np.sqrt(365), b.coin_return.mean()/b.coin_return.std()*np.sqrt(365), (b.book_return!=0).mean()))
    out["book by coin"] = pd.DataFrame(br, columns=["coin","mean","sharpe","hold_sharpe","share_active"]).round(4)
    return out
