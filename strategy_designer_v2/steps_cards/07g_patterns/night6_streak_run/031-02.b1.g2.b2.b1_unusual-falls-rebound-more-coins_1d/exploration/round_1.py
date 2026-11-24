def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20, min_periods=10).std()
            z = r / vol.shift(1)
            # streak: signed count of consecutive same-direction closes
            s = np.sign(r).fillna(0).values
            st = np.zeros(len(s))
            for i in range(len(s)):
                if s[i] == 0: st[i] = 0
                elif i > 0 and np.sign(st[i-1]) == s[i]: st[i] = st[i-1] + s[i]
                else: st[i] = s[i]
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            volq = vol / vol.rolling(60, min_periods=20).mean()
            for h in (1, 2, 5):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(b), h)
                d = pd.DataFrame({
                    "coin": coin, "w": w, "h": h,
                    "day": pd.to_datetime(b["timestamp"]).dt.floor("D").values[idx],
                    "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values[idx],
                    "yr": pd.to_datetime(b["timestamp"]).dt.year.values[idx],
                    "z": z.values[idx], "st": st[idx], "r5": r5.values[idx] / (vol.values[idx] * np.sqrt(5)),
                    "r20": r20.values[idx] / (vol.values[idx] * np.sqrt(20)),
                    "volq": volq.values[idx], "fwd": fwd.values[idx],
                    "fc": b["forecast"].values[idx]})
                rows.append(d)
    D = pd.concat(rows).dropna(subset=["fwd"])
    D["ex"] = D["fwd"] - D.groupby(["coin", "h"])["fwd"].transform("mean")
    usual = D.groupby(["coin", "h"])["fwd"].transform("std")
    D["exs"] = D["ex"] / usual

    def tab(g, col="exs"):
        out = []
        for k, x in g:
            x = x.dropna(subset=[col])
            ds = x.groupby("day")[col].sum()
            n = len(x); nd = len(ds)
            m = x[col].mean()
            se = np.sqrt((ds - ds.mean() * 0 - m * x.groupby("day").size()).pow(2).sum()) / n if n > 1 else np.nan
            out.append((k, n, nd, round(x["ex"].mean() * 100, 3), round(m, 4), round(m / se if se else np.nan, 2)))
        return pd.DataFrame(out, columns=["group", "n", "days", "ex_%", "strength", "t_day"])

    res = {}
    for h in (2, 5):
        X = D[D.h == h].dropna(subset=["z"])
        X = X.assign(zb=pd.cut(X["z"], [-99, -2.5, -1.5, -0.75, 0, 0.75, 1.5, 2.5, 99]))
        res[f"z bins h{h}"] = tab(X.groupby("zb", observed=True))
        Y = D[D.h == h].assign(stb=D[D.h == h]["st"].clip(-5, 5))
        res[f"streak h{h}"] = tab(Y.groupby("stb"))
        Z = D[D.h == h].dropna(subset=["r20"])
        Z = Z.assign(b=pd.qcut(Z["r20"], 5, labels=False))
        res[f"20d scaled ret quintile h{h}"] = tab(Z.groupby("b"))
        V = D[D.h == h].dropna(subset=["volq"])
        V = V.assign(b=pd.qcut(V["volq"], 4, labels=False))
        res[f"vol ratio quartile h{h}"] = tab(V.groupby("b"))
    X = D[D.h == 1]
    res["weekday h1"] = tab(X.groupby("wd"))
    X2 = D[(D.h == 2)].dropna(subset=["z"])
    X2 = X2[X2.z < 0]
    X2 = X2.assign(vb=pd.qcut(X2["volq"], 3, labels=False), zb=pd.cut(X2["z"], [-99, -1.5, 0]))
    res["falls by vol tercile x size h2"] = tab(X2.groupby(["vb", "zb"], observed=True))
    # book daily returns: by year and largest days
    bk = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            bk.append(d.assign(coin=coin, w=w))
    B = pd.concat(bk)
    B["day"] = pd.to_datetime(B["day"])
    bd = B.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    bd["yr"] = bd.index.year
    res["book by year"] = bd.groupby("yr").agg(n=("book_return", "size"), book=("book_return", "mean"), hold=("coin_return", "mean"))
    return res
