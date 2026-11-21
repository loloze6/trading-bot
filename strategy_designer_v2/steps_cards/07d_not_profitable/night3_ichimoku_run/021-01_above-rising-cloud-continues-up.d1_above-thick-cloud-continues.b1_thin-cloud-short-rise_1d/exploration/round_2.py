def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; out={}
    br=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True).copy()
            cl,h,l=b.close,b.high,b.low
            b["r1"]=cl.shift(-1)/cl-1
            b["r5"]=cl.shift(-5)/cl-1
            b["r10"]=cl.shift(-10)/cl-1
            b["coin"]=c;b["w"]=w;b["pos"]=np.arange(len(b))
            b["alloc"]=b.postRebalance_current_allocation
            tr=(b.regime=="trending").astype(int)
            b["tr"]=tr
            b["exit"]=(tr.shift(1)==1)&(tr==0)
            b["entry"]=(tr.shift(1)==0)&(tr==1)
            # bars since regime exit
            grp=(tr!=tr.shift()).cumsum()
            b["run"]=b.groupby(grp).cumcount()
            # price vs 26-bar midrange (kijun), short warmup
            kij=(h.rolling(26).max()+l.rolling(26).min())/2
            b["kdist"]=(cl-kij)/cl*100
            b["ret20"]=cl/cl.shift(20)-1
            br.append(b[["coin","w","pos","forecast","tr","alloc","r1","r5","r10","exit","entry","run","kdist","ret20"]])
    B=pd.concat(br,ignore_index=True)
    mu1=B.groupby("coin").r1.mean(); B["ex1"]=B.r1-B.coin.map(mu1)
    G=B[B.pos%5==0].copy()
    mu5=G.groupby("coin").r5.mean(); B["ex5"]=B.r5-B.coin.map(mu5)
    # gain by forecast bucket (per bar, contribution to mean)
    B["gain"]=B.alloc*B.r1
    B["fb"]=pd.cut(B.forecast,[-0.001,0.001,5,10,15,21])
    out["gain_by_fb"]=B.groupby("fb").agg(n=("r1","size"),ex1=("ex1","mean"),r1=("r1","mean"),alloc=("alloc","mean"),gain_sum_share=("gain","sum"))
    # after regime exit and after entry
    def summ(m):
        x=B.loc[m]
        return pd.Series({"n":len(x),"ex5":x.ex5.mean(),"t5":stats.ttest_1samp(x.ex5.dropna(),0).statistic,"r10":x.r10.mean()})
    out["after_exit_entry"]=pd.DataFrame({"exit":summ(B.exit),"entry":summ(B.entry)}).T
    # out of regime: run length since exit buckets, excess 1d
    O=B[B.tr==0].copy()
    O["rb"]=pd.cut(O.run,[-1,4,9,19,49,1000])
    out["out_by_run"]=O.groupby("rb").agg(n=("ex1","size"),ex1=("ex1","mean"),r1=("r1","mean"))
    # out of regime: graded by distance to 26-day midrange, grid
    Og=O[O.pos%5==0].dropna(subset=["ex5","kdist"]).copy()
    Og["kq"]=pd.qcut(Og.kdist,5,labels=False)
    out["out_by_kijun_q"]=Og.groupby("kq").agg(n=("ex5","size"),kd=("kdist","mean"),ex5=("ex5","mean"),r5=("r5","mean"))
    Ig=B[(B.tr==1)&(B.pos%5==0)].dropna(subset=["ex5","kdist"]).copy()
    Ig["kq"]=pd.qcut(Ig.kdist,4,labels=False)
    out["in_by_kijun_q"]=Ig.groupby("kq").agg(n=("ex5","size"),kd=("kdist","mean"),ex5=("ex5","mean"),fc=("forecast","mean"))
    Ig["fq"]=pd.qcut(Ig.forecast.rank(method="first"),4,labels=False)
    out["in_by_fc_q"]=Ig.groupby("fq").agg(n=("ex5","size"),fc=("forecast","mean"),ex5=("ex5","mean"),r10=("r10","mean"),alloc=("alloc","mean"))
    # in-regime 10-day vs 5-day
    out["in_horizon"]=pd.Series({"ex5_in":Ig.ex5.mean(),"r5_in":Ig.r5.mean() if "r5" in Ig else np.nan,"r10_in":Ig.r10.mean(),
                                 "corr_fc_ret20":Ig[["forecast","ret20"]].corr().iloc[0,1]})
    return out
