def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            vol=r1.rolling(20,min_periods=15).std()
            z=r1/vol
            ret30=c/c.shift(30)-1
            ret90=c/c.shift(90)-1
            f5=c.shift(-5)/c-1
            f1=c.shift(-1)/c-1
            f2=c.shift(-2)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":z,"ret30":ret30,"ret90":ret90,
                            "f5":f5,"f1":f1,"f2":f2,"wd":ts.dt.weekday,"yr":ts.dt.year})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["u1"]=D["f1"]-D.coin.map(D.groupby("coin")["f1"].mean())
    D["s1"]=D["u1"]/D.coin.map(D.groupby("coin")["f1"].std())
    g=D[D.pos%5==0].copy()
    g["u5"]=g["f5"]-g.coin.map(g.groupby("coin")["f5"].mean())
    g["s5"]=g["u5"]/g.coin.map(g.groupby("coin")["f5"].std())
    g2=D[D.pos%2==0].copy()
    g2["u2"]=g2["f2"]-g2.coin.map(g2.groupby("coin")["f2"].mean())
    g2["s2"]=g2["u2"]/g2.coin.map(g2.groupby("coin")["f2"].std())
    out={}
    def reg(df,x,y):
        s=df.dropna(subset=[x,y])
        if len(s)<20: return [np.nan,np.nan,len(s)]
        lr=stats.linregress(s[x],s[y]); return [lr.slope,lr.slope/lr.stderr,len(s)]
    # 1-day reversal after down days: graded on negative z only
    neg=D[D.z<0]
    res={}
    res["pooled"]=reg(neg,"z","s1")
    for c_,s in neg.groupby("coin"): res[c_]=reg(s,"z","s1")
    out["s1 on z (z<0) by coin"]=pd.DataFrame(res,index=["slope","t","n"]).T
    res={}
    for y,s in neg.groupby("yr"): res[y]=reg(s,"z","s1")
    out["s1 on z (z<0) by year"]=pd.DataFrame(res,index=["slope","t","n"]).T
    # same at 2 days
    neg2=g2[g2.z<0]; res={"pooled":reg(neg2,"z","s2")}
    for c_,s in neg2.groupby("coin"): res[c_]=reg(s,"z","s2")
    out["s2 on z (z<0) by coin"]=pd.DataFrame(res,index=["slope","t","n"]).T
    # momentum: 5-day after up days, graded, split by ret90 sign
    pos=g[g.z>0]; res={}
    for k,s in [("all",pos),("ret90>0",pos[pos.ret90>0]),("ret90<0",pos[pos.ret90<0])]: res[k]=reg(s,"z","s5")
    for c_,s in pos.groupby("coin"): res[c_]=reg(s,"z","s5")
    out["s5 on z (z>0)"]=pd.DataFrame(res,index=["slope","t","n"]).T
    res={}
    for y,s in pos.groupby("yr"): res[y]=reg(s,"z","s5")
    out["s5 on z (z>0) by year"]=pd.DataFrame(res,index=["slope","t","n"]).T
    # ret30 graded per coin and year
    res={"pooled":reg(g,"ret30","s5")}
    for c_,s in g.groupby("coin"): res[c_]=reg(s,"ret30","s5")
    for y,s in g.groupby("yr"): res[str(y)]=reg(s,"ret30","s5")
    out["s5 on ret30"]=pd.DataFrame(res,index=["slope","t","n"]).T
    # weekday consistency: Friday and Wednesday per coin
    wk=D.dropna(subset=["s1"])
    t=wk.groupby(["coin","wd"])["s1"].mean().unstack()
    out["s1 mean by coin x weekday"]=t
    t2=wk.groupby(["yr","wd"])["s1"].mean().unstack()
    out["s1 mean by year x weekday"]=t2
    return out
