import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","close"]].copy().reset_index(drop=True)
            c = pd.Series(d["close"].values)
            r1 = c.pct_change()
            d["vol60"] = r1.rolling(60).std()
            d["z1"] = r1/d["vol60"]
            d["m5"] = c.pct_change(5)/(d["vol60"]*np.sqrt(5))
            d["m10"] = c.pct_change(10)/(d["vol60"]*np.sqrt(10))
            for h in (1,2,5,10):
                d[f"f{h}"] = c.shift(-h)/c - 1
            d["day"] = pd.to_datetime(d["timestamp"]).dt.floor("D")
            d["pos"] = np.arange(len(d)); d["coin"] = coin; d["wn"] = int(w[1:])
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def slope(g, x, y):
        g = g[[x,y,"day"]].dropna()
        if len(g) < 30: return (len(g), np.nan, np.nan, np.nan)
        X = g[x].values; Y = g[y].values
        xm = X - X.mean(); b = (xm*(Y-Y.mean())).sum()/(xm**2).sum()
        e = Y - Y.mean() - b*xm
        s = pd.Series(xm*e).groupby(g["day"].values).sum()
        se = np.sqrt((s**2).sum())/(xm**2).sum()
        return (len(g), g["day"].nunique(), b*100, b/se)
    def prep(h, off=0):
        g = A[(A["pos"] % h == off)].copy()
        mu = A[A["pos"] % h == 0].groupby("coin")[f"f{h}"].mean()
        g["ex"] = g[f"f{h}"] - g["coin"].map(mu)
        return g
    # grid offsets robustness for rise continuation, positive side
    res = []
    for L in ("m5","m10"):
        for off in range(10):
            g = prep(10, off); gp = g[g[L]>0]
            n,dd,b,t = slope(gp, L, "ex")
            top = gp[gp[L]>2]["ex"]
            res.append((L, off, n, b, t, len(top), top.mean()*100))
    out["offsets rise h10"] = pd.DataFrame(res, columns=["L","off","n","b%","t","n_top","top_ex%"])
    g = prep(10); gp = g[g["m5"]>0]
    pc = []
    for coin, gg in gp.groupby("coin"): pc.append((coin,)+slope(gg,"m5","ex"))
    gp = gp.assign(half=np.where(gp["wn"]<=12,"w1-12","w13-24"))
    for hf, gg in gp.groupby("half"): pc.append((hf,)+slope(gg,"m5","ex"))
    out["rise side m5 h10 by coin/half"] = pd.DataFrame(pc, columns=["grp","n","days","b%","t"]).set_index("grp")
    # raw vol-scaled fall (no vol weighting) for rebound
    res = []
    for h in (1,2,5):
        for off in range(h):
            g = prep(h, off); gn = g[g["z1"]<0].copy(); gn["fall"] = -gn["z1"]
            n,dd,b,t = slope(gn, "fall", "ex")
            res.append((h, off, n, dd, b, t))
    out["fall z slope"] = pd.DataFrame(res, columns=["h","off","n","days","b%","t"])
    return out
