def explore(data):
    import pandas as pd, numpy as np
    out = {}
    bars = data["bars"]
    recs=[]
    for c in bars:
        for w,df in bars[c].items():
            df=df.reset_index(drop=True)
            cl=df.close; pos=df.postRebalance_current_allocation.fillna(0)
            nr=cl.shift(-1)/cl-1
            r30=cl/cl.shift(30)-1
            r5=cl/cl.shift(5)-1
            r90=cl/cl.shift(90)-1
            hi=df.high.rolling(30).max(); lo=df.low.rolling(30).min()
            t=pd.DataFrame({"c":c,"w":w,"pos":pos,"pnl":pos*nr,"side":np.sign(pos),
              "bir":df["debug_info.bars_in_regime"],"r5dir":np.sign(pos)*r5,
              "r30dir":np.sign(pos)*r30,"r90dir":np.sign(pos)*r90,"abspos":pos.abs()})
            recs.append(t)
    a=pd.concat(recs); a=a[a.pos!=0].dropna(subset=["pnl"])
    wn=a.w.str[1:].astype(int)
    a["stretch"]=np.where((wn>=3)&(wn<=10),"dd_w3_w10","rest")
    def st(x):
        r=x.groupby(list(x.columns[:0]) or None)
    g=a.groupby(["stretch","side"])["pnl"].agg(["mean","count","sum"])
    out["stretch_side"]=g.round(5)
    out["stretch_coin"]=a.groupby(["stretch","c"])["pnl"].agg(["mean","sum"]).unstack(0).round(4)
    a["birb"]=pd.cut(a.bir,[0,2,4,9,100])
    out["stretch_bir"]=a.groupby(["stretch","birb"],observed=True)["pnl"].agg(["mean","count","sum"]).round(5)
    a["r30b"]=pd.qcut(a.r30dir,4)
    out["side_r30"]=a.groupby(["side","r30b"],observed=True)["pnl"].agg(["mean","count","sum"]).round(5)
    a["r90b"]=pd.qcut(a.r90dir,4,duplicates="drop")
    x=a.dropna(subset=["r90dir"])
    r=x.groupby("r90b",observed=True)["pnl"].agg(["mean","std","count","sum"])
    r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]))
    out["by_r90dir"]=r.round(5)
    out["stretch_r90"]=x.groupby(["stretch","r90b"],observed=True)["pnl"].agg(["mean","sum"]).round(5)
    a["r5b"]=pd.qcut(a.r5dir,4)
    out["stretch_r5"]=a.groupby(["stretch","r5b"],observed=True)["pnl"].agg(["mean","sum"]).round(5)
    # abs allocation in stretch
    out["abspos_by_stretch"]=a.groupby("stretch")["abspos"].mean().round(3)
    # worst 5% bar losses: share by side and bir
    q=a.pnl.quantile(0.02); wl=a[a.pnl<q]
    out["worst2pct_side_bir"]=wl.groupby(["side","birb"],observed=True)["pnl"].agg(["count","sum"]).round(4)
    out["worst2pct_r5"]=wl.groupby("r5b",observed=True)["pnl"].agg(["count","sum"]).round(4)
    return out
