def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # book daily
    wins = sorted(data["days"]["BTCUSD"].keys(), key=lambda w:int(w[1:]))
    books=[]
    for w in wins:
        cols=[]
        for c in data["days"]:
            d=data["days"][c][w].set_index("day")["book_return"]
            cols.append(d.rename(c))
        df=pd.concat(cols,axis=1).mean(axis=1).dropna()
        books.append(pd.DataFrame({"w":w,"r":df.values}))
    B=pd.concat(books,ignore_index=True)
    eq=(1+B.r).cumprod(); dd=eq/eq.cummax()-1
    B["dd"]=dd.values
    per=B.groupby("w").agg(mean=("r","mean"),sum=("r","sum"),mindd=("dd","min"),n=("r","size"))
    # within-window maxdd
    per["win_mdd"]=B.groupby("w")["r"].apply(lambda s:((1+s).cumprod()/(1+s).cumprod().cummax()-1).min())
    out["per_window"]=per.reindex(wins).round(4)
    out["overall_mdd"]=float(dd.min()); out["ann"]=float(B.r.mean()*365)
    # per-bar position analysis
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy()
            cl=b.close
            r1=cl.pct_change()
            nxt=cl.shift(-1)/cl-1
            a=b.postRebalance_current_allocation.astype(float)
            mad=r1.abs().rolling(60,min_periods=20).mean()
            z=r1/mad
            r20=cl/cl.shift(20)-1; r5=cl/cl.shift(5)-1
            vol20=r1.rolling(20).std(); vol60=r1.rolling(60).std()
            hi20=cl/cl.rolling(20).max()-1
            dn=(r1<0).astype(int)
            run=dn.groupby((dn==0).cumsum()).cumsum()
            rows.append(pd.DataFrame({"c":c,"w":w,"a":a,"f":b.forecast,"nxt":nxt,"z":z,"r20":r20,"r5":r5,
                 "vr":vol20/vol60,"vol20":vol20,"hi20":hi20,"run":run,"pnl":a*nxt}))
    D=pd.concat(rows,ignore_index=True).dropna(subset=["nxt"])
    H=D[D.a>0].copy()
    out["held_share_bars"]=float(len(H)/len(D))
    out["alloc_desc"]=H.a.describe().round(3)
    def g(col,q=5):
        H["_b"]=pd.qcut(H[col],q,duplicates="drop")
        t=H.groupby("_b",observed=True).agg(n=("nxt","size"),nxt=("nxt","mean"),pnl=("pnl","mean"),pnl_sum=("pnl","sum"),p5=("pnl",lambda s:s.quantile(.05)))
        return t.round(5)
    for col in ["f","z","r20","r5","vr","vol20","hi20","run"]:
        out["by_"+col]=g(col)
    # worst 5% book days? use coin-level worst pnl bars: conditions
    w=H.pnl.quantile(.02)
    out["worst2pct_vs_all"]=pd.DataFrame({"worst":H[H.pnl<=w][["z","r20","r5","vr","vol20","hi20","run","a"]].median(),
                                          "all":H[["z","r20","r5","vr","vol20","hi20","run","a"]].median()}).round(4)
    out["by_coin"]=H.groupby("c").agg(n=("pnl","size"),pnl=("pnl","mean"),sum=("pnl","sum"))
    return out
