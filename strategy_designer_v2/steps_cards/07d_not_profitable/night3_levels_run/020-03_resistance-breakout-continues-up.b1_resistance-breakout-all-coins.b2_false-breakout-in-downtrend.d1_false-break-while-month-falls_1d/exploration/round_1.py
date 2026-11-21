import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H=10
    rows=[]; base=[]; trd=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].values.astype(float); n=len(c)
            if n<40: continue
            piv=np.zeros(n,bool)
            for i in range(2,n-2):
                if c[i]==c[i-2:i+3].max(): piv[i]=True
            r30=np.full(n,np.nan); r30[30:]=c[30:]/c[:-30]-1
            r10p=np.full(n,np.nan); r10p[10:]=c[10:]/c[:-10]-1
            fwd=np.full(n,np.nan); fwd[:n-H]=c[H:]/c[:-H]-1
            for t in range(0,n-H,H): base.append((coin,fwd[t]))
            fc=b["forecast"].values
            for t in range(5,n-H):
                idx=[i for i in range(max(0,t-90),t-1) if piv[i] and i+2<=t-1]
                if len(idx)<1: continue
                lv=c[idx]
                below=lv[lv<c[t]]
                if len(below)==0: continue
                L=below.max()
                if not (c[t-1]<=L): continue
                cnt=int(((lv>=L*0.98)&(lv<=L*1.02)).sum())
                rows.append(dict(coin=coin,w=w,t=t,cell=t//H,cnt=cnt,r30=r30[t],r10p=r10p[t],
                                 brk=c[t]/L-1,fwd=fwd[t],short=fc[t]<0))
            tr=data["trades"][coin][w]
            if len(tr): trd.append(tr[["side","net_profit_loss_percent","profit_loss_percent"]])
    df=pd.DataFrame(rows).drop_duplicates(["coin","w","cell"])
    bs=pd.DataFrame(base,columns=["coin","fwd"]).dropna()
    drift=bs.groupby("coin").fwd.mean()
    df["ex"]=df.fwd-df.coin.map(drift)
    df=df.dropna(subset=["ex"])
    def g(s):
        x=s.dropna(); return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    out={}
    out["drift10_all"]=pd.Series(dict(mean=bs.fwd.mean(),sd=bs.fwd.std(),n=len(bs)))
    df["cntb"]=pd.cut(df.cnt,[0,1,2,3,5,100])
    df["r30s"]=np.where(df.r30<0,"neg","pos")
    out["ex_by_cnt_r30sign"]=df.groupby(["r30s","cntb"]).ex.apply(g).unstack()
    df["r30q"]=pd.qcut(df.r30,5)
    out["ex_by_r30q"]=df.groupby("r30q").ex.apply(g).unstack()
    out["ex_by_r30q_cnt3"]=df[df.cnt>=3].groupby("r30q").ex.apply(g).unstack()
    df["brkq"]=pd.qcut(df.brk,4)
    out["ex_by_breaksize"]=df.groupby("brkq").ex.apply(g).unstack()
    out["fwd_total_by_short_flag"]=df.groupby("short").fwd.apply(g).unstack()
    T=pd.concat(trd)
    out["trades"]=T.groupby("side").agg(n=("net_profit_loss_percent","size"),net=("net_profit_loss_percent","mean"),gross=("profit_loss_percent","mean"),win=("net_profit_loss_percent",lambda x:(x>0).mean()))
    return out
