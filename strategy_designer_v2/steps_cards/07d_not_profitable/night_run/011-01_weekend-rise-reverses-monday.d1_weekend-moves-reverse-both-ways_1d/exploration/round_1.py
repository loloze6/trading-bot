def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"])
            c=b["close"].values
            r1=pd.Series(c).pct_change()
            vol20=r1.rolling(20).std()
            ret20=pd.Series(c)/pd.Series(c).shift(20)-1
            v=b["volume"]; vrel=v/v.rolling(20).mean()
            n=len(b)
            for i in range(n):
                if ts.iloc[i].dayofweek!=6: continue
                d={"coin":coin,"w":w,"f":b["forecast"].iloc[i],"pos":b["postRebalance_current_allocation"].iloc[i],
                   "prev":b["previous_allocation"].iloc[i],"wk":r1.iloc[i],"z":r1.iloc[i]/vol20.iloc[i] if vol20.iloc[i]>0 else np.nan,
                   "ret20":ret20.iloc[i],"vrel":vrel.iloc[i]}
                for h in (1,2,3,5):
                    d[f"r{h}"]=c[i+h]/c[i]-1 if i+h<n else np.nan
                d["r_tue"]=c[i+2]/c[i+1]-1 if i+2<n else np.nan
                d["fee"]=(b["postRebalance_total_value"].iloc[i]/b["total_portfolio_value"].iloc[i]-1)
                rows.append(d)
    df=pd.DataFrame(rows)
    df["s"]=-np.sign(df["wk"])
    out={}
    def g(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    tab={}
    for k in ["r1","r_tue","r2","r3","r5"]:
        tab[k]=g(df["s"]*df[k])
    out["fade sign x fwd ret (Sunday)"]=pd.DataFrame(tab).T
    df["az"]=df["z"].abs()
    df["zq"]=pd.qcut(df["az"],4,labels=["q1","q2","q3","q4"])
    out["by |z| quartile: fade x r1, r2"]=df.groupby("zq").apply(lambda x: pd.Series({"n":len(x),"fade_r1":(x.s*x.r1).mean(),"fade_r2":(x.s*x.r2).mean(),"t_r2":(x.s*x.r2).mean()/(x.s*x.r2).std()*np.sqrt(x.r2.notna().sum())}))
    df["side"]=np.where(df["wk"]>0,"rise->short","fall->long")
    out["by side"]=df.groupby("side").apply(lambda x: pd.Series({"n":len(x),"fade_r1":(x.s*x.r1).mean(),"fade_r2":(x.s*x.r2).mean(),"raw_r2":x.r2.mean(),"mean_abs_pos":x.pos.abs().mean()}))
    df["trend"]=np.where(df["ret20"]>0,"up20","down20")
    out["by 20d trend x side fade_r2"]=df.groupby(["trend","side"]).apply(lambda x: pd.Series({"n":len(x),"fade_r2":(x.s*x.r2).mean(),"t":(x.s*x.r2).mean()/(x.s*x.r2).std()*np.sqrt(x.r2.notna().sum())}))
    df["vq"]=pd.qcut(df["vrel"],3,labels=["lowvol","mid","high"])
    out["by Sunday rel volume fade_r2"]=df.groupby("vq").apply(lambda x: pd.Series({"n":len(x),"fade_r2":(x.s*x.r2).mean(),"t":(x.s*x.r2).mean()/(x.s*x.r2).std()*np.sqrt(x.r2.notna().sum())}))
    out["by coin fade_r1 fade_r2"]=df.groupby("coin").apply(lambda x: pd.Series({"fade_r1":(x.s*x.r1).mean(),"fade_r2":(x.s*x.r2).mean()}))
    out["fees & pos"]=pd.Series({"mean_fee_per_sunday":df.fee.mean(),"mean_abs_pos":df.pos.abs().mean(),"mean_pos_x_r1":(df.pos*df.r1).mean()})
    # book daily
    bd=[];hd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            bd.append(d[["day","book_return","coin_return"]].assign(w=w))
    D=pd.concat(bd)
    agg=D.groupby(["w","day"])[["book_return","coin_return"]].mean()
    agg["dow"]=pd.to_datetime(agg.index.get_level_values("day")).dayofweek
    out["book by dow"]=agg.groupby("dow")[["book_return","coin_return"]].agg(["mean","std","count"])
    return out
