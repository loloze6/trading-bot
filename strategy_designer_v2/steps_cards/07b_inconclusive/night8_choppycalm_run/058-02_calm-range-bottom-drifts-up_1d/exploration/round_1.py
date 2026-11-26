def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            hi = b["high"].rolling(20).max(); lo = b["low"].rolling(20).min()
            pos = (b["close"] - lo) / (hi - lo) * 2 - 1  # -1 low, +1 high
            c = b["close"].values
            for h in [1, 3, 5, 10, 20]:
                fr = pd.Series(np.nan, index=b.index)
                fr.iloc[:len(b)-h] = c[h:] / c[:-h] - 1
                b[f"fr{h}"] = fr
            b["pos"] = pos; b["coin"] = coin; b["win"] = w
            b["prof"] = (b["regime"] == "unknown")
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["i"] = np.arange(len(b))
            rows.append(b[["coin","win","year","i","pos","prof","forecast","fr1","fr3","fr5","fr10","fr20"]])
    d = pd.concat(rows, ignore_index=True)
    out = {}
    # drift per coin per horizon on own grid
    for h in [1,3,5,10,20]:
        g = d[d["i"] % h == 0]
        dr = g.groupby("coin")[f"fr{h}"].mean()
        d[f"ex{h}"] = d[f"fr{h}"] - d["coin"].map(dr)
    # by position bin, profile vs not, 5-day grid
    g5 = d[(d["i"] % 5 == 0) & d["pos"].notna() & d["ex5"].notna()].copy()
    g5["bin"] = pd.cut(g5["pos"], [-1.01,-0.6,-0.2,0.2,0.6,1.01], labels=["bot","lowmid","mid","highmid","top"])
    def summ(x, col="ex5"):
        v = x[col]; n = len(v)
        return pd.Series({"n": n, "mean%": v.mean()*100, "t": v.mean()/(v.std(ddof=1)/np.sqrt(n)) if n>2 else np.nan})
    out["5d ex by bin, profile"] = g5[g5.prof].groupby("bin").apply(summ)
    out["5d ex by bin, outside profile"] = g5[~g5.prof].groupby("bin").apply(summ)
    # horizons in profile by bin bottom-half
    hz = []
    for h in [1,3,5,10,20]:
        g = d[(d["i"] % h == 0) & d.prof & d["pos"].notna() & d[f"ex{h}"].notna()]
        for side, m in [("lower half", g.pos < 0), ("upper half", g.pos >= 0)]:
            s = summ(g[m], f"ex{h}"); s["h"] = h; s["side"] = side
            sl = stats.linregress(g["pos"], g[f"ex{h}"])
            s["slope_on_pos"] = sl.slope; s["t_slope"] = sl.slope/sl.stderr
            hz.append(s)
    out["profile by horizon and half"] = pd.DataFrame(hz)
    gp = g5[g5.prof]
    out["profile lower half by coin"] = gp[gp.pos < 0].groupby("coin").apply(summ)
    out["profile lower half by year"] = gp[gp.pos < 0].groupby("year").apply(summ)
    out["profile upper half by year"] = gp[gp.pos >= 0].groupby("year").apply(summ)
    out["profile share of bars"] = d.prof.mean()
    return out
