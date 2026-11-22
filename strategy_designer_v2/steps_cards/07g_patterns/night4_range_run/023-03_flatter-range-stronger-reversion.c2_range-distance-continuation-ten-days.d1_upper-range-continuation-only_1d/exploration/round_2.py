def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    drow=[]; grid=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            lr=np.log(c).diff()
            vol=lr.rolling(30).std().shift(1)
            r1=c.pct_change()
            z=lr/vol
            ts=pd.to_datetime(b["timestamp"])
            n=len(b)
            for i in range(1,n-1):
                drow.append(dict(coin=coin,w=w,yr=ts[i].year,wd=ts[i].dayofweek,r=c[i+1]/c[i]-1,
                                 r3=(c[i+3]/c[i]-1) if i+3<n else np.nan,r1=r1[i],z=z[i]))
            hi=c.rolling(30).max(); lo=c.rolling(30).min()
            for i in range(0,n-10,10):
                grid.append(dict(coin=coin,fwd=c[i+10]/c[i]-1,athi=float(c[i]>=hi[i]-1e-12),
                                 pos=(c[i]-lo[i])/(hi[i]-lo[i]) if hi[i]>lo[i] else np.nan,yr=ts[i].year))
    d=pd.DataFrame(drow)
    d["dm"]=d["r"]-d.groupby("coin")["r"].transform("mean")
    def tt(s):
        s=s.dropna(); return pd.Series({"n":len(s),"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s)))})
    dz=d.dropna(subset=["z"]).copy()
    dz["zq"]=pd.cut(dz["z"],[-99,-3,-2,-1.5,-1,0,1,1.5,2,3,99])
    out["vol-scaled day move bucket -> next day excess"]=dz.groupby("zq",observed=True)["dm"].apply(tt).unstack().round(4)
    big=dz[dz["z"]<-1.5]
    out["after z<-1.5 drop: next-day excess by coin"]=big.groupby("coin")["dm"].apply(tt).unstack().round(4)
    out["after z<-1.5 drop: by year"]=big.groupby("yr")["dm"].apply(tt).unstack().round(4)
    sl=stats.linregress(dz.loc[dz.z<0,"z"],dz.loc[dz.z<0,"dm"])
    out["slope next-day excess on z, down days"]=pd.Series({"slope":sl.slope,"t":sl.slope/sl.stderr,"n":int((dz.z<0).sum())}).round(5)
    su=dz[dz.z>0]; sl2=stats.linregress(su["z"],su["dm"])
    out["slope next-day excess on z, up days"]=pd.Series({"slope":sl2.slope,"t":sl2.slope/sl2.stderr,"n":len(su)}).round(5)
    # 3-day non-overlap-ish: only big drops, spaced
    out["after z<-1.5: 3-day fwd excess"]=tt(big["r3"]-d.groupby("coin")["r3"].transform("mean").loc[big.index]).round(4)
    # weekday stability
    piv=d.groupby(["wd","coin"])["dm"].mean().unstack().round(4)
    out["weekday x coin next-day excess"]=piv
    out["weekday x year (Fri,Mon) excess"]=d[d.wd.isin([0,4])].groupby(["wd","yr"])["dm"].mean().unstack().round(4)
    # range top
    g=pd.DataFrame(grid); g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    out["at 30d high vs not, fwd10 excess"]=g.groupby("athi")["ex"].apply(tt).unstack().round(4)
    out["at 30d high by coin"]=g[g.athi==1].groupby("coin")["ex"].apply(tt).unstack().round(4)
    gp=g.dropna(subset=["pos"]).copy(); gp["pq"]=pd.cut(gp["pos"],[-0.01,0.1,0.3,0.5,0.7,0.9,0.999,1.0])
    out["range position bucket fwd10 excess"]=gp.groupby("pq",observed=True)["ex"].apply(tt).unstack().round(4)
    # book largest days
    br=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; br.append(x)
    B=pd.concat(br)
    bk=B.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    q=bk["book_return"].quantile([0.02,0.98])
    out["book top/bottom 2% days: mean book, mean coin"]=pd.DataFrame({
        "worst":bk[bk.book_return<=q.iloc[0]].mean(),"best":bk[bk.book_return>=q.iloc[1]].mean()}).round(4)
    out["share of book mean from best 2% days"]=float(bk.loc[bk.book_return>=q.iloc[1],"book_return"].sum()/bk["book_return"].sum())
    return out
