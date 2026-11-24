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
            for L in (3,5,10,20):
                d[f"m{L}"] = (c.pct_change(L)/(d["vol60"]*np.sqrt(L)))
            for h in (3,5,10,20):
                d[f"f{h}"] = c.shift(-h)/c - 1
            d["day"] = pd.to_datetime(d["timestamp"]).dt.floor("D")
            d["year"] = pd.to_datetime(d["timestamp"]).dt.year
            d["pos"] = np.arange(len(d)); d["coin"] = coin; d["win"] = w
            d["wn"] = int(w[1:])
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def slope(g, x, y):
        g = g[[x,y,"day"]].dropna()
        if len(g) < 30: return (len(g), np.nan, np.nan)
        X = g[x].values; Y = g[y].values
        xm = X - X.mean(); b = (xm*(Y-Y.mean())).sum()/(xm**2).sum()
        e = Y - Y.mean() - b*xm
        s = pd.Series(xm*e).groupby(g["day"].values).sum()
        se = np.sqrt((s**2).sum())/(xm**2).sum()
        return (len(g), g["day"].nunique(), b*100, b/se)
    def prep(h):
        g = A[(A["pos"] % h == 0)].copy()
        mu = g.groupby("coin")[f"f{h}"].mean()
        g["ex"] = g[f"f{h}"] - g["coin"].map(mu)
        return g
    res = []
    for L in (3,5,10,20):
        for h in (3,5,10,20):
            g = prep(h)
            n, dd, b, t = slope(g, f"m{L}", "ex")
            gp = g[g[f"m{L}"]>0]; gn = g[g[f"m{L}"]<0]
            _,_,bp,tp = slope(gp, f"m{L}", "ex"); _,_,bn,tn = slope(gn, f"m{L}", "ex")
            res.append((L,h,n,dd,b,t,bp,tp,bn,tn))
    out["slope ex on mL, pooled"] = pd.DataFrame(res, columns=["L","h","n","days","b%","t","b_up%","t_up","b_dn%","t_dn"])
    for L,h in ((5,10),(10,10),(20,20)):
        g = prep(h)
        pc = []
        for coin, gg in g.groupby("coin"):
            pc.append((coin,)+slope(gg, f"m{L}", "ex"))
        g["half"] = np.where(g["wn"]<=12, "w1-12", "w13-24")
        for hf, gg in g.groupby("half"):
            pc.append((hf,)+slope(gg, f"m{L}", "ex"))
        out[f"by coin/half L{L} h{h}"] = pd.DataFrame(pc, columns=["grp","n","days","b%","t"]).set_index("grp")
        g["q"] = pd.cut(g[f"m{L}"], [-np.inf,-2,-1,0,1,2,np.inf])
        out[f"bins L{L} h{h}"] = g.groupby("q")["ex"].agg(["size","mean"])
    # book's largest days
    D = pd.concat([df.assign(coin=c, win=w) for c, ws in data["days"].items() for w, df in ws.items()])
    bk = D.groupby(["win","day"])[["book_return","coin_return"]].mean().dropna()
    q = bk["book_return"].quantile([0.02,0.98])
    out["book tails"] = pd.DataFrame({
        "worst2%": bk[bk.book_return<=q.iloc[0]].mean(),
        "best2%": bk[bk.book_return>=q.iloc[1]].mean(),
        "all": bk.mean()})
    return out
