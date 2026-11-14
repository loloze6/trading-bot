import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]; samp=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            f=b["forecast"].astype(float)
            a=b["postRebalance_current_allocation"].astype(float)
            v=b["postRebalance_total_value"].astype(float)
            r1=c.shift(-1)/c-1
            br=v.shift(-1)/v-1
            mom20=c/c.shift(20)-1
            hi=c/c.rolling(30,min_periods=10).max()-1
            dd=v/v.cummax()-1
            df=pd.DataFrame(dict(coin=coin,w=w,f=f,a=a,r1=r1,br=br,mom20=mom20,hi=hi,dd=dd,pos=np.arange(len(b))))
            rows.append(df)
            idx=np.arange(0,len(b)-10,10)
            s=df.iloc[idx].copy(); s["fr"]=(c.shift(-10)/c-1).iloc[idx].values
            samp.append(s)
    D=pd.concat(rows); S=pd.concat(samp)
    S["ex"]=S["fr"]-S.groupby("coin")["fr"].transform("mean")
    out={}
    # momentum effect in flat state too
    off=S[S.f==0].dropna(subset=["mom20","ex"]).copy()
    off["q"]=pd.qcut(off.mom20,4,labels=False)
    t=off.groupby("q").agg(n=("ex","count"),mid=("mom20","median"),ex=("ex","mean"),sd=("ex","std"))
    t["t"]=t.ex/(t.sd/np.sqrt(t.n)); out["flat 10bar excess by q mom20"]=t.drop(columns="sd")
    # active, regression ex on f within mom20 sign
    on=S[S.f>0].dropna(subset=["mom20","ex"])
    res={}
    for nm,g in [("mom>0",on[on.mom20>0]),("mom<=0",on[on.mom20<=0])]:
        r=stats.linregress(g.f,g.ex); res[nm]=dict(n=len(g),mean_ex=g.ex.mean(),t_mean=g.ex.mean()/(g.ex.std()/np.sqrt(len(g))),slope=r.slope,t_slope=r.slope/r.stderr)
    out["active by mom sign"]=pd.DataFrame(res).T
    # book daily by mom sign while active
    act=D[D.a>0].dropna(subset=["br","mom20"])
    act=act.assign(ms=np.where(act.mom20>0,"up","down"))
    out["active daily book by mom sign"]=act.groupby("ms").agg(n=("br","count"),book=("br","mean"),coin=("r1","mean"),alloc=("a","mean"),bsd=("br","std"))
    # proxy book: gain a*r1 vs gain a*r1*(mom>0)
    D2=D.dropna(subset=["r1","mom20"]).copy()
    D2["g0"]=D2.a*D2.r1; D2["g1"]=D2.g0*(D2.mom20>0); D2["g2"]=D2.a*D2.r1*np.clip(D2.mom20/0.1,0,1)
    def stat(x):
        eq=np.cumprod(1+x.values); mdd=(eq/np.maximum.accumulate(eq)-1).min()
        yr=eq[-1]**(365/len(x))-1
        return dict(mean=x.mean(),sharpe=x.mean()/x.std()*np.sqrt(365),calmar=yr/abs(mdd),mdd=mdd)
    D2=D2.sort_values(["w","coin","pos"])
    port={}
    for g in ["g0","g1","g2","r1"]:
        daily=D2.groupby(["w","pos"])[g].mean()
        port[g]=stat(daily)
    out["proxy books (avg coins)"]=pd.DataFrame(port).T
    # deepest falls: state at bars inside book drawdown <-15%
    deep=D[(D.dd<-0.15)&(D.a>0)].dropna(subset=["mom20"])
    out["in deep dd vs active"]=pd.DataFrame({"deep":deep[["mom20","hi","a","f"]].median(),"active":act[["mom20","hi","a","f"]].median(),"share_mom_down":pd.Series({"mom20":(deep.mom20<=0).mean(),"hi":(act.mom20<=0).mean()})})
    out["book by window"]=D.groupby("w").agg(book=("br","mean"),coin=("r1","mean"))
    return out
