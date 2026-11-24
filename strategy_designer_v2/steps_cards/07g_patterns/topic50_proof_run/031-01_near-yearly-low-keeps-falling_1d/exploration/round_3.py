def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            vol = r.shift(1).rolling(30, min_periods=15).std()
            z = r / vol
            raw = b["debug_info.components.low_prox.last_history_value"]
            n = len(b)
            d = pd.DataFrame(dict(coin=coin, w=w, i=np.arange(n), ts=b["timestamp"], r=r, z=z, vol=vol, raw=raw,
                                  n1=c.shift(-1)/c-1, n3=c.shift(-3)/c-1, n5=c.shift(-5)/c-1,
                                  p60=c/c.shift(60)-1,
                                  lowpos=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = pd.to_datetime(D["ts"]).dt.floor("D")
    def clus_slope(x, y, days):
        x = x - x.mean(); yy = y - y.mean()
        beta = (x*yy).sum()/(x*x).sum()
        e = yy - beta*x
        s = (x*e).groupby(days).sum()
        se = np.sqrt((s**2).sum())/(x*x).sum()
        return beta, beta/se, days.nunique()
    def clus_mean(s, days):
        m = s.mean(); dev = (s-m).groupby(days).sum()
        return m, m/(np.sqrt((dev**2).sum())/len(s)), days.nunique()
    res = {}
    for h in [1,3,5]:
        col = f"n{h}"
        mu = D.groupby("coin")[col].transform("mean")
        D[f"e{h}"] = D[col] - mu
        # non-overlapping grid per window
        G = D[(D["i"] % h == 0)].dropna(subset=["z", f"e{h}"])
        dn = G[G["z"] < 0]
        b_, t_, nd = clus_slope(-dn["z"], dn[f"e{h}"], dn["day"])
        res[f"h{h}_slope_on_dropsize"] = dict(beta=b_, t_day=t_, n=len(dn), days=nd)
        bg = G[G["z"] <= -2]
        m, t, nd = clus_mean(bg[f"e{h}"], bg["day"])
        res[f"h{h}_z<=-2_mean"] = dict(beta=m, t_day=t, n=len(bg), days=nd)
        upg = G[G["z"] > 0]
        b_, t_, nd = clus_slope(upg["z"], upg[f"e{h}"], upg["day"])
        res[f"h{h}_slope_on_risesize"] = dict(beta=b_, t_day=t_, n=len(upg), days=nd)
    out["drop_then_rebound"] = pd.DataFrame(res).T
    G = D[D["i"] % 3 == 0].dropna(subset=["z","e3"])
    dn = G[G["z"] < 0].copy()
    dn["tr"] = np.where(dn["p60"]>0.1,"rising",np.where(dn["p60"]<-0.1,"falling","choppy"))
    rr=[]
    for k,g in dn.groupby("tr"):
        b_,t_,nd = clus_slope(-g["z"], g["e3"], g["day"]); rr.append(dict(tr=k,beta=b_,t=t_,n=len(g)))
    out["h3_drop_slope_by_trend"] = pd.DataFrame(rr)
    dn["near"] = dn["raw"] > dn["raw"].median()
    rr=[]
    for k,g in dn.dropna(subset=["raw"]).groupby("near"):
        b_,t_,nd = clus_slope(-g["z"], g["e3"], g["day"]); rr.append(dict(near=k,beta=b_,t=t_,n=len(g)))
    out["h3_drop_slope_by_nearlow"] = pd.DataFrame(rr)
    rr=[]
    for k,g in dn.groupby("w"):
        rr.append(dict(w=k, n=len(g), corr=np.corrcoef(-g["z"], g["e3"])[0,1]))
    out["h3_drop_corr_by_window"] = pd.DataFrame(rr)
    # close location in day's range on big drop days
    bd = D[(D["z"]<=-1.5)].dropna(subset=["e1","lowpos"]).copy()
    bd["lp"] = pd.qcut(bd["lowpos"].rank(method="first"),3,labels=["closelow","mid","closehigh"])
    out["bigdrop_next1_by_closeloc"] = bd.groupby("lp")["e1"].agg(["size","mean"])
    return out
