def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); a=b["postRebalance_current_allocation"].astype(float)
            raw=b["debug_info.components.below_ma.last_history_value"].astype(float)
            sma=c/(1+raw/100.0) if raw.abs().median()>1 else c/(1+raw)
            slope=sma/sma.shift(20)-1
            r10=c.shift(-10)/c-1; r1=c.shift(-1)/c-1
            lr=np.log(c).diff(); vol=lr.rolling(30).std()
            dd=c/c.rolling(60,min_periods=20).max()-1
            mom5=c/c.shift(5)-1
            rows.append(pd.DataFrame({"coin":coin,"w":w,"a":a,"f":b["forecast"].astype(float),"raw":raw,
                "slope":slope,"r10":r10,"r1":r1,"vol":vol,"dd":dd,"mom5":mom5}))
    d=pd.concat(rows,ignore_index=True).dropna(subset=["r10"])
    cm=d.groupby("coin")["r1"].transform("mean")
    d["ex10"]=d["r10"]-10*cm
    out={}
    out["raw_scale"]=d["raw"].describe()
    act=d[d.a!=0].copy()
    act["rawq"]=pd.qcut(act["raw"].rank(method="first"),5,labels=["deepest","q2","q3","q4","shallow"])
    def agg(g):
        return g.agg(n=("ex10","size"),raw=("raw","mean"),ex10=("ex10","mean"),
            t=("ex10",lambda x:x.mean()/x.std()*np.sqrt(len(x)/10)),up=("ex10",lambda x:(x>0).mean()))
    out["by_raw_q"]=agg(act.groupby("rawq"))
    act["slopes"]=np.where(act.slope<0,"sma_falling","sma_rising")
    out["by_slope"]=agg(act.groupby("slopes"))
    act["ddq"]=pd.cut(act["dd"],[-1,-0.5,-0.3,-0.15,0.01],labels=["dd>50","dd30-50","dd15-30","dd<15"])
    out["by_drawdown"]=agg(act.groupby("ddq"))
    act["m5"]=np.where(act.mom5<0,"fell5d","rose5d")
    out["slope_x_m5"]=agg(act.groupby(["slopes","m5"]))
    act["volq"]=act.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=False))
    out["slope_x_vol"]=agg(act.groupby(["slopes","volq"]))
    ab=d[d.a==0].copy()
    ab["slopes"]=np.where(ab.slope<0,"sma_falling","sma_rising")
    out["above_sma_by_slope"]=agg(ab.groupby("slopes"))
    return out
