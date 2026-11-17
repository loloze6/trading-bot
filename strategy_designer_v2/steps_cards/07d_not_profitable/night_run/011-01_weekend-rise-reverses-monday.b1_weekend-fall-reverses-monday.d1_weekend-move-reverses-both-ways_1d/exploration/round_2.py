def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"].astype(float)
            ro=c/c.shift(1)-1
            d=pd.DataFrame({"coin":coin,"w":w,"wd":ts.dt.weekday,"yr":ts.dt.year,
                "f":b["forecast"].astype(float),"pos":b["postRebalance_current_allocation"].astype(float),
                "r1":c.shift(-1)/c-1,"r3":c.shift(-3)/c-1,"z":ro/ro.rolling(20).std(),
                "ret30":c/c.shift(30)-1,"vol20":ro.rolling(20).std()})
            d["gain"]=d.pos*d.r1
            rows.append(d)
    D=pd.concat(rows)
    m1=D.groupby("coin").r1.mean(); m3=D.groupby("coin").r3.mean()
    S=D[(D.wd==6)&(D.f!=0)].dropna(subset=["r1","r3","z","ret30"]).copy()
    S["rev1"]=-np.sign(S.z)*(S.r1-S.coin.map(m1))
    S["rev3"]=-np.sign(S.z)*(S.r3-S.coin.map(m3))
    S["zq"]=pd.qcut(S.z,5,labels=False)
    out={}
    out["zq_detail"]=S.groupby("zq").agg(n=("z","size"),abspos=("pos",lambda x:x.abs().mean()),absf=("f",lambda x:x.abs().mean()),rev1=("rev1","mean"),rev3=("rev3","mean"),gain=("gain","mean"))
    S["absz_q"]=pd.qcut(S.z.abs(),4,labels=False)
    S["tr"]=np.where(S.ret30>0,"up30","down30")
    S["dirn"]=np.where(S.z>0,"rise","fall")
    g=S.groupby(["tr","dirn"])
    out["trend30_dir"]=g.agg(n=("z","size"),rev1=("rev1","mean"),rev3=("rev3","mean"),gain=("gain","mean"),t1=("rev1",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    out["absz_q_by_trend"]=S.groupby(["tr","absz_q"]).agg(n=("z","size"),rev1=("rev1","mean"),rev3=("rev3","mean"))
    S["vq"]=pd.qcut(S.vol20,3,labels=False)
    out["vol_tercile"]=S.groupby("vq").agg(n=("z","size"),rev1=("rev1","mean"),rev3=("rev3","mean"),gain=("gain","mean"))
    dd=pd.concat([d.assign(coin=c,w=w) for c,ws in data["days"].items() for w,d in ws.items()])
    dd["yr"]=pd.to_datetime(dd["day"]).dt.year
    out["book_by_year"]=dd.groupby("yr").agg(book=("book_return","mean"),hold=("coin_return","mean"))
    worst=dd.nsmallest(60,"book_return")
    out["worst60_book_days_coinret"]=pd.Series({"mean_book":worst.book_return.mean(),"mean_coin":worst.coin_return.mean(),"share_coin_up":(worst.coin_return>0).mean()})
    return out
