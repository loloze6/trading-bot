import pandas as pd, numpy as np

def ct(df,col="u5"):
    s=df.groupby("day")[col].apply(lambda x:(x-df[col].mean()).sum())
    G=len(s); n=len(df)
    if G<3: return np.nan
    se=np.sqrt((s**2).sum()*G/(G-1))/n
    return df[col].mean()/se

def explore(data):
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            sma=cl.rolling(20).mean(); sd=r.rolling(20).std()
            n=len(b)
            rows.append(pd.DataFrame({"coin":c,"win":w,"pos":np.arange(n),
              "z":(cl-sma)/sma/sd,"tr60":cl/cl.shift(60)-1,
              "f5":cl.shift(-5)/cl-1,"choppy":(b["regime"]=="unknown").values,
              "day":pd.to_datetime(b["timestamp"]).dt.floor("D").astype(str),
              "yr":pd.to_datetime(b["timestamp"]).dt.year,"alloc":b["postRebalance_current_allocation"]}))
    D=pd.concat(rows)
    G=D[D["pos"]%5==0].dropna(subset=["f5","z"]).copy()
    G["u5"]=G["f5"]-G["coin"].map(G.groupby("coin")["f5"].mean())
    G["trend"]=np.where(G.choppy,"choppy",np.where(G.tr60.isna(),"nontrend_unknown",np.where(G.tr60>0.1,"rising",np.where(G.tr60<-0.1,"falling","choppy_by_tr"))))
    G["zb"]=pd.cut(G["z"],[-99,-2,-1,0,1,2,99])
    out={}
    res=[]
    for (t,zb),g in G.groupby(["trend","zb"],observed=True):
        res.append({"trend":t,"zb":str(zb),"n":len(g),"days":g.day.nunique(),"mean":g.u5.mean(),"t_day":ct(g)})
    out["u5 by trend and z bin"]=pd.DataFrame(res)
    res=[]
    for t,g in G.groupby("trend"):
        x=g.z.values; y=g.u5.values
        b=np.polyfit(x,y,1)[0]
        res.append({"trend":t,"n":len(g),"slope_per_z":b,"corr":np.corrcoef(x,y)[0,1]})
    out["slope u5 on z by trend"]=pd.DataFrame(res)
    # non choppy: by year, z>1 and z<-1
    for nm,m in [("nonchoppy z>1",(~G.choppy)&(G.z>1)),("nonchoppy z<-1",(~G.choppy)&(G.z<-1)),("choppy z<-1",G.choppy&(G.z<-1)),("choppy z>1",G.choppy&(G.z>1))]:
        g=G[m]; gg=g.groupby("yr")["u5"]
        out[nm+" by year"]=pd.DataFrame({"n":gg.size(),"mean":gg.mean()})
        out[nm+" all"]=f"n={len(g)} days={g.day.nunique()} mean={g.u5.mean():.4f} t_day={ct(g):.2f} total={g.f5.mean():.4f}"
    # falling: z<0 graded
    F=G[G.trend=="falling"]
    out["falling short-dir unusual z<0"]=f"n={(F.z<0).sum()} mean_short={-F[F.z<0].u5.mean():.4f} t={-ct(F[F.z<0]):.2f}"
    return out
