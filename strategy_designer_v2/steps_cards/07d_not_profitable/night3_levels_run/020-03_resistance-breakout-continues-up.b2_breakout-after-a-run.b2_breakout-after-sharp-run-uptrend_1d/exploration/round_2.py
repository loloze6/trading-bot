def explore(data):
    import pandas as pd, numpy as np
    days=data["days"]; bars=data["bars"]
    coins=list(days.keys())
    wins=sorted({w for c in coins for w in days[c].keys()}, key=lambda s:int(s[1:]))
    # book chain and drawdown flags per day
    rows=[]
    for w in wins:
        fr=[]
        for c in coins:
            if w in days[c]:
                d=days[c][w][["day","book_return","coin_return"]].copy(); d["coin"]=c; fr.append(d)
        f=pd.concat(fr)
        g=f.groupby("day").agg(book=("book_return","mean"),hold=("coin_return","mean")).reset_index(); g["w"]=w; rows.append(g)
    B=pd.concat(rows).dropna(subset=["book"]).reset_index(drop=True)
    eq=(1+B.book).cumprod(); dd=eq/eq.cummax()-1
    # falling phase: from peak to trough of episodes deeper than 15%
    B["falling"]=False
    i=0;n=len(B)
    while i<n:
        if dd.iloc[i]<0:
            j=i
            while j<n and dd.iloc[j]<0: j+=1
            seg=dd.iloc[i:j]
            if seg.min()<-0.15:
                k=int(seg.idxmin()); B.loc[i:k,"falling"]=True
            i=j
        else: i+=1
    fallday=set(zip(B.w,B.day.astype(str)))
    P=[]
    for c in coins:
        for w in bars[c]:
            b=bars[c][w].copy()
            cl=b.close; lr=np.log(cl).diff()
            b["g"]=b.postRebalance_current_allocation*(cl.shift(-1)/cl-1)
            b["a"]=b.postRebalance_current_allocation
            b["vol20"]=lr.rolling(20).std()*np.sqrt(365)
            b["vol_ratio"]=lr.rolling(10).std()/lr.rolling(60).std()
            b["r60"]=cl/cl.shift(60)-1
            b["r20"]=cl/cl.shift(20)-1
            b["r30"]=cl/cl.shift(30)-1
            b["ma50"]=cl/cl.rolling(50).mean()-1
            b["day"]=pd.to_datetime(b.timestamp).dt.floor("D").astype(str)
            b["w"]=w; b["coin"]=c
            b["falling"]=[(w,d) in fallday for d in b.day]
            P.append(b[["g","a","vol20","vol_ratio","r60","r20","r30","ma50","falling","w","coin"]])
    P=pd.concat(P)
    H=P[P.a>0].dropna(subset=["g"])
    out={}
    out["held_share_fall_vs_not"]=H.groupby("falling").agg(n=("g","size"),mean_g=("g","mean"),sd=("g","std"),alloc=("a","mean"),vol20=("vol20","median"),vr=("vol_ratio","median"),r60=("r60","median"),r20=("r20","median"),ma50=("ma50","median"))
    def q(col,k=5):
        x=H.dropna(subset=[col]).copy(); x["q"]=pd.qcut(x[col],k,duplicates="drop")
        r=x.groupby("q").agg(n=("g","size"),mean_g_bps=("g",lambda s:s.mean()*1e4),sd=("g","std"),alloc=("a","mean"),
                                  t=("g",lambda s:s.mean()/(s.std()/np.sqrt(len(s)))),p5=("g",lambda s:s.quantile(0.05)),share_fall=("falling","mean"))
        r["ratio"]=r.mean_g_bps/1e4/r.sd
        return r
    for col in ["vol20","vol_ratio","r60","r20","ma50"]:
        out["by_"+col]=q(col)
    out["alloc_dist"]=H.a.describe()
    return out
