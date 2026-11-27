import pandas as pd, numpy as np

def explore(data):
    H=7
    feats={}
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(b)
            fwd=np.full(n,np.nan); fwd[:n-H]=c[H:]/c[:n-H]-1
            r30=np.full(n,np.nan); r30[30:]=c[30:]/c[:-30]-1
            r60=np.full(n,np.nan); r60[60:]=c[60:]/c[:-60]-1
            dr=pd.Series(np.r_[np.nan,np.diff(np.log(c))])
            v30=dr.rolling(30).std()
            v90=dr.rolling(90,min_periods=60).std()
            ag=(v30/v90).values
            agp=v30.expanding(min_periods=30).apply(lambda x:(x<=x[-1]).mean(),raw=True).values
            ts=pd.to_datetime(b["timestamp"]).dt.normalize()
            f=pd.DataFrame(dict(ts=ts,r30=r30,r60=r60,ag=ag,agp=agp,fc=b["forecast"],reg=b["regime"],
                                alloc=b["postRebalance_current_allocation"],fwd=fwd))
            feats[(coin,w)]=f
            for i in range(0,n,H):
                rows.append(dict(coin=coin,w=w,**f.iloc[i].to_dict()))
    g=pd.DataFrame(rows).dropna(subset=["fwd"])
    g["drift"]=g.coin.map(g.groupby("coin")["fwd"].mean()); g["ex"]=g.fwd-g.drift
    g["s_tot"]=-g.fwd; g["s_ex"]=-g.ex
    def summ(d):
        out={}
        for col in ["s_tot","s_ex"]:
            x=d[col].dropna(); out[col+"_n"]=len(x); out[col+"_m"]=x.mean()
            out[col+"_t"]=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        return pd.Series(out)
    ch=g[g.reg=="unknown"].copy()
    ch["sig"]=ch.fc<=-2
    ch["hiag"]=ch.ag>1.0
    ch["hiagp"]=ch.agp>0.5
    out={}
    out["choppy grid: signal x agit(v30/v90>1)"]=ch.groupby(["sig","hiag"]).apply(summ)
    out["choppy grid: signal x agit percentile>0.5"]=ch.groupby(["sig","hiagp"]).apply(summ)
    out["choppy grid: signal x r60<0"]=ch.groupby(["sig",ch.r60<0]).apply(summ)
    # raw r30 graded in agitated vs calm
    ch["q30"]=pd.qcut(ch.r30,3,labels=["low","mid","high"])
    out["choppy grid: r30 tercile x agit"]=ch.groupby(["hiag","q30"]).apply(summ)
    # trades with entry features
    tr=[]
    for c,ws in data["trades"].items():
        for w,t in ws.items():
            f=feats[(c,w)]
            for _,r in t.iterrows():
                d=pd.to_datetime(r.entry_time).normalize()
                m=f[f.ts==d]
                if len(m)==0: continue
                m=m.iloc[0]
                tr.append(dict(gross=r.profit_loss_percent,net=r.net_profit_loss_percent,ag=m.ag,agp=m.agp,r30=m.r30,r60=m.r60,
                               dur=r.duration_minutes/1440))
    T=pd.DataFrame(tr)
    agg=lambda d: pd.Series(dict(n=len(d),gross=d.gross.mean(),net=d.net.mean(),t=d.gross.mean()/(d.gross.std()/np.sqrt(len(d))),dur=d.dur.mean()))
    out["trades by agit v30/v90>1"]=T.groupby(T.ag>1).apply(agg)
    out["trades by r60<0"]=T.groupby(T.r60<0).apply(agg)
    out["trades by raw r30 tercile"]=T.groupby(pd.qcut(T.r30,3)).apply(agg)
    out["trades by duration bucket"]=T.groupby(pd.cut(T.dur,[0,3,7,8,14,30,200])).apply(agg)
    out["trade gross quantiles"]=T.gross.describe()
    # book daily return on days in position, by agitation
    dd=[]
    for (c,w),f in feats.items():
        d=data["days"][c][w].copy()
        d["day"]=pd.to_datetime(d["day"]).dt.normalize()
        d=d.merge(f[["ts","ag","r60","alloc"]].rename(columns={"ts":"day"}),on="day",how="left")
        d["held"]=d.alloc.shift(1).fillna(0)!=0
        dd.append(d)
    D=pd.concat(dd)
    H_=D[D.held]
    out["book days held by agit"]=H_.groupby(H_.ag>1).book_return.agg(["count","mean","std"])
    out["book days held by r60<0"]=H_.groupby(H_.r60<0).book_return.agg(["count","mean","std"])
    return out
