def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            v=b["volume"].astype(float)
            n=len(c)
            ret30=c/c.shift(30)-1
            hi60=c.rolling(60,min_periods=20).max()
            depth=c/hi60-1
            r7p=c/c.shift(7)-1
            r1=c.pct_change()
            vol20=r1.rolling(20).std()
            vrel=v/v.rolling(20).mean()
            newhigh=(c>=c.shift(1).rolling(60,min_periods=20).max()).astype(float)
            fwd7=c.shift(-7)/c-1
            fwd1=c.shift(-1)/c-1
            wd=pd.to_datetime(b["timestamp"]).dt.weekday
            for i in range(0,n,7):
                if i+7>=n: break
                rows.append(dict(coin=coin,w=w,ret30=ret30[i],depth=depth[i],r7p=r7p[i],vol20=vol20[i],
                    vrel=vrel[i],newhigh=newhigh[i],fwd7=fwd7[i],fc=b["forecast"][i],
                    alloc=b["postRebalance_current_allocation"][i]))
    g=pd.DataFrame(rows)
    g["ex"]=g["fwd7"]-g.groupby("coin")["fwd7"].transform("mean")
    out={}
    def tab(df,col,q=5):
        d=df.dropna(subset=[col,"ex"]).copy()
        d["q"]=pd.qcut(d[col].rank(method="first"),q,labels=False)
        t=d.groupby("q")["ex"].agg(["mean","count"])
        t["t"]=d.groupby("q")["ex"].apply(lambda x:x.mean()/(x.std()/np.sqrt(len(x))))
        return t
    def slope(df,col):
        d=df.dropna(subset=[col,"ex"])
        r=stats.linregress(d[col],d["ex"]); return f"slope {r.slope:.4g} t {r.slope/r.stderr:.2f} n {len(d)}"
    out["depth q, ret30<0"]=tab(g[g.ret30<0],"depth")
    out["depth q, ret30>=0"]=tab(g[g.ret30>=0],"depth")
    out["slope depth all"]=slope(g,"depth")
    out["slope depth ret30>=0"]=slope(g[g.ret30>=0],"depth")
    out["r7p q all"]=tab(g,"r7p")
    out["ret30 q all"]=tab(g,"ret30")
    out["slope ret30"]=slope(g,"ret30")
    out["vol20 q"]=tab(g,"vol20")
    out["vrel q"]=tab(g,"vrel")
    nh=g.dropna(subset=["ex"]).groupby("newhigh")["ex"]
    out["newhigh ex"]=nh.agg(["mean","count"])
    a=g.loc[g.newhigh==1,"ex"];bb=g.loc[g.newhigh==0,"ex"]
    out["newhigh t"]=float(stats.ttest_ind(a,bb,equal_var=False).statistic)
    # daily weekday and book
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy();d["coin"]=coin;d["w"]=w;dd.append(d)
    D=pd.concat(dd)
    D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    wt=D.groupby("wd")["coin_return"].agg(["mean","count","std"])
    wt["t"]=wt["mean"]/(wt["std"]/np.sqrt(wt["count"]))
    out["weekday coin"]=wt
    out["year coin/book"]=D.assign(y=pd.to_datetime(D["day"]).dt.year).groupby("y")[["coin_return","book_return"]].mean()
    out["coin book means"]=D.groupby("coin")[["coin_return","book_return"]].mean()
    return out
