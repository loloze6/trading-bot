def explore(data):
    import numpy as np, pandas as pd
    H=5
    grid=[]; ev=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); hi=b["high"].astype(float); lo=b["low"].astype(float)
            n=len(b)
            er=(c-c.shift(60)).abs()/c.diff().abs().rolling(60).sum()
            ph=hi.shift(1).rolling(60).max(); pl=lo.shift(1).rolling(60).min()
            mr=(hi-lo).rolling(60).mean()
            pos=(c-pl)/(ph-pl)
            dn=(pl-c)/mr
            r60=c/c.shift(60)-1
            fwd=c.shift(-H)/c-1
            day=pd.to_datetime(b["timestamp"]).dt.floor("D")
            for s in range(0,n,H):
                if s+H>=n: break
                grid.append(dict(coin=coin,w=w,fwd=fwd[s],pos=pos[s],er=er[s],day=day[s],r60=r60[s]))
                seg=[i for i in range(s,min(s+H,n-H)) if dn[i]>0]
                if seg:
                    i=seg[0]
                    ev.append(dict(coin=coin,w=w,mag=dn[i],er=er[i],fwd=fwd[i],day=day[i],r60=r60[i]))
    g=pd.DataFrame(grid); e=pd.DataFrame(ev)
    drift=g.groupby("coin")["fwd"].mean()
    g["un"]=g["fwd"]-g["coin"].map(drift); e["un"]=e["fwd"]-e["coin"].map(drift)
    def summ(x):
        x=x.dropna(subset=["un"])
        if len(x)<3: return pd.Series({"n":len(x),"mean":x["un"].mean() if len(x) else np.nan,"t":np.nan,"days":x["day"].nunique()})
        m=x["un"].mean(); dsum=(x["un"]-m).groupby(x["day"]).sum(); D=len(dsum)
        se=np.sqrt((dsum**2).sum()*D/(D-1))/len(x)
        return pd.Series({"n":len(x),"mean":m,"t":m/se,"days":D})
    out={}
    gg=g.dropna(subset=["pos","er"]).copy()
    gg["qpos"]=pd.qcut(gg["pos"],5,labels=False)
    gg["chop"]=gg["er"]<=0.3
    out["pos_x_chop"]=gg.groupby(["chop","qpos"]).apply(summ)
    out["pos_top_byyear"]=gg[gg.qpos==4].groupby(gg["day"].dt.year).apply(summ)
    out["pos_bottom_byyear"]=gg[gg.qpos<=1].groupby(gg["day"].dt.year).apply(summ)
    out["pos_top_bycoin"]=gg[gg.qpos==4].groupby("coin").apply(summ)
    x=gg.dropna(subset=["un"])
    out["corr_pos_un"]=float(np.corrcoef(x["pos"],x["un"])[0,1])
    e=e.dropna(subset=["er"])
    e["trend_down"]=(e["r60"]<0)
    e["erb"]=pd.cut(e["er"],[0,0.3,1.01])
    out["dn_er_r60"]=e.groupby(["erb","trend_down"]).apply(summ)
    out["dn_er_gt03_byyear"]=e[e.er>0.3].groupby(e["day"].dt.year).apply(summ)
    out["dn_er_gt03_bycoin"]=e[e.er>0.3].groupby("coin").apply(summ)
    return out
