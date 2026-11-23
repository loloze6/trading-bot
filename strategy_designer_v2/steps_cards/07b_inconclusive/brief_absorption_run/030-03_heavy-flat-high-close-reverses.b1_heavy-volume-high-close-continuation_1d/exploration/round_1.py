def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1,3,5,10,20]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        for h in H:
            g = []
            for w, df in ws.items():
                c = df["close"].values
                for i in range(0, len(c)-h, h):
                    g.append(c[i+h]/c[i]-1)
            drift[(coin,h)] = (np.mean(g), np.std(g))
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values; o = df["open"].values
            v = df["volume"].values
            rng = hi - lo
            cl = np.where(rng > 0, (2*c - hi - lo)/np.where(rng>0,rng,1), 0)
            vr = v / pd.Series(v).shift(1).rolling(20, min_periods=20).mean().values
            body = np.where(rng>0, np.abs(c-o)/np.where(rng>0,rng,1), np.nan)
            ret1 = pd.Series(c).pct_change().values
            f = df["forecast"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(c)
            for i in range(n):
                r = {"coin": coin, "w": w, "i": i, "cell": i//10, "cl": cl[i], "vr": vr[i],
                     "body": body[i], "f": f[i], "year": yr[i], "r1": ret1[i]}
                for h in H:
                    if i+h < n:
                        r["u%d"%h] = c[i+h]/c[i]-1 - drift[(coin,h)][0]
                    else:
                        r["u%d"%h] = np.nan
                rows.append(r)
    D = pd.DataFrame(rows)
    # heavy-volume days: vr top; one per grid cell (first) for 10-day
    def summ(sub, col="u10"):
        x = sub[col].dropna()
        if len(x) < 3: return pd.Series({"n": len(x), "mean": np.nan, "t": np.nan})
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))})
    heavy = D[D["vr"] >= 2.0]
    hv1 = heavy.sort_values("i").groupby(["coin","w","cell"]).head(1)
    out = {}
    hv1 = hv1.copy()
    hv1["clb"] = pd.cut(hv1["cl"], [-1.01,-0.5,0,0.5,1.01])
    out["heavy vr>=2, by close-loc bucket, u10"] = hv1.groupby("clb").apply(summ)
    for h in [1,3,5,20]:
        out["heavy by clb u%d"%h] = hv1.groupby("clb").apply(lambda s: summ(s,"u%d"%h))
    # ordinary days by clb
    ordd = D[(D["vr"] < 1.2)].sort_values("i").groupby(["coin","w","cell"]).head(1).copy()
    ordd["clb"] = pd.cut(ordd["cl"], [-1.01,-0.5,0,0.5,1.01])
    out["ordinary vr<1.2 by clb u10"] = ordd.groupby("clb").apply(summ)
    # flat heavy days (small body)
    fl = hv1[hv1["body"] < 0.3]
    out["heavy & flat body<0.3 by clb u10"] = fl.groupby("clb").apply(summ)
    # heavy high-close: by coin, year, sign of day return
    hh = hv1[hv1["cl"] > 0.5].copy()
    out["heavy high-close by coin u10"] = hh.groupby("coin").apply(summ)
    out["heavy high-close by year u10"] = hh.groupby("year").apply(summ)
    hh["up"] = hh["r1"] > 0
    out["heavy high-close by day up u10"] = hh.groupby("up").apply(summ)
    # replicated cases: forecast>=2 first per cell
    cs = D[D["f"] >= 2].sort_values("i").groupby(["coin","w","cell"]).head(1).copy()
    cs["fq"] = pd.qcut(cs["f"], 4, labels=False, duplicates="drop")
    out["cases by forecast quartile u10"] = cs.groupby("fq").apply(summ)
    out["cases by coin u10"] = cs.groupby("coin").apply(summ)
    out["cases by year u10"] = cs.groupby("year").apply(summ)
    out["cases vr bucket u10"] = cs.groupby(pd.cut(cs["vr"],[0,1,1.5,2,3,100])).apply(summ)
    out["cases all horizons"] = pd.DataFrame({h: summ(cs,"u%d"%h) for h in H})
    # graded: correlation cl*vr with u10 among heavy
    x = hv1.dropna(subset=["u10"])
    out["heavy: spearman cl vs u10"] = float(stats.spearmanr(x["cl"], x["u10"])[0])
    out["heavy: n"] = len(x)
    return out
