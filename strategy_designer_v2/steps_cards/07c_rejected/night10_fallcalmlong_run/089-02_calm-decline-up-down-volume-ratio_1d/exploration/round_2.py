def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            up = (r1 > 0).astype(float); dn = (r1 < 0).astype(float)
            upv = (v*up).rolling(20).sum()/up.rolling(20).sum()
            dnv = (v*dn).rolling(20).sum()/dn.rolling(20).sum()
            base = v.rolling(60).mean()
            lr = np.log(upv/dnv)
            upr = np.log(upv/base); dnr = np.log(dnv/base)
            vs = np.log(v.rolling(10).mean()/base)
            vs20 = np.log(v.rolling(20).mean()/base)
            upshare = up.rolling(20).mean()
            n = len(b)
            for h in [5,10,20]:
                fwd = c.shift(-h)/c - 1
                for i in range(0, n, h):
                    if i+h >= n or pd.isna(fwd.iloc[i]): continue
                    ts = pd.Timestamp(b["timestamp"].iloc[i])
                    rows.append(dict(coin=coin, w=w, h=h, year=ts.year, fc=b["regime"].iloc[i]=="unknown",
                                     lr=lr.iloc[i], upr=upr.iloc[i], dnr=dnr.iloc[i], vs=vs.iloc[i], vs20=vs20.iloc[i],
                                     upshare=upshare.iloc[i], fwd=fwd.iloc[i], day=ts.floor("D")))
    df = pd.DataFrame(rows)
    df["ex"] = df["fwd"] - df.groupby(["coin","h"])["fwd"].transform("mean")
    out = {}
    fc = df[df.fc]
    res = []
    for col in ["lr","upr","dnr","vs","vs20","upshare"]:
        for h in [5,10,20]:
            g = fc[fc.h==h].dropna(subset=[col,"ex"])
            if len(g) < 10: continue
            rho, p = stats.spearmanr(g[col], g["ex"])
            zc = (g[col]-g[col].mean())/g[col].std()
            prod = zc*g["ex"]
            dd = prod.groupby(g["day"]).sum()
            tcl = prod.mean()/(np.sqrt((dd**2).sum())/len(prod)) if len(prod)>0 else np.nan
            res.append(dict(var=col, h=h, n=len(g), days=g["day"].nunique(), rho=rho, p=p, t_slope_cl=tcl))
    out["fc_graded"] = pd.DataFrame(res)
    for col in ["vs","dnr","upr"]:
        for h in [5,10]:
            q = fc[fc.h==h].dropna(subset=[col]).copy()
            q["qb"] = pd.qcut(q[col],4,labels=False)
            out[f"q_{col}_h{h}"] = q.groupby("qb").agg(n=("ex","size"), x=(col,"mean"), ex=("ex","mean"), tot=("fwd","mean"))
    nf = df[~df.fc]
    res2=[]
    for col in ["vs","dnr","lr"]:
        for h in [5,10]:
            g = nf[nf.h==h].dropna(subset=[col])
            res2.append(dict(var=col,h=h,n=len(g),rho=stats.spearmanr(g[col],g["ex"])[0]))
    out["outside_fc"] = pd.DataFrame(res2)
    g = fc[fc.h==5].dropna(subset=["vs"])
    out["vs_h5_by_coin"] = g.groupby("coin").apply(lambda x: pd.Series(dict(n=len(x), rho=stats.spearmanr(x.vs,x.ex)[0])))
    out["vs_h5_by_year"] = g.groupby("year").apply(lambda x: pd.Series(dict(n=len(x), rho=stats.spearmanr(x.vs,x.ex)[0])))
    return out
