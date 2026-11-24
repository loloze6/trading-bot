def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; h = 14
    drift = {}
    for coin, ws in bars.items():
        rs = []
        for w, df in ws.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - h, h)
            rs += list(c[idx + h] / c[idx] - 1)
        drift[coin] = (np.mean(rs), np.std(rs))
    cases = []; grid = []
    for coin, ws in bars.items():
        d, s = drift[coin]
        for w, df in ws.items():
            c = df["close"].astype(float).reset_index(drop=True)
            v = df["volume"].astype(float).reset_index(drop=True)
            f = df["forecast"].astype(float).fillna(0).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            ret14 = c / c.shift(14) - 1; ret60 = c / c.shift(60) - 1; ret30 = c / c.shift(30) - 1
            vr = v.rolling(14).mean() / v.rolling(30).mean() - 1
            n = len(c)
            # step-5 style cases
            low = 0.0; taken = set()
            for i in range(n):
                fi = f.iloc[i]
                if fi >= 0:
                    low = 0.0; continue
                if fi <= low - 2:
                    cell = i // h
                    low = fi
                    if cell not in taken and i + h < n:
                        taken.add(cell)
                        r = c.iloc[i + h] / c.iloc[i] - 1
                        cases.append(dict(coin=coin, w=w, year=ts.iloc[i].year, day=ts.iloc[i].normalize(),
                                          f=fi, vr=vr.iloc[i], ret14=ret14.iloc[i], ret60=ret60.iloc[i],
                                          ret30=ret30.iloc[i], sx=-(r - d), sz=-(r - d) / s))
            # all-offset grid situation (offsets 0..13, each its own grid)
            for off in range(h):
                for i in range(off, n - h, h):
                    if ret14.iloc[i] > 0 and vr.iloc[i] < 0 and not np.isnan(ret60.iloc[i]):
                        r = c.iloc[i + h] / c.iloc[i] - 1
                        grid.append(dict(off=off, coin=coin, day=ts.iloc[i].normalize(), year=ts.iloc[i].year,
                                         vr=vr.iloc[i], ret60=ret60.iloc[i], sx=-(r - d)))
    C = pd.DataFrame(cases); G = pd.DataFrame(grid)

    def st(g, col="sx"):
        x = g[col].dropna(); dd = g.loc[x.index, "day"]
        if len(x) < 5:
            return pd.Series(dict(n=len(x), mean=np.nan, t=np.nan, days=np.nan))
        dev = (x - x.mean()).groupby(dd).sum(); k = len(dev)
        se = np.sqrt((dev ** 2).sum() * k / max(k - 1, 1)) / len(x)
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / se, days=k))
    out = {}
    out["step5 cases all"] = st(C).to_frame().T
    C["r60s"] = np.where(C.ret60 > 0, "up", np.where(C.ret60 <= 0, "down", "na"))
    out["step5 cases by ret60 sign"] = C.groupby("r60s").apply(st)
    out["step5 cases by vr quartile"] = C.groupby(pd.qcut(C.vr, 4, labels=["driest","q2","q3","mildest"])).apply(st)
    out["step5 cases by forecast quartile"] = C.groupby(pd.qcut(C.f.rank(method="first"), 4, labels=["deepest","q2","q3","shallow"])).apply(st)
    Cd = C[C.r60s == "down"]
    out["step5 ret60down by vr half"] = Cd.groupby(pd.qcut(Cd.vr, 2, labels=["drier","milder"])).apply(st)
    out["step5 ret60down by year"] = Cd.groupby("year").apply(st)
    out["corr vr vs sx, ret60 down / up"] = pd.Series({"down": Cd[["vr","sx"]].corr().iloc[0,1],
                                                       "up": C[C.r60s=="up"][["vr","sx"]].corr().iloc[0,1]})
    G["r60s"] = np.where(G.ret60 > 0, "up", "down")
    out["grid all offsets: mean of per-offset t by ret60 sign"] = G.groupby(["r60s","off"]).apply(st).groupby(level=0)[["n","mean","t"]].mean()
    Gd = G[G.r60s == "down"]
    out["grid ret60down by vr half (mean over offsets)"] = Gd.groupby([pd.qcut(Gd.vr, 2, labels=["drier","milder"]), "off"]).apply(st).groupby(level=0)[["n","mean","t"]].mean()
    out["grid all-offset situation (mean over offsets)"] = G.groupby("off").apply(st)[["n","mean","t"]].mean().to_frame().T
    return out
