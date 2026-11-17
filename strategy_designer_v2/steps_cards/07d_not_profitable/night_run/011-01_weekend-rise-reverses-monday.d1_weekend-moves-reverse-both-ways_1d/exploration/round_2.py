def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]); c=b["close"].values
            r1=pd.Series(c).pct_change(); vol20=r1.rolling(20).std()
            ret20=pd.Series(c)/pd.Series(c).shift(20)-1
            n=len(b)
            for i in range(n):
                if i+3>=n or np.isnan(vol20.iloc[i]) or vol20.iloc[i]<=0: continue
                rows.append({"coin":coin,"w":w,"dow":ts.iloc[i].dayofweek,"z":r1.iloc[i]/vol20.iloc[i],
                             "r1":c[i+1]/c[i]-1,"r2":c[i+2]/c[i]-1,"r3":c[i+3]/c[i]-1,"ret20":ret20.iloc[i],
                             "pos":b["postRebalance_current_allocation"].iloc[i]})
    df=pd.DataFrame(rows); df["s"]=-np.sign(df["z"])
    out={}
    def tt(x):
        x=x.dropna(); return x.mean()/x.std()*np.sqrt(len(x))
    # weekday comparison: fade of 1-day move by day of week, r2 on grid of every 7th (dow-specific, nonoverlapping)
    out["fade r2 by dow of move"]=df.groupby("dow").apply(lambda x: pd.Series({"n":len(x),"fade_r1":(x.s*x.r1).mean(),"fade_r2":(x.s*x.r2).mean(),"t_r2":tt(x.s*x.r2)}))
    su=df[df.dow==6].copy(); su["az"]=su.z.abs()
    su["zq"]=pd.qcut(su.az,4,labels=["q1","q2","q3","q4"])
    su["side"]=np.where(su.z>0,"rise","fall")
    out["sunday |z| q x side fade_r2"]=su.groupby(["zq","side"]).apply(lambda x: pd.Series({"n":len(x),"fade_r2":(x.s*x.r2).mean(),"t":tt(x.s*x.r2)}))
    out["sunday |z| q x trend fade_r2"]=su.groupby(["zq",np.where(su.ret20>0,"up20","down20")]).apply(lambda x: pd.Series({"n":len(x),"fade_r2":(x.s*x.r2).mean(),"fade_r3":(x.s*x.r3).mean()}))
    out["sunday mean |z| per q"]=su.groupby("zq").az.agg(["min","mean","max"])
    # book falls
    bd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items(): bd.append(d[["day","book_return","coin_return"]].assign(w=w))
    D=pd.concat(bd); agg=D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    agg=agg.dropna()
    eq=(1+agg.book_return).cumprod(); dd=eq/eq.cummax()-1
    out["book summary"]=pd.Series({"days":len(agg),"mean":agg.book_return.mean(),"active_share":(agg.book_return.abs()>1e-6).mean(),
        "mean_on_active":agg.book_return[agg.book_return.abs()>1e-6].mean(),"maxdd":dd.min(),
        "yearly":eq.iloc[-1]**(365/len(agg))-1,"worst5_mean":agg.book_return.nsmallest(5).mean(),"best5_mean":agg.book_return.nlargest(5).mean()})
    agg["ddbin"]=dd.values
    out["dd by window (min)"]=agg.groupby("w").ddbin.min().sort_values().head(6)
    return out
