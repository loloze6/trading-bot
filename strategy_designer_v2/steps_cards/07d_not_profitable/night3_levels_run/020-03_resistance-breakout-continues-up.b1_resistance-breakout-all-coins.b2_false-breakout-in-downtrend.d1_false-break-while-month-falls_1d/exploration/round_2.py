import pandas as pd, numpy as np

def explore(data):
    H=10
    allr=[]; brk=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].values.astype(float); n=len(c)
            if n<40: continue
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            piv=np.zeros(n,bool)
            for i in range(2,n-2):
                if c[i]==c[i-2:i+3].max(): piv[i]=True
            r30=np.full(n,np.nan); r30[30:]=c[30:]/c[:-30]-1
            fwd=np.full(n,np.nan); fwd[:n-H]=c[H:]/c[:-H]-1
            for t in range(0,n-H,H):
                allr.append(dict(coin=coin,w=w,yr=yr[t],r30=r30[t],fwd=fwd[t]))
            seen=set()
            for t in range(5,n-H):
                idx=[i for i in range(max(0,t-90),t-2) if piv[i]]
                if not idx: continue
                lv=c[idx]; below=lv[lv<c[t]]
                if len(below)==0: continue
                L=below.max()
                if not (c[t-1]<=L): continue
                if t//H in seen: continue
                seen.add(t//H)
                cnt=int(((lv>=L*0.98)&(lv<=L*1.02)).sum())
                brk.append(dict(coin=coin,w=w,yr=yr[t],r30=r30[t],fwd=fwd[t],cnt=cnt))
    A=pd.DataFrame(allr).dropna(); B=pd.DataFrame(brk).dropna()
    drift=A.groupby("coin").fwd.mean()
    A["ex"]=A.fwd-A.coin.map(drift); B["ex"]=B.fwd-B.coin.map(drift)
    def g(s):
        x=s.dropna(); return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    edges=[-10,-0.25,-0.122,-0.05,0,0.09,0.25,100]
    A["q"]=pd.cut(A.r30,edges); B["q"]=pd.cut(B.r30,edges)
    out={}
    out["all_grid_ex_by_r30"]=A.groupby("q").ex.apply(g).unstack()
    out["breaks_ex_by_r30"]=B.groupby("q").ex.apply(g).unstack()
    Bd=B[B.r30<-0.122]; Ad=A[A.r30<-0.122]
    out["deep_breaks_by_year"]=Bd.groupby("yr").ex.apply(g).unstack()
    out["deep_all_by_year"]=Ad.groupby("yr").ex.apply(g).unstack()
    out["deep_breaks_by_cnt"]=Bd.assign(cb=pd.cut(Bd.cnt,[0,1,2,100])).groupby("cb").ex.apply(g).unstack()
    out["deep_breaks_by_coin_sign"]=pd.Series(dict(coins_neg=(Bd.groupby("coin").ex.mean()<0).sum(),coins=Bd.coin.nunique()))
    # graded within negative r30: correlation
    Bn=B[B.r30<0]; An=A[A.r30<0]
    out["corr_r30_ex_neg"]=pd.Series(dict(breaks=np.corrcoef(Bn.r30,Bn.ex)[0,1],allbars=np.corrcoef(An.r30,An.ex)[0,1],nb=len(Bn),na=len(An)))
    return out
