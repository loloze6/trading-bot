def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"].astype(float)
            r1=c.shift(-1)/c-1; r2=c.shift(-2)/c-1; r3=c.shift(-3)/c-1
            r_own=c/c.shift(1)-1
            vol20=r_own.rolling(20).std()
            ret7=c/c.shift(7)-1
            d=pd.DataFrame({"coin":coin,"w":w,"wd":ts.dt.weekday,"yr":ts.dt.year,
                "f":b["forecast"].astype(float),"pos":b["postRebalance_current_allocation"].astype(float),
                "r1":r1,"r2":r2,"r3":r3,"rown":r_own,"z":r_own/vol20,"ret7":ret7,
                "vol":b["volume"].astype(float),"vmed":b["volume"].astype(float).rolling(20).median()})
            d["gain"]=d["pos"]*d["r1"]
            rows.append(d)
    D=pd.concat(rows)
    out={}
    out["gain_by_weekday"]=D.groupby("wd").agg(n=("gain","size"),mean_gain=("gain","mean"),mean_abs_pos=("pos",lambda x:x.abs().mean()),coin_r1=("r1","mean"))
    S=D[(D.wd==6)&(D.f!=0)].dropna(subset=["r1","r2","z"])
    S["side"]=np.where(S.f>0,"long","short")
    m1=D.groupby("coin")["r1"].mean()
    S["r1x"]=S.r1-S.coin.map(m1)
    out["sunday_by_side"]=S.groupby("side").agg(n=("r1","size"),r1=("r1","mean"),r1x=("r1x","mean"),r2=("r2","mean"),gain=("gain","mean"),abspos=("pos",lambda x:x.abs().mean()))
    S["zq"]=pd.qcut(S.z,5,labels=False)
    out["sunday_z_quintile"]=S.groupby("zq").agg(n=("r1","size"),z=("z","mean"),r1=("r1","mean"),r2=("r2","mean"),r3=("r3","mean"),gain=("gain","mean"))
    S["vq"]=pd.qcut((S.vol/S.vmed).rank(method="first"),3,labels=False)
    S["rev"]=-np.sign(S.z)*S.r1
    out["rev_by_relvol_tercile"]=S.groupby("vq").agg(n=("rev","size"),rev1=("rev","mean"))
    S["tq"]=pd.qcut(S.ret7.rank(method="first"),3,labels=False)
    out["rev_by_7d_trend_tercile_side"]=S.groupby(["tq","side"]).agg(n=("rev","size"),rev1=("rev","mean"),gain=("gain","mean"))
    out["by_year"]=S.groupby("yr").agg(n=("rev","size"),rev1=("rev","mean"),gain=("gain","mean"))
    out["by_coin"]=S.groupby("coin").agg(n=("rev","size"),rev1=("rev","mean"),t=("rev",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    fee=[];
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            fee.append(t[["profit_loss_percent","net_profit_loss_percent","total_commission"]])
    F=pd.concat(fee)
    out["trades"]=F.mean()
    dd=pd.concat([d.assign(coin=c,w=w) for c,ws in data["days"].items() for w,d in ws.items()])
    out["book_vs_hold_daily"]=pd.Series({"book_mean":dd.book_return.mean(),"coin_mean":dd.coin_return.mean(),"book_sd":dd.book_return.std(),"coin_sd":dd.coin_return.std()})
    return out
