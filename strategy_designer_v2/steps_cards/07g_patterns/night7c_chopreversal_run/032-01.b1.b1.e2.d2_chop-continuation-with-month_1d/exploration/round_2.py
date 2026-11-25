def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].astype(float).reset_index(drop=True)
            r=c.pct_change()
            er=(c-c.shift(30)).abs()/(c.diff().abs().rolling(30).sum())
            r7=c/c.shift(7)-1; r30=c/c.shift(30)-1
            vol=r.rolling(30).std()
            vol90=r.rolling(90,min_periods=60).std()
            fwd=c.shift(-7)/c-1
            fwd3=c.shift(-3)/c-1
            df=pd.DataFrame({"coin":coin,"w":w,"er":er,"r7":r7,"r30":r30,"vol":vol,"vr":vol/vol90,"fwd":fwd,
                             "alloc":b["postRebalance_current_allocation"].values})
            rows.append(df.iloc[::7])
    d=pd.concat(rows).dropna(subset=["er","r30","fwd","vol"])
    d["ex"]=d.fwd-d.groupby("coin")["fwd"].transform("mean")
    d["s7"]=d.r7/(d.vol*np.sqrt(7)); d["s30"]=d.r30/(d.vol*np.sqrt(30))
    d["s23"]=(((1+d.r30)/(1+d.r7))-1)/(d.vol*np.sqrt(23))
    d["chop"]=d.er<=0.3
    def reg(g,col):
        g=g.dropna(subset=[col,"ex"])
        x=np.sign(g[col])*g.ex; sl=stats.linregress(g[col],g.ex)
        return pd.Series({"n":len(g),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(g))),"slope_t":sl.slope/sl.stderr})
    out={}
    ch=d[d.chop]
    out["chop_s30"]=reg(ch,"s30"); out["chop_s7"]=reg(ch,"s7"); out["chop_s23_older"]=reg(ch,"s23")
    X=np.column_stack([np.ones(len(ch)),ch.s7,ch.s23]); y=ch.ex.values
    beta,res,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@beta
    cov=np.linalg.inv(X.T@X)*(e@e/(len(y)-3))
    out["chop_multi_s7_s23"]=pd.Series({"b_s7":beta[1],"t_s7":beta[1]/np.sqrt(cov[1,1]),"b_s23":beta[2],"t_s23":beta[2]/np.sqrt(cov[2,2])})
    ch=ch.copy(); ch["vq"]=ch.groupby("coin")["vol"].transform(lambda v: pd.qcut(v,3,labels=False))
    out["chop_s30_by_volq"]=ch.groupby("vq").apply(lambda g: reg(g,"s30"))
    ch["vrq"]=pd.qcut(ch.vr,3,labels=False)
    out["chop_s30_by_vol_ratio"]=ch.groupby("vrq").apply(lambda g: reg(g,"s30"))
    ch["erb"]=pd.cut(ch.er,[0,0.1,0.2,0.3])
    out["chop_s30_by_er"]=ch.groupby("erb").apply(lambda g: reg(g,"s30"))
    hi=d[d.er>0.5]
    out["trend_er_gt05_s7"]=reg(hi,"s7"); out["trend_er_gt05_s30"]=reg(hi,"s30")
    out["chop_s30_by_coin"]=ch.groupby("coin").apply(lambda g: reg(g,"s30"))
    # book extremes
    dd=pd.concat([x.assign(coin=c,w=w) for c,ws in data["days"].items() for w,x in ws.items()])
    bk=dd.groupby(["w","day"]).agg(b=("book_return","mean"),h=("coin_return","mean")).dropna()
    q=bk.b.quantile([0.02,0.98])
    out["book_tails"]=pd.DataFrame({"n":[ (bk.b<=q.iloc[0]).sum(),(bk.b>=q.iloc[1]).sum()],
        "book_mean":[bk.b[bk.b<=q.iloc[0]].mean(),bk.b[bk.b>=q.iloc[1]].mean()],
        "hold_mean":[bk.h[bk.b<=q.iloc[0]].mean(),bk.h[bk.b>=q.iloc[1]].mean()]},index=["worst2%","best2%"])
    out["corr_book_hold"]=bk.b.corr(bk.h)
    return out
