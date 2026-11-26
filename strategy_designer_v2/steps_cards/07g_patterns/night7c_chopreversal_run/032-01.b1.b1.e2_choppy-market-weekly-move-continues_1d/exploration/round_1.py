def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; daily=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            net=(c-c.shift(30)).abs(); path=c.diff().abs().rolling(30).sum()
            er=net/path
            vol=r.rolling(30).std()
            s7=(c/c.shift(7)-1)/(vol*np.sqrt(7))
            s30=(c/c.shift(30)-1)/(vol*np.sqrt(30))
            f7=c.shift(-7)/c-1
            f1=c.shift(-1)/c-1
            s1=r/vol
            alloc=b["postRebalance_current_allocation"].astype(float)
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"er":er,"vol":vol,"s7":s7,"s30":s30,"f7":f7,"f1":f1,"s1":s1,
                             "alloc":alloc,"fc":b["forecast"].astype(float),"wd":ts.dt.weekday,"yr":ts.dt.year,
                             "pos":np.arange(len(b))})
            daily.append(df)
    D=pd.concat(daily,ignore_index=True)
    D["volr"]=D.groupby("coin")["vol"].rank(pct=True)
    G=D[D.pos%7==0].copy()
    G["drift"]=G.groupby("coin")["f7"].transform("mean")
    G["x"]=G.f7-G.drift
    out={}
    def slope(df,xc,yc):
        d=df[[xc,yc]].dropna()
        if len(d)<30: return (np.nan,np.nan,len(d))
        lr=stats.linregress(d[xc],d[yc]); return (lr.slope,lr.slope/lr.stderr,len(d))
    res=[]
    G["erb"]=pd.cut(G.er,[0,0.15,0.3,0.5,1.01])
    for k,g in G.groupby("erb",observed=True):
        s,t,n=slope(g,"s7","x"); s2,t2,_=slope(g,"s30","x"); res.append([str(k),s,t,n,s2,t2])
    out["s7_s30_slope_by_ER"]=pd.DataFrame(res,columns=["er","slope_s7","t_s7","n","slope_s30","t_s30"])
    res=[]
    G["vb"]=pd.cut(G.volr,[0,1/3,2/3,1.0])
    for k,g in G.groupby("vb",observed=True):
        s,t,n=slope(g,"s7","x"); s2,t2,_=slope(g,"s30","x"); res.append([str(k),s,t,n,s2,t2])
    out["slope_by_vol_tercile"]=pd.DataFrame(res,columns=["vol","slope_s7","t_s7","n","slope_s30","t_s30"])
    # quintiles of s7 in choppy
    ch=G[G.er<=0.3].copy(); ch["q"]=pd.qcut(ch.s7,5,labels=False)
    out["choppy_s7_quintile"]=ch.groupby("q")["x"].agg(["mean","count",lambda v:v.mean()/v.std()*np.sqrt(len(v))])
    # all bars s7 quintile
    G["q"]=pd.qcut(G.s7,5,labels=False)
    out["all_s7_quintile"]=G.groupby("q")["x"].agg(["mean","count",lambda v:v.mean()/v.std()*np.sqrt(len(v))])
    # daily: next-day vs scaled today move
    D["d1"]=D.f1-D.groupby("coin")["f1"].transform("mean")
    D["erb"]=pd.cut(D.er,[0,0.3,0.5,1.01])
    res=[]
    for k,g in D.groupby("erb",observed=True):
        s,t,n=slope(g,"s1","d1"); res.append([str(k),s,t,n])
    s,t,n=slope(D,"s1","d1"); res.append(["all",s,t,n])
    out["next_day_on_scaled_day"]=pd.DataFrame(res,columns=["er","slope","t","n"])
    out["weekday_next_day"]=D.groupby("wd")["d1"].agg(["mean","count",lambda v:v.mean()/v.std()*np.sqrt(len(v))])
    # book
    D["gain"]=D.alloc*D.f1
    D["side"]=np.sign(D.alloc)
    out["gain_by_side"]=D.groupby("side")["gain"].agg(["mean","sum","count"])
    out["gain_by_year"]=D.groupby("yr")["gain"].agg(["mean","count"])
    out["coin_gain"]=D.groupby("coin")["gain"].agg(["mean","count"])
    out["side_by_coin_corr"]=D.groupby("coin").apply(lambda g:np.corrcoef(g.s7.fillna(0),g.alloc.fillna(0))[0,1])
    return out
