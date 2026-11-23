def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=10
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            lvr=np.log(v/v.shift(1).rolling(20).mean())
            r1=c/c.shift(1)-1
            vol20=r1.rolling(20).std()
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"lvr":lvr,"r1":r1,
                             "r5p":c/c.shift(5)-1,"r10p":c/c.shift(10)-1,"r20p":c/c.shift(20)-1,"r30p":c/c.shift(30)-1,
                             "vol20":vol20,"fwd":c.shift(-H)/c-1,"fwd5":c.shift(-5)/c-1,"fwd20":c.shift(-20)/c-1,
                             "yr":ts.dt.year,"alloc":b["postRebalance_current_allocation"]})
            df["r10s"]=df["r10p"]/(vol20*np.sqrt(10))
            df["r20s"]=df["r20p"]/(vol20*np.sqrt(20))
            df["lvr_x_r1"]=lvr*np.sign(r1)
            df=df.iloc[::H]
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["fwd"])
    for f in ["fwd","fwd5","fwd20"]:
        d["z_"+f]=(d[f]-d.groupby("coin")[f].transform("mean"))/d.groupby("coin")[f].transform("std")
    d["z"]=d["z_fwd"]
    def slope(s,col,y="z"):
        s=s.dropna(subset=[col,y]).copy()
        s[col]=s.groupby("coin")[col].transform(lambda x:(x-x.mean())/x.std())
        r=stats.linregress(s[col],s[y]); return pd.Series({"n":len(s),"slope":r.slope,"t":r.slope/r.stderr})
    out={}
    out["mom_lookbacks_h10"]=pd.DataFrame({c:slope(d,c) for c in ["r5p","r10p","r20p","r30p","r10s","r20s","lvr_x_r1"]}).T
    out["r10p_horizons"]=pd.DataFrame({y:slope(d,"r10p",y) for y in ["z_fwd5","z_fwd","z_fwd20"]}).T
    out["r20p_horizons"]=pd.DataFrame({y:slope(d,"r20p",y) for y in ["z_fwd5","z_fwd","z_fwd20"]}).T
    out["r10p_by_coin"]=pd.DataFrame({c:slope(d[d.coin==c],"r10p") for c in d.coin.unique()}).T
    out["r10p_by_year"]=pd.DataFrame({y:slope(d[d.yr==y],"r10p") for y in sorted(d.yr.unique())}).T
    d["volq"]=d.groupby("coin")["vol20"].transform(lambda x:pd.qcut(x,3,labels=False))
    out["r10p_by_volterc"]=pd.DataFrame({q:slope(d[d.volq==q],"r10p") for q in [0,1,2]}).T
    out["lvr_lowvol_by_year"]=pd.DataFrame({y:slope(d[(d.yr==y)&(d.volq==0)],"lvr") for y in sorted(d.yr.unique())}).T
    out["lvr_lowvol_by_coin"]=pd.DataFrame({c:slope(d[(d.coin==c)&(d.volq==0)],"lvr") for c in d.coin.unique()}).T
    # interaction: lvr slope by sign of r10p
    d["up10"]=np.sign(d["r10p"])
    out["lvr_by_r10sign"]=pd.DataFrame({s:slope(d[d.up10==s],"lvr") for s in [-1,1]}).T
    # book: daily returns, largest gains/losses context
    dl=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w
            x["cr_prev10"]=(1+x["coin_return"]).rolling(10).apply(np.prod,raw=True).shift(1)-1
            dl.append(x)
    D=pd.concat(dl).dropna(subset=["book_return"])
    q=D["book_return"].quantile([0.01,0.99])
    out["book_tails_context"]=pd.DataFrame({
        "worst1pct":[ (D.book_return<=q[0.01]).sum(), D.loc[D.book_return<=q[0.01],"coin_return"].mean(), D.loc[D.book_return<=q[0.01],"cr_prev10"].mean()],
        "best1pct":[ (D.book_return>=q[0.99]).sum(), D.loc[D.book_return>=q[0.99],"coin_return"].mean(), D.loc[D.book_return>=q[0.99],"cr_prev10"].mean()],
        "all":[len(D),D.coin_return.mean(),D.cr_prev10.mean()]},index=["n","coin_ret","coin_prev10"])
    return out
