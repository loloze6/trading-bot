import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            z=r/sd
            nxt=c.shift(-1)/c-1
            nxt2=c.shift(-2)/c-1
            ret60=c/c.shift(60)-1
            d=pd.DataFrame({"coin":coin,"w":w,"year":pd.to_datetime(b["timestamp"]).dt.year,
                            "r":r,"z":z,"nxt":nxt,"nxt2":nxt2,"ret60":ret60,
                            "agit":(b["regime"]!="chop"),"fc":b["forecast"].astype(float),
                            "day":pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["r"].mean()
    D["ex"]=D["nxt"]-D["coin"].map(mu)
    D=D.dropna(subset=["z","ex"])
    def st(g):
        dd=g.groupby("day")["ex"].mean()
        return pd.Series({"n":len(g),"days":len(dd),"mean_ex%":g["ex"].mean()*100,
                          "t_day":dd.mean()/(dd.std()/np.sqrt(len(dd))) if len(dd)>2 else np.nan})
    D["zb"]=pd.cut(D["z"],[-99,-2,-1,-0.5,0,0.5,1,2,99])
    out={}
    out["agit_by_z"]=D[D.agit].groupby("zb",observed=True).apply(st)
    out["calm_by_z"]=D[~D.agit].groupby("zb",observed=True).apply(st)
    A=D[D.agit&(D.z>0)]
    out["agit_up_by_coin"]=A.groupby("coin").apply(st)
    out["agit_up_by_window"]=A.groupby("w").apply(st)
    A2=A.copy(); A2["tr"]=np.where(A2.ret60>0.1,"rising",np.where(A2.ret60<-0.1,"falling",np.where(A2.ret60.notna(),"choppy","na")))
    out["agit_up_by_trend"]=A2.groupby("tr").apply(st)
    out["agit_up_z>1_by_trend"]=A2[A2.z>1].groupby("tr").apply(st)
    # correlations
    out["corr_agit_up_z_ex"]=float(np.corrcoef(A.z,A.ex)[0,1])
    Dn=D[D.agit&(D.z<0)]
    out["corr_agit_down_z_ex"]=float(np.corrcoef(Dn.z,Dn.ex)[0,1])
    # two-day horizon for agit up
    A3=A.dropna(subset=["nxt2"]).copy(); A3["ex2"]=A3.nxt2-2*A3.coin.map(mu)
    out["agit_up_2day_by_z"]=A3.groupby(pd.cut(A3.z,[0,0.5,1,2,99]),observed=True)["ex2"].agg(["count","mean"])
    out["fc_pos_share_agit_up"]=float((A.fc>0).mean())
    return out
