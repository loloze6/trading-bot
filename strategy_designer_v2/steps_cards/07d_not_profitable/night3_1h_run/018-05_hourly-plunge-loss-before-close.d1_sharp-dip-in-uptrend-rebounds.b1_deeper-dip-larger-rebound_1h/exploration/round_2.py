def explore(data):
    import pandas as pd, numpy as np
    out={}
    coins=list(data["bars"].keys())
    P=[]; C=[]
    drift={}
    # normal drift per coin over 72 bars, non-overlapping
    for c in coins:
        rs=[]
        for w,b in data["bars"][c].items():
            cl=b.close.reset_index(drop=True).values
            idx=np.arange(0,len(cl)-72,72)
            rs+=list(cl[idx+72]/cl[idx]-1)
        drift[c]=np.mean(rs)
    for c in coins:
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True); cl=b.close
            r24=cl/cl.shift(24)-1
            r30=cl/cl.shift(720)-1; r7=cl/cl.shift(168)-1
            vol=cl.pct_change().rolling(168).std(); volL=cl.pct_change().rolling(1440,min_periods=500).std()
            hi=cl.rolling(720,min_periods=200).max(); dfh=cl/hi-1
            pos=b.postRebalance_current_allocation.fillna(0)
            g=pos*(cl.shift(-1)/cl-1)
            df=pd.DataFrame(dict(g=g,pos=pos,r30=r30,r7=r7,volr=vol/volL,dfh=dfh,r24=r24))
            df["coin"]=c; P.append(df[df.pos>0].dropna())
            # cases: forecast rise >=2 from min since last bet, first per grid cell
            f=b.forecast.fillna(0).values; n=len(f)
            lo=0; taken=set()
            for i in range(n):
                if f[i]<=0: lo=0; continue
                if f[i]-lo>=2:
                    cell=i//72
                    if cell not in taken and i+72<n:
                        taken.add(cell)
                        C.append(dict(coin=c,u=cl[i+72]/cl[i]-1-drift[c],r7=r7[i],r30=r30[i],volr=(vol/volL)[i],dfh=dfh[i],f=f[i]))
                    lo=f[i]
                else: lo=min(lo,f[i])
    P=pd.concat(P)
    for col in ["r7","r30","volr","dfh"]:
        q=pd.qcut(P[col],5,duplicates="drop")
        out["bookgain_by_"+col]=P.groupby(q).agg(bars=("g","size"),sum_gain=("g","sum"),mean_bps=("g",lambda x:x.mean()*1e4),mean_pos=("pos","mean"))
    C=pd.DataFrame(C).dropna()
    out["cases_n"]=len(C)
    for col in ["r7","r30","volr","dfh"]:
        q=pd.qcut(C[col],5,duplicates="drop")
        out["cases_by_"+col]=C.groupby(q).u.agg(["count","mean","std",lambda x:x.mean()/(x.std()/np.sqrt(len(x))),lambda x:(x<-0.1).mean()])
    # interaction r7 x r30 terciles
    C["r7t"]=pd.qcut(C.r7,3,labels=["lo","mid","hi"]); C["r30t"]=pd.qcut(C.r30,3,labels=["lo","mid","hi"])
    out["cases_r7_x_r30"]=C.groupby(["r30t","r7t"]).u.agg(["count","mean"])
    return out
