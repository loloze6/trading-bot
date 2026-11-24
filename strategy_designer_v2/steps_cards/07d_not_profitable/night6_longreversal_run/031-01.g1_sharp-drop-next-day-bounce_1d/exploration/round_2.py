def explore(data):
    import pandas as pd, numpy as np
    out = {}
    recs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp")
            cl = b["close"].astype(float)
            r = cl.pct_change()
            df = pd.DataFrame({
                "ts": pd.to_datetime(b["timestamp"]).dt.floor("D").values,
                "fc": b["forecast"].values.astype(float),
                "alloc": b["postRebalance_current_allocation"].values.astype(float),
                "fwd": (cl.shift(-1)/cl-1).values,
                "r1": r.values,
                "vol30": r.rolling(30).std().values,
                "vol7": r.rolling(7).std().values,
                "ret20": (cl/cl.shift(20)-1).values,
            })
            df["coin"] = c; df["w"] = w
            recs.append(df)
    D = pd.concat(recs, ignore_index=True)
    D["wn"] = D["w"].str[1:].astype(int)
    cm = D.groupby("coin")["fwd"].mean()
    D["ex"] = D["fwd"] - D["coin"].map(cm)
    D["vr"] = D["vol7"]/D["vol30"]
    D["z"] = D["r1"]/D["vol30"]
    cost_side = 0.0019/2

    def book(mask_mult, name):
        X = D.copy()
        X["a"] = X["alloc"]*mask_mult
        X["a"] = X["a"].fillna(0)
        X["prev"] = X.groupby(["coin","w"])["a"].shift(1).fillna(0)
        X["g"] = X["a"]*X["fwd"].fillna(0) - cost_side*(X["a"]-X["prev"]).abs()
        d = X.groupby(["wn","ts"])["g"].mean().sort_index()
        v = (1+d).cumprod(); dd = (v/v.cummax()-1).min()
        yrs = len(d)/365
        yr = v.iloc[-1]**(1/yrs)-1
        inpos = (X["a"]>0).mean()
        return pd.Series({"sharpe": d.mean()/d.std()*np.sqrt(365), "yearly": yr, "maxdd": dd,
                          "calmar": yr/abs(dd), "share in pos": inpos, "mean/day in pos": d.mean()/max(inpos,1e-9)})
    one = pd.Series(1.0, index=D.index)
    res = {}
    res["base (approx)"] = book(one, "base")
    res["fc>8 only"] = book((D.fc>8).astype(float), "")
    res["fc>12 only"] = book((D.fc>12).astype(float), "")
    res["vr above median"] = book((D.vr>D.vr.median()).astype(float), "")
    res["fc>8 & vr>median"] = book(((D.fc>8)&(D.vr>D.vr.median())).astype(float), "")
    vrk = D["vr"].rank(pct=True)
    res["scaled by vr rank*2"] = book((2*vrk).clip(0,2), "")
    res["fc>8 scaled vr*2"] = book(((D.fc>8)*(2*vrk)).clip(0,2), "")
    out["variant books"] = pd.DataFrame(res).T
    # condition alone check: vol ratio high without signal, and with signal, by z of fall
    S = D.dropna(subset=["fwd","vr","z"]).copy()
    S["vrq"] = pd.qcut(S["vr"], 4, labels=["calm","2","3","hot"])
    S["zb"] = pd.cut(S["z"], [-99,-2,-1.5,-1,-0.5,0,99])
    out["ex by z bin x vrq"] = S.groupby(["zb","vrq"], observed=True)["ex"].mean().unstack()
    out["n by z bin x vrq"] = S.groupby(["zb","vrq"], observed=True)["ex"].size().unstack()
    # t of ex in hot & z<-1 clustered by day
    sub = S[(S.vrq=="hot")&(S.z<-1)]
    g = sub.groupby("ts")["ex"].sum(); n=len(sub)
    out["hot & z<-1"] = pd.Series({"n": n, "days": len(g), "ex mean": sub.ex.mean(), "t day-clustered": sub.ex.sum()/np.sqrt((g**2).sum())})
    sub2 = S[(S.vrq=="hot")&(S.z>=0)]
    out["hot & up day (no signal)"] = pd.Series({"n": len(sub2), "ex": sub2.ex.mean()})
    # during deepest fall w9: losses by fc bin
    W = D[D.w.isin(["w8","w9"])].dropna(subset=["fwd"])
    W["gain"]=W.alloc*W.fwd
    W["fcb"]=pd.cut(W.fc,[0,8,12,20.01])
    out["w8-w9 gain by fc bin"] = W.groupby("fcb",observed=True).agg(n=("gain","size"),sum_gain=("gain","sum"),ex=("ex","mean"))
    return out
