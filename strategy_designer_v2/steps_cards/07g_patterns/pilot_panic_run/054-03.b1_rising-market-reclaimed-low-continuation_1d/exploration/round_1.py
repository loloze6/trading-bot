def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [3, 10]
    rows = []
    # build per coin-window feature frames
    frames = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            d = df[["timestamp","open","high","low","close","regime"]].copy().reset_index(drop=True)
            d["coin"]=coin; d["w"]=w; d["pos"]=np.arange(len(d))
            d["low30"]=d["low"].rolling(30).min().shift(1)
            d["high30"]=d["high"].rolling(30).max().shift(1)
            d["ret1"]=d["close"].pct_change()
            d["rising"]=(d["regime"]!="chop")
            d["vol30"]=d["ret1"].rolling(30).std()
            d["day"]=pd.to_datetime(d["timestamp"]).dt.floor("D")
            d["wd"]=pd.to_datetime(d["timestamp"]).dt.weekday
            for h in H:
                d[f"f{h}"]=d["close"].shift(-h)/d["close"]-1
            frames.append(d)
    A = pd.concat(frames, ignore_index=True)
    # drift per coin per h from non-overlapping grid
    drift = {}
    for h in H:
        g = A[A["pos"]%h==0]
        drift[h] = g.groupby("coin")[f"f{h}"].mean()
    A["volq"]=A.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    ev = {
        "pierce_reclaim": (A["low"]<A["low30"])&(A["close"]>=A["low30"]),
        "close_below_low30": A["close"]<A["low30"],
        "pierce_high_fail": (A["high"]>A["high30"])&(A["close"]<=A["high30"]),
        "close_above_high30": A["close"]>A["high30"],
        "bigdown_day": A["ret1"]< -2*A["vol30"],
        "bigup_day": A["ret1"]> 2*A["vol30"],
    }
    def stat(mask, h):
        sub = A[mask & A[f"f{h}"].notna()].copy()
        if len(sub)==0: return dict(n=0)
        sub["cell"]=sub["pos"]//h
        sub = sub.groupby(["coin","w","cell"]).head(1)
        sub["u"]=sub[f"f{h}"]-sub["coin"].map(drift[h])
        per = sub.groupby("day")["u"].sum()
        G=len(per); m=sub["u"].mean(); n=len(sub)
        se = np.sqrt((per**2).sum()*G/(G-1))/n if G>1 else np.nan
        return dict(n=n, days=G, mean_unusual=m, t_day=m/se if se else np.nan, mean_total=sub[f"f{h}"].mean())
    for name, m in ev.items():
        for h in H:
            for reg, rm in [("all", A["rising"]|~A["rising"]),("rising",A["rising"]),("notrising",~A["rising"])]:
                r = stat(m & rm, h); r.update(event=name,h=h,reg=reg); rows.append(r)
    out = {"events": pd.DataFrame(rows)}
    # vol tercile next-10 unusual for all grid bars
    vr=[]
    for h in H:
        g=A[(A["pos"]%h==0)&A[f"f{h}"].notna()].copy()
        g["u"]=g[f"f{h}"]-g["coin"].map(drift[h])
        for q,s in g.groupby("volq"):
            vr.append(dict(h=h,volq=q,n=len(s),mean=s["u"].mean(),t=s["u"].mean()/(s["u"].std()/np.sqrt(len(s)))))
        for reg,s in g.groupby("rising"):
            vr.append(dict(h=h,volq=f"rising={reg}",n=len(s),mean=s["u"].mean(),t=s["u"].mean()/(s["u"].std()/np.sqrt(len(s)))))
    out["vol_regime"]=pd.DataFrame(vr)
    wdr = A.dropna(subset=["ret1"]).groupby("wd")["ret1"].agg(["mean","std","count"])
    wdr["t"]=wdr["mean"]/(wdr["std"]/np.sqrt(wdr["count"]))
    out["weekday"]=wdr
    # book: days
    dd=[]
    for coin, ws in data["days"].items():
        for w, df in ws.items():
            x=df.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    D=pd.concat(dd)
    out["book_by_window"]=D.groupby("w")["book_return"].agg(["mean","sum","count"])
    T=[]
    for coin, ws in data["trades"].items():
        for w, df in ws.items():
            if len(df): x=df.copy(); x["coin"]=coin; x["w"]=w; T.append(x)
    if T:
        T=pd.concat(T)
        out["trades_by_coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","sum"])
        out["trades_by_side"]=T.groupby("side")["net_profit_loss_percent"].agg(["count","mean"])
    return out
