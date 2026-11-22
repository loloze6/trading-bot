def explore(data):
    import numpy as np, pandas as pd
    out={}
    H=18
    allr=[]
    for c, ws in data["bars"].items():
        for w,b in ws.items():
            cl=b["close"].values; idx=np.arange(0,len(cl)-H,H)
            allr.append(pd.DataFrame({"c":c,"r":cl[idx+H]/cl[idx]-1}))
    allr=pd.concat(allr); drift=allr.groupby("c")["r"].mean(); usual=allr.groupby("c")["r"].std()
    recs=[]; share=[]
    for c, ws in data["bars"].items():
        for w,b in ws.items():
            cl=b["close"].values; f=b["forecast"].fillna(0).values; vol=b["volume"].values
            al=b["postRebalance_current_allocation"].fillna(0).values
            share.append({"in_long":(al>0.05).mean(),"f_pos":(f>0).mean()})
            r=np.r_[np.nan, cl[1:]/cl[:-1]-1]
            vr=(pd.Series(vol).rolling(3).mean()/pd.Series(vol).rolling(180).mean()).values
            vr1=(pd.Series(vol)/pd.Series(vol).rolling(180).mean()).values
            p30=pd.Series(cl).pct_change(180).values
            nb=len(cl); taken=set(); lowsince=0.0
            for k in range(nb):
                lowsince=min(lowsince,f[k])
                if f[k]-lowsince>=2 and k+H<nb:
                    cell=k//H
                    if cell not in taken:
                        taken.add(cell); ret=cl[k+H]/cl[k]-1
                        path=cl[k:k+H+1]/cl[k]-1
                        recs.append({"c":c,"w":w,"ret":ret,"unus":ret-drift[c],"str":(ret-drift[c])/usual[c],
                                     "vr":vr[k],"vr1":vr1[k],"p30":p30[k],"minpath":path.min()})
                    lowsince=f[k]
    cs=pd.DataFrame(recs).dropna()
    out["time_in_market"]=pd.DataFrame(share).mean()
    cs["vq"]=pd.qcut(cs.vr,4,labels=False)
    cs["pq"]=np.where(cs.p30<0,"down30","up30")
    def tt(x): return x.mean()/x.std()*np.sqrt(len(x))
    g=cs.groupby(["pq","vq"]).agg(n=("unus","size"),unusual=("unus","mean"),total=("ret","mean"),strength=("str","mean"),worst_path_mean=("minpath","mean"))
    g["t"]=cs.groupby(["pq","vq"])["unus"].apply(tt)
    out["by_trend_and_vol"]=g
    cs["v1q"]=pd.qcut(cs.vr1,4,labels=False)
    g2=cs.groupby("v1q").agg(n=("unus","size"),unusual=("unus","mean"),strength=("str","mean"),p10=("ret",lambda x:x.quantile(.1)),minpath=("minpath","mean"))
    g2["t"]=cs.groupby("v1q")["unus"].apply(tt)
    out["by_signal_bar_volume"]=g2
    dd_w=["w1","w2","w3","w12","w13","w14","w6","w7","w21","w22","w24"]
    cs["in_dd"]=cs.w.isin(dd_w)
    g3=cs.groupby(["in_dd","vq"]).agg(n=("unus","size"),unusual=("unus","mean"),total=("ret","mean"))
    g3["t"]=cs.groupby(["in_dd","vq"])["unus"].apply(tt)
    out["drawdown_windows_by_vol"]=g3
    # chained per-case total returns by vol quartile, sum per window, worst window
    pw=cs.groupby(["vq","w"])["ret"].mean().unstack(0)
    out["worst_window_mean_ret_by_vq"]=pw.min()
    out["share_windows_positive_by_vq"]=(pw>0).mean()
    cs["coin_year"]=cs.c
    out["vq_top_minus_bottom_by_coin"]=cs.groupby("c").apply(lambda d:d[d.vq==3].unus.mean()-d[d.vq==0].unus.mean())
    return out
