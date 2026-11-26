def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    def build(h):
        rows = []
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].astype(float); v = b["volume"].astype(float)
                r1 = c.pct_change()
                sd = r1.rolling(20).std().shift(1)
                z = r1 / sd
                z3 = (c / c.shift(3) - 1) / (sd * np.sqrt(3))
                r5p = c / c.shift(5) - 1
                z5 = r5p / (sd * np.sqrt(5))
                r20 = c / c.shift(20) - 1
                r60 = c / c.shift(60) - 1
                vol30 = r1.rolling(30).std()
                fwd = c.shift(-h) / c - 1
                vr = np.log(v.rolling(30).mean() / v.shift(30).rolling(30).mean())
                d = pd.DataFrame({"coin": coin, "w": w, "z": z, "z3": z3, "z5": z5, "r5p": r5p, "r20": r20, "r60": r60,
                                  "vol30": vol30, "vr": vr, "fwd": fwd,
                                  "yr": pd.to_datetime(b["timestamp"]).dt.year}).iloc[np.arange(0, len(b), h)]
                rows.append(d)
        g = pd.concat(rows).dropna(subset=["fwd", "r60"])
        g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
        g["tr"] = np.where(g["r60"] > 0.1, "rising", np.where(g["r60"] < -0.1, "falling", "choppy"))
        g["ag"] = np.where(g["vol30"] > g.groupby("coin")["vol30"].transform("median"), "agit", "calm")
        return g
    def summ(df, col):
        r = df.groupby(col, observed=True)["ex"].agg(["count", "mean", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.round(4)
    for h in [3, 5]:
        g = build(h)
        f = g[g["tr"] == "falling"].copy()
        f["zb"] = pd.cut(f["z"], [-99, -1, 0, 0.5, 1, 1.5, 2, 99])
        out[f"falling h{h}: by day z"] = summ(f, "zb")
        up = f[f["z"] > 0]
        s = stats.linregress(up["z"].clip(upper=4), up["ex"])
        out[f"falling h{h}: slope ex on z (z>0)"] = f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} n {len(up)}"
        f["z3b"] = pd.cut(f["z3"], [-99, -1, 0, 1, 2, 99])
        out[f"falling h{h}: by 3-day z"] = summ(f, "z3b")
        if h == 3:
            sub = f[f["z"] > 1]
            out["falling h3 z>1: by year"] = summ(sub, "yr")
            out["falling h3 z>1: by coin"] = summ(sub, "coin")
            out["falling h3 z>1: by agitation proxy"] = summ(sub, "ag")
            out["falling h3 z>1: by window"] = summ(sub, "w")
        ch = g[g["tr"] == "choppy"].copy()
        ch["z5b"] = pd.cut(ch["z5"], [-99, -1.5, -0.5, 0.5, 1.5, 99])
        out[f"choppy h{h}: by 5-day z"] = summ(ch, "z5b")
        dn = ch[ch["z5"] < 0]
        s = stats.linregress(dn["z5"].clip(lower=-4), dn["ex"])
        out[f"choppy h{h}: slope ex on z5 (z5<0)"] = f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} n {len(dn)}"
        if h == 5:
            sub = ch[ch["z5"] < -0.5]
            out["choppy h5 z5<-0.5: by year"] = summ(sub, "yr")
            out["choppy h5 z5<-0.5: by agitation proxy"] = summ(sub, "ag")
            out["choppy h5 z5<-0.5: by coin"] = summ(sub, "coin")
            g["r20q"] = g.groupby("coin")["r20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
            out["h5 r20 quintile x trend (mean)"] = g.groupby(["tr", "r20q"])["ex"].agg(["count", "mean"]).round(4)
            ff = f.copy()
            ff["vrq"] = pd.qcut(ff["vr"], 4, labels=False, duplicates="drop")
            out["falling h5 vr quartile by year (mean)"] = ff.groupby(["yr", "vrq"])["ex"].mean().unstack().round(4)
    return out
