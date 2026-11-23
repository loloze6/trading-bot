def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    G = []; E = []
    for coin, wins in data["bars"].items():
        d24 = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 24, 24)
            d24.extend(c[idx + 24] / c[idx] - 1)
        drift24 = np.mean(d24)
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            ct = ts + pd.Timedelta(hours=1)
            c = df["close"]
            r24 = c / c.shift(24) - 1
            sc = r24.abs().rolling(720, min_periods=240).mean()
            vr = sc / sc.rolling(2000, min_periods=500).median()
            f24 = c.shift(-24) / c - 1 - drift24
            t = pd.DataFrame({"coin": coin, "wd": ct.dt.weekday, "hr": ct.dt.hour, "year": ct.dt.year,
                              "z": r24 / sc, "f24": f24, "f24s": f24 / sc, "vr": vr})
            G.append(t.iloc[np.arange(0, len(t), 24)])
            # evening window: close of bar starting 20h (close 21:00) to close of bar starting 22h (close 23:00)
            e = t[t["hr"] == 21].copy()
            pos = e.index.values
            ok = pos + 2 < len(c)
            e = e[ok]; pos = pos[ok]
            e["ev"] = c.values[pos + 2] / c.values[pos] - 1
            e["evs"] = e["ev"] / e["vr"].values  # unused
            e["ev_sc"] = e["ev"] / sc.values[pos]
            E.append(e)
    A = pd.concat(G).dropna(subset=["z", "f24", "vr"])
    def reg(g, x="z", y="f24"):
        g = g.dropna(subset=[x, y])
        if len(g) < 30: return pd.Series({"n": len(g)})
        s = stats.linregress(g[x], g[y])
        return pd.Series({"n": len(g), "slope": s.slope, "t": s.slope / s.stderr})
    out = {}
    out["24h grid: f24 on z, all"] = reg(A).to_frame().T
    A["volq"] = pd.qcut(A["vr"], 3, labels=["low", "mid", "high"])
    out["24h grid: by vol tercile"] = A.groupby("volq").apply(reg)
    H = A[A["volq"] == "high"]
    out["24h grid high vol: by year"] = H.groupby("year").apply(reg)
    out["24h grid high vol: by coin"] = H.groupby("coin").apply(reg)
    out["24h grid: f24 by vol x z tercile"] = A.assign(zq=pd.qcut(A["z"], 3, labels=["dn", "mid", "up"])).groupby(["volq", "zq"])["f24"].mean().unstack()
    # interaction: f24 on z*vr
    A["zv"] = A["z"] * A["vr"]
    m = np.column_stack([np.ones(len(A)), A["z"], A["zv"]])
    b, *_ = np.linalg.lstsq(m, A["f24"].values, rcond=None)
    res = A["f24"].values - m @ b
    cov = np.linalg.inv(m.T @ m) * res.var(ddof=3)
    out["f24 ~ z + z*volratio"] = pd.DataFrame({"coef": b, "t": b / np.sqrt(np.diag(cov))}, index=["c", "z", "z*vr"])
    Ev = pd.concat(E).dropna(subset=["ev"])
    s = Ev["ev"]
    out["21-23h return: overall"] = pd.Series({"mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))), "n": len(s)}).to_frame().T
    out["21-23h by year"] = Ev.groupby("year")["ev"].agg(lambda x: x.mean() / (x.std() / np.sqrt(len(x)))).to_frame("t").join(Ev.groupby("year")["ev"].mean().rename("mean"))
    out["21-23h by coin"] = Ev.groupby("coin")["ev"].agg(["mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    out["21-23h by weekday"] = Ev.groupby("wd")["ev"].agg(["mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x))), "size"])
    Evd = Ev.dropna(subset=["z", "vr"]).copy()
    Evd["volq"] = pd.qcut(Evd["vr"], 3, labels=["low", "mid", "high"])
    out["21-23h by vol tercile"] = Evd.groupby("volq")["ev"].agg(["mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x))), "size"])
    out["21-23h on prior 24h z"] = reg(Evd, "z", "ev").to_frame().T
    out["21-23h by prior z tercile"] = Evd.groupby(pd.qcut(Evd["z"], 3, labels=["dn", "mid", "up"]))["ev"].agg(["mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    return out
