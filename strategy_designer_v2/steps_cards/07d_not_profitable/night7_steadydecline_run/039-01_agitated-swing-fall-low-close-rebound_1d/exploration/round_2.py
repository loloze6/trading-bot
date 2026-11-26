def explore(data):
    import numpy as np, pandas as pd
    out = {}
    recs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = b["close"]; r1 = cl.shift(-1)/cl-1
            ret = cl.pct_change()
            sd30 = ret.rolling(30).std()
            sdy = ret.rolling(30).std()
            # agitation within window: 30d sd vs its own past (approx, window-limited)
            ag = sdy.rolling(len(b), min_periods=30).apply(lambda x: (x<=x[-1]).mean(), raw=True)
            pos = b["postRebalance_current_allocation"]
            recs.append(pd.DataFrame({"coin":c,"window":w,"i":np.arange(len(b)),"r1":r1,"ret":ret,
                "fallz":-ret/sd30,"cloc":(b["high"]-cl)/(b["high"]-b["low"]),
                "tr60":cl/cl.shift(60)-1,"tr30":cl/cl.shift(30)-1,"r3":cl.pct_change(3),
                "pos":pos,"fc":b["forecast"],"regime":b["regime"],"gain":pos*r1}))
    X = pd.concat(recs).dropna(subset=["r1"])
    X["ex"] = X["r1"]-X["coin"].map(X.groupby("coin")["r1"].mean())
    X["sig"] = (X.fc>0)
    X["agit"] = X.regime!="chop"
    X["trend"] = pd.cut(X.tr60,[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    X["trend30"] = pd.cut(X.tr30,[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    # condition check: trend with and without signal, agitated bars
    A = X[X.agit]
    def tt(s):
        s=s.dropna(); return pd.Series({"n":len(s),"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    rows={}
    for tr in ["fall","chop","rise"]:
        for sg in [True,False]:
            rows[(tr,sg)] = tt(A[(A.trend==tr)&(A.sig==sg)].ex)
    out["agit_trend60_x_signal_ex"] = pd.DataFrame(rows).T
    rows={}
    for tr in ["fall","chop","rise"]:
        for sg in [True,False]:
            rows[(tr,sg)] = tt(A[(A.trend30==tr)&(A.sig==sg)].ex)
    out["agit_trend30_x_signal_ex"] = pd.DataFrame(rows).T
    # graded within signal by trend: forecast slope
    S = A[A.sig]
    S = S.assign(fq=pd.qcut(S.fc.rank(method="first"),3,labels=False))
    out["sig_trend60_fq"] = S.groupby(["trend","fq"],observed=True).ex.agg(["size","mean"]).unstack()
    # held bars: gain by trend30 and its std (risk)
    H = X[X.pos>0]
    out["held_trend30"] = H.groupby("trend30",observed=True).agg(n=("gain","size"),gain=("gain","mean"),sd=("gain","std"),worst=("gain","min"),pos=("pos","mean"))
    # w16 episode: held bars in w16 by trend30, losing
    W = X[(X.window=="w16")]
    Wh = W[W.pos>0]
    out["w16_held"] = Wh.groupby(["coin","trend30"],observed=True).agg(n=("gain","size"),gain_sum=("gain","sum"),pos=("pos","mean"),r1=("r1","mean"))
    out["w16_coin_path"] = W.groupby("coin").agg(tr30_mean=("tr30","mean"),ret_sum=("ret","sum"),held=("pos",lambda p:(p>0).mean()))
    # held after bar with fc=0 (carry from min holding / sizing) gain
    out["held_fc0_vs_fcpos"] = H.groupby(H.fc>0).agg(n=("gain","size"),gain=("gain","mean"))
    # prev 3-day fall as condition alone vs with signal (agitated)
    A = A.assign(r3q=pd.qcut(A.r3.rank(method="first"),4,labels=False))
    out["agit_r3q_x_sig"] = A.groupby(["r3q","sig"]).ex.agg(["size","mean"]).unstack()
    return out
