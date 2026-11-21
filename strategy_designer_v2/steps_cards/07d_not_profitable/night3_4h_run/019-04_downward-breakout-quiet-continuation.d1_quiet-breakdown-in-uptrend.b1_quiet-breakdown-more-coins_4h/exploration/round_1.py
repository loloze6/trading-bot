def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    H=18
    for coin, wins in data["bars"].items():
        # drift per coin over 18-bar grid
        fr=[]
        for w,b in wins.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-H,H)
            fr+=list(c[idx+H]/c[idx]-1)
        drift=np.mean(fr) if fr else 0; usual=np.std(fr) if fr else np.nan
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; h=b["high"]; l=b["low"]
            lo12=l.shift(1).rolling(12).min(); hi12=h.shift(1).rolling(12).max()
            span=(hi12-lo12)/c
            mbr=((h-l)/c).shift(1).rolling(180,min_periods=60).mean()
            narrow=span/mbr
            r30=c/c.shift(180)-1
            r3d=c/c.shift(18)-1
            n=len(b)
            for k in [6,18,36]:
                pass
            fwd={k:(c.shift(-k)/c-1) for k in [6,18,36]}
            dn=c<lo12; up=c>hi12
            depth=np.where(dn,(lo12-c)/c,np.where(up,(c-hi12)/c,np.nan))
            grid=np.arange(n)//H
            df=pd.DataFrame({"g":grid,"dn":dn,"up":up,"narrow":narrow,"r30":r30,"r3d":r3d,
                             "depth":depth,"f6":fwd[6],"f18":fwd[18],"f36":fwd[36]})
            for typ,col in [("dn","dn"),("up","up")]:
                s=df[df[col]].dropna(subset=["narrow","r30","f18"])
                s=s.groupby("g").head(1)
                s=s.assign(typ=typ,coin=coin,win=w,drift=drift,usual=usual)
                rows.append(s)
    A=pd.concat(rows)
    A["u18"]=A["f18"]-A["drift"]
    A["r30pos"]=A["r30"]>0
    A["nq"]=A.groupby("typ")["narrow"].transform(lambda x: pd.qcut(x,5,labels=False))
    A["rq"]=A.groupby("typ")["r30"].transform(lambda x: pd.qcut(x,5,labels=False))
    def agg(g):
        m=g["u18"].mean(); s=g["u18"].std(); n=len(g)
        return pd.Series({"n":n,"mean_u18":m,"t":m/(s/np.sqrt(n)),"mean_f6":g["f6"].mean(),"mean_f18":g["f18"].mean(),"mean_f36":g["f36"].mean(),"narrow_med":g["narrow"].median()})
    out={}
    out["by_type_r30sign"]=A.groupby(["typ","r30pos"]).apply(agg)
    out["by_type_narrowq"]=A.groupby(["typ","nq"]).apply(agg)
    out["by_type_r30q"]=A.groupby(["typ","rq"]).apply(agg)
    A["year"]=0
    out["dn_r30pos_by_coin"]=A[(A.typ=="dn")&A.r30pos].groupby("coin").apply(agg)
    out["corr_narrow_u18"]=A.groupby("typ").apply(lambda g: g[["narrow","u18"]].corr().iloc[0,1])
    out["corr_r3d_u18"]=A.groupby("typ").apply(lambda g: g[["r3d","u18"]].corr().iloc[0,1])
    A["r3q"]=A.groupby("typ")["r3d"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["by_type_r3dq"]=A.groupby(["typ","r3q"]).apply(agg)
    # book
    d=[]
    for coin,wins in data["days"].items():
        for w,t in wins.items():
            d.append(t.assign(coin=coin,win=w))
    D=pd.concat(d)
    D["year"]=pd.to_datetime(D["day"]).dt.year
    out["book_by_year"]=D.groupby("year").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("book_return","count"))
    tr=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            tr.append(t)
    T=pd.concat(tr)
    out["trades"]=pd.Series({"n":len(T),"pl_mean":T["profit_loss_percent"].mean(),"net_mean":T["net_profit_loss_percent"].mean(),"win_share":(T["net_profit_loss_percent"]>0).mean(),"dur_h_median":T["duration_minutes"].median()/60})
    return out
