def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.copy().reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            mabs = r.abs().shift(1).rolling(60, min_periods=20).mean()
            z = r / mabs
            vol20 = r.rolling(20).std()
            vrank = vol20.rolling(100, min_periods=30).apply(lambda x: (x[-1] >= x).mean(), raw=True)
            volz = np.log(b["volume"] / b["volume"].shift(1).rolling(30, min_periods=10).mean())
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "z": z, "vrank": vrank,
                              "volz": volz, "r20": c / c.shift(20) - 1,
                              "f3": c.shift(-3) / c - 1, "f7": c.shift(-7) / c - 1})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    def reg(df, y, x):
        df = df.dropna(subset=[y, x])
        if len(df) < 20: return pd.Series({"slope": np.nan, "t": np.nan, "n": len(df)})
        s = stats.linregress(df[x], df[y])
        return pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(df)})
    res = {}
    for H, col in [(3, "f3"), (7, "f7")]:
        g = D[D.pos % H == 0].dropna(subset=[col, "z", "vrank"]).copy()
        g["ex"] = g[col] - g.groupby("coin")[col].transform("mean")
        g["zc"] = g.z.clip(-6, 6)
        for hv, sub in [("hi", g[g.vrank >= 0.5]), ("lo", g[g.vrank < 0.5]), ("all", g)]:
            res[(H, hv, "all")] = reg(sub, "ex", "zc")
            for coin in sub.coin.unique():
                res[(H, hv, coin)] = reg(sub[sub.coin == coin], "ex", "zc")
            for ww in ["first", "second"]:
                wn = sub.w.str[1:].astype(int)
                part = sub[wn <= 12] if ww == "first" else sub[wn > 12]
                res[(H, hv, ww)] = reg(part, "ex", "zc")
        # volume interaction in hiVol
        hi = g[g.vrank >= 0.5].dropna(subset=["volz"]).copy()
        hi["zv"] = hi.zc * hi.volz
        res[(H, "hi", "z*volz")] = reg(hi, "ex", "zv")
        hi["vq"] = hi.volz > hi.volz.median()
        res[(H, "hi", "z|hiVolume")] = reg(hi[hi.vq], "ex", "zc")
        res[(H, "hi", "z|loVolume")] = reg(hi[~hi.vq], "ex", "zc")
        lo = g[g.vrank < 0.5].dropna(subset=["volz"]).copy()
        lo["vq"] = lo.volz > lo.volz.median()
        res[(H, "lo", "z|hiVolume")] = reg(lo[lo.vq], "ex", "zc")
        res[(H, "lo", "z|loVolume")] = reg(lo[~lo.vq], "ex", "zc")
        # vrank as continuous moderator
        g["zr"] = g.zc * (g.vrank - 0.5)
        res[(H, "all", "z*(vrank-.5)")] = reg(g, "ex", "zr")
    out["slopes of excess return on z"] = pd.DataFrame(res).T
    return out
