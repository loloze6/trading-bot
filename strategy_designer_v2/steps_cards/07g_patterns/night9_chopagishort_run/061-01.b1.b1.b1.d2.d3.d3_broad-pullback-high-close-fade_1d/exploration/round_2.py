def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float)
            rng=(h-l).replace(0,np.nan)
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b))})
            d["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D").values
            d["year"]=pd.to_datetime(b["timestamp"]).dt.year.values
            d["clv"]=(c-l)/rng
            d["r1"]=c.pct_change()
            d["mad"]=d["r1"].abs().rolling(20).mean()
            d["z1"]=d["r1"]/d["mad"]
            d["tr60"]=c/c.shift(60)-1
            d["vol30"]=d["r1"].rolling(30).std()
            rr=rng/c
            d["rngz"]=rr/rr.rolling(20).mean()
            d["rng5"]=rr.rolling(5).mean()/rr.rolling(30).mean()
            for k in (1,2,3,5):
                d[f"f{k}"]=c.shift(-k)/c-1
            d["alloc"]=b["postRebalance_current_allocation"].values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for k in (1,2,3,5):
        g=D[D.pos%k==0]
        dr=g.groupby("coin")[f"f{k}"].mean()
        D[f"x{k}"]=D[f"f{k}"]-D.coin.map(dr)
    D["volhi"]=D.groupby("coin")["vol30"].transform(lambda s: s>s.median())
    D["trend"]=np.where(D.tr60>0.10,"rising",np.where(D.tr60<-0.10,"falling",np.where(D.tr60.notna(),"choppy","na")))
    D["tv"]=D.trend+"_"+np.where(D.volhi,"agi","calm")
    def ct(df,k,by):
        g=df[(df.pos%k==0)].dropna(subset=[f"x{k}"])
        res={}
        for key,s in g.groupby(by):
            dsum=s.groupby("day")[f"x{k}"].sum()
            n=len(s); nd=len(dsum); m=s[f"x{k}"].mean()
            se=dsum.std()*np.sqrt(nd)/n if nd>2 else np.nan
            res[key]={"n":n,"days":nd,"mean":m,"t_day":m/se if se else np.nan}
        return pd.DataFrame(res).T
    out={}
    D["rzq"]=pd.qcut(D.rngz,5,labels=False)
    out["rangez q->x2 clustered"]=ct(D,2,"rzq")
    out["rangez q->x3 clustered"]=ct(D,3,"rzq")
    out["narrow(q0) by profile x2"]=ct(D[D.rzq==0],2,"tv")
    out["wide(q4) by profile x2"]=ct(D[D.rzq==4],2,"tv")
    out["narrow(q0) by year x2"]=ct(D[D.rzq==0],2,"year")
    D["r5q"]=pd.qcut(D.rng5,5,labels=False)
    out["5d range compress q->x3"]=ct(D,3,"r5q")
    D["z1q"]=pd.qcut(D.z1,7,labels=False)
    out["z1 sept->x1 clustered"]=ct(D,1,"z1q")
    out["small up(z1q3-4) by profile x1"]=ct(D[D.z1q.isin([3,4])],1,"tv")
    # grading inside narrow days: rngz continuous corr with x2
    g=D[(D.pos%2==0)].dropna(subset=["x2","rngz"])
    out["spearman rngz x2 all"]=float(g[["rngz","x2"]].corr("spearman").iloc[0,1])
    for tv,s in g.groupby("tv"):
        out[f"spearman rngz x2 {tv}"]=float(s[["rngz","x2"]].corr("spearman").iloc[0,1])
    # book's largest days
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            t=t.copy();t["coin"]=coin;dd.append(t)
    Dy=pd.concat(dd)
    bk=Dy.groupby("day")[["book_return","coin_return"]].mean().dropna()
    q=bk.book_return.quantile([0.02,0.98])
    out["book worst2% coin_ret"]=float(bk[bk.book_return<=q.iloc[0]].coin_return.mean())
    out["book best2% coin_ret"]=float(bk[bk.book_return>=q.iloc[1]].coin_return.mean())
    out["corr book coin daily"]=float(bk.corr().iloc[0,1])
    return out
