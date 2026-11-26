import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]; daily=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            r1=c.pct_change()
            r7=c/c.shift(7)-1
            mabs=r7.abs().rolling(30).mean()
            sc=r7/mabs
            hh=h.rolling(7).max(); ll=l.rolling(7).min()
            pos=(c-ll)/(hh-ll)
            r30=c/c.shift(30)-1
            r1d=r1
            vol30=r1.rolling(30).std()
            volrel=vol30/r1.rolling(90).std()
            fwd=c.shift(-7)/c-1
            fwd3=c.shift(-3)/c-1
            inprof=(b["regime"]!="chop").astype(int)
            wd=pd.to_datetime(b["timestamp"]).dt.weekday
            df=pd.DataFrame(dict(coin=coin,win=w,sc=sc,pos=pos,r30=r30,r1=r1d,fwd=fwd,fwd3=fwd3,
                                 inprof=inprof,volrel=volrel,wd=wd,alloc=b["postRebalance_current_allocation"]))
            df["grid"]=(np.arange(len(df))%7==0)
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    G=A[A.grid & A.fwd.notna()].copy()
    drift=G.groupby("coin").fwd.transform("mean")
    G["ex"]=G.fwd-drift
    def summ(g):
        n=len(g); m=g.ex.mean(); s=g.ex.std()
        return pd.Series(dict(n=n,mean_ex=m,t=m/(s/np.sqrt(n)) if n>2 else np.nan,mean_tot=g.fwd.mean()))
    out={}
    out["inprof_vs_out"]=G.groupby("inprof").apply(summ)
    Gs=G[G.sc.notna()].copy()
    Gs["scq"]=pd.qcut(Gs.sc,5,labels=False)
    out["scaled7_quint_by_prof"]=Gs.groupby(["inprof","scq"]).apply(summ)
    Gp=G[G.pos.notna()].copy(); Gp["posq"]=pd.cut(Gp.pos,[-.01,.2,.4,.6,.8,1.01],labels=False)
    out["weekpos_by_prof"]=Gp.groupby(["inprof","posq"]).apply(summ)
    Gr=G[G.r30.notna()].copy(); Gr["r30q"]=pd.qcut(Gr.r30,5,labels=False)
    out["r30_quint_by_prof"]=Gr.groupby(["inprof","r30q"]).apply(summ)
    Gv=G[G.volrel.notna()].copy(); Gv["vq"]=pd.qcut(Gv.volrel,4,labels=False)
    out["volrel_quart"]=Gv.groupby("vq").apply(summ)
    Gq=G[G.r1.notna()].copy(); Gq["r1q"]=pd.qcut(Gq.r1,5,labels=False)
    out["r1_quint"]=Gq.groupby("r1q").apply(summ)
    out["weekday"]=G.groupby("wd").apply(summ)
    # daily 1-day forward by weekday all bars
    A["f1"]=A.groupby(["coin","win"]).r1.shift(-1)
    out["next_day_by_weekday_allbars"]=A.groupby("wd").f1.agg(["count","mean",lambda x:x.mean()/x.std()*np.sqrt(x.count())])
    # book
    D=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; d["win"]=w; D.append(d)
    D=pd.concat(D)
    bk=D.groupby(["win","day"]).book_return.mean().dropna()
    out["book_by_window"]=bk.groupby(level=0).agg(["count","mean","std","sum"])
    trd=pd.concat([t.assign(coin=c,win=w) for c,ws in data["trades"].items() for w,t in ws.items() if len(t)])
    out["trades_by_coin"]=trd.groupby("coin").net_profit_loss_percent.agg(["count","mean","sum"])
    out["trades_by_window"]=trd.groupby("win").net_profit_loss_percent.agg(["count","mean","sum"])
    return out
