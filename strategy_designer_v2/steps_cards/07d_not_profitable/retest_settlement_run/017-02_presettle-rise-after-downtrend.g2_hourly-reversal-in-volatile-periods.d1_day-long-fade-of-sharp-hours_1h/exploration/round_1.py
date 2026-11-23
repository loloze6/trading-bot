def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    H=[6,24,48,72]
    for coin,ws in data["bars"].items():
        drift={}
        for h in H:
            allr=[]
            for w,b in ws.items():
                c=b["close"].values
                idx=np.arange(0,len(c)-h,h)
                allr.append(c[idx+h]/c[idx]-1)
            drift[h]=np.concatenate(allr).mean()
        for w,b in ws.items():
            c=b["close"].reset_index(drop=True)
            r1=c.pct_change()
            s24=r1.rolling(24).std()
            vr=s24/s24.rolling(720,min_periods=240).mean()
            z=r1/s24
            f=b["forecast"].reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            n=len(c)
            for h in H:
                idx=np.arange(0,n-h,h)
                fr=c.values[idx+h]/c.values[idx]-1
                d=pd.DataFrame({"coin":coin,"w":w,"h":h,"f":f.values[idx],"z":z.values[idx],"vr":vr.values[idx],
                                "year":ts.dt.year.values[idx],
                                "tot":np.sign(f.values[idx])*fr,"exc":np.sign(f.values[idx])*(fr-drift[h])})
                rows.append(d)
    D=pd.concat(rows); D=D[D.f!=0]
    def agg(g):
        return pd.Series({"n":len(g),"mean_exc%":g.exc.mean()*100,"mean_tot%":g.tot.mean()*100,
                          "t":g.exc.mean()/(g.exc.std()/np.sqrt(len(g)))})
    out={}
    out["by_horizon"]=D.groupby("h").apply(agg)
    D24=D[D.h==24].copy()
    D24["absf_dec"]=pd.qcut(D24.f.abs(),10,labels=False,duplicates="drop")
    out["h24_by_absf_decile"]=D24.groupby("absf_dec").apply(agg)
    D72=D[D.h==72].copy(); D72["absf_q"]=pd.qcut(D72.f.abs(),5,labels=False,duplicates="drop")
    out["h72_by_absf_quint"]=D72.groupby("absf_q").apply(agg)
    D24["side"]=np.where(D24.f>0,"long","short")
    out["h24_side"]=D24.groupby("side").apply(agg)
    D24b=D24.dropna(subset=["z","vr"]).copy()
    D24b["zq"]=pd.qcut(D24b.z.abs(),3,labels=["zlo","zmid","zhi"])
    D24b["vrq"]=pd.qcut(D24b.vr,3,labels=["vlo","vmid","vhi"])
    out["h24_z_x_vr"]=D24b.groupby(["zq","vrq"]).apply(agg)
    out["h24_by_year"]=D24.groupby("year").apply(agg)
    top=D24[D24.absf_dec>=D24.absf_dec.max()-1]
    out["h24_top20_side"]=top.groupby("side").apply(agg)
    T=pd.concat([t2 for c,ws in data["trades"].items() for w,t2 in ws.items()])
    out["trades"]=T.groupby("side").agg(n=("side","size"),gross=("profit_loss_percent","mean"),
        net=("net_profit_loss_percent","mean"),dur_h=("duration_minutes",lambda x:x.mean()/60))
    tv=[];al=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            tv.append((b["postRebalance_current_allocation"]-b["previous_allocation"]).abs().sum()/len(b)*24)
            al.append(b["postRebalance_current_allocation"].abs().mean())
    out["turnover_per_day_mean"]=float(np.mean(tv)); out["mean_abs_alloc"]=float(np.mean(al))
    return out
