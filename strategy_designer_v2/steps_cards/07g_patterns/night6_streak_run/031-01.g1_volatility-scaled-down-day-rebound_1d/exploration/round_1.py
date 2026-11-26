def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 3
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol60 = r.rolling(60, min_periods=20).std()
            # streak: signed count of consecutive same-sign closes
            s = np.sign(r.fillna(0)).values
            st = np.zeros(len(s))
            for i in range(len(s)):
                if s[i] == 0:
                    st[i] = 0
                elif i > 0 and np.sign(st[i-1]) == s[i]:
                    st[i] = st[i-1] + s[i]
                else:
                    st[i] = s[i]
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "r1z": r / vol60, "r3": c / c.shift(3) - 1, "r7": c / c.shift(7) - 1,
                "r30": c / c.shift(30) - 1,
                "streak": st, "vol": vol60, "fwd": fwd, "fwd1": fwd1,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "range": (b["high"] - b["low"]) / c,
                "clo": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
            })
            d["r3z"] = d["r3"] / (vol60 * np.sqrt(3))
            d["r7z"] = d["r7"] / (vol60 * np.sqrt(7))
            d["r30z"] = d["r30"] / (vol60 * np.sqrt(30))
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % H == 0) & A["fwd"].notna()].copy()
    stat = G.groupby("coin")["fwd"].agg(["mean", "std"])
    G["y"] = (G["fwd"] - G["coin"].map(stat["mean"])) / G["coin"].map(stat["std"])
    G["vrank"] = G.groupby("coin")["vol"].rank(pct=True)
    G["rrank"] = G.groupby("coin")["range"].rank(pct=True)

    def tab(col, q=5, cut=None):
        g = G.dropna(subset=[col, "y"]).copy()
        if cut is None:
            g["b"] = pd.qcut(g[col].rank(method="first"), q, labels=False)
        else:
            g["b"] = g[col].clip(-cut, cut)
        out = []
        for k, x in g.groupby("b"):
            dd = x.groupby("day")["y"].sum()
            n = len(x)
            m = x["y"].mean()
            se = dd.std(ddof=1) * np.sqrt(len(dd)) / n
            out.append({"bin": k, "lo": x[col].min(), "hi": x[col].max(), "n": n,
                        "mean_y": m, "t": m / se, "raw_fwd%": 100 * x["fwd"].mean()})
        return pd.DataFrame(out)

    def slope(col):
        g = G.dropna(subset=[col, "y"])
        x = (g[col] - g[col].mean()) / g[col].std()
        b = (x * g["y"]).sum() / (x ** 2).sum()
        e = g["y"] - g["y"].mean() - b * x
        dd = (x * e).groupby(g["day"]).sum()
        se = np.sqrt((dd ** 2).sum()) / (x ** 2).sum()
        return b / se

    res = {}
    res["streak"] = tab("streak", cut=5)
    res["r1z"] = tab("r1z", 10)
    res["r7z"] = tab("r7z", 5)
    res["r30z"] = tab("r30z", 5)
    res["vol_rank"] = tab("vrank", 5)
    res["range_rank"] = tab("rrank", 5)
    res["close_loc"] = tab("clo", 5)
    res["weekday"] = tab("wd", cut=6)
    res["slopes_t"] = pd.Series({c: slope(c) for c in ["streak", "r1z", "r3z", "r7z", "r30z", "vrank", "rrank", "clo"]})
    # per coin r7z and r30z slope sign
    pc = {}
    for coin, x in G.groupby("coin"):
        for c in ["r1z", "r7z", "r30z", "streak"]:
            xx = x.dropna(subset=[c])
            pc[(coin, c)] = stats.spearmanr(xx[c], xx["y"]).correlation
    res["per_coin_spearman"] = pd.Series(pc).unstack()
    # book: days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, win=w))
    D = pd.concat(D)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    res["book_by_year"] = D.groupby("yr")[["book_return", "coin_return"]].mean() * 100
    res["book_by_coin"] = D.groupby("coin")[["book_return", "coin_return"]].agg(["mean", "std"]) * 100
    return res
