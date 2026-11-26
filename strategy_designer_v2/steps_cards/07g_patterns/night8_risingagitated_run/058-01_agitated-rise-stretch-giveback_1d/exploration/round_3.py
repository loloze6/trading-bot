def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]
    rows=[]
    for coin in bars:
        for w,df in bars[coin].items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float)
            r1=c.pct_change()
            r20p=(c/c.shift(20)-1)*100
            r60p=(c/c.shift(60)-1)*100
            vol20=(r1*100).rolling(20).std()
            vol30=r1.rolling(30).std()
            fwd5=(c.shift(-5)/c-1)*100
            fwd10=(c.shift(-10)/c-1)*100
            ts=pd.to_datetime(df["timestamp"])
            for i in range(0,len(df),5):
                rows.append(dict(coin=coin,w=w,day=ts.iloc[i].normalize(),r60p=r60p.iloc[i],vol30=vol30.iloc[i],
                    z20=r20p.iloc[i]/(vol20.iloc[i]*np.sqrt(20)) if vol20.iloc[i]>0 else np.nan,
                    fwd5=fwd5.iloc[i],fwd10=fwd10.iloc[i] if i%10==0 else np.nan))
    G=pd.DataFrame(rows)
    G["ex5"]=G.fwd5-G.groupby("coin").fwd5.transform("mean")
    G["ex10"]=G.fwd10-G.groupby("coin").fwd10.transform("mean")
    G["usual"]=G.groupby("coin").fwd5.transform("std")
    G["trend"]=np.where(G.r60p>10,"rising",np.where(G.r60p<-10,"falling",np.where(G.r60p.notna(),"choppy","na")))
    G["vmed"]=G.groupby("coin").vol30.transform("median")
    G["agit"]=np.where(G.vol30>G.vmed,"agit","calm")
    G=G.dropna(subset=["z20","ex5"])
    out={}
    def reg(s,y="ex5"):
        s=s.dropna(subset=["z20",y])
        if len(s)<20: return "n<20"
        r=stats.linregress(s.z20,s[y]); return f"slope {r.slope:.3f} t {r.slope/r.stderr:.2f} n {len(s)}"
    ch=G[G.trend=="choppy"]
    out["choppy agit"]=reg(ch[ch.agit=="agit"]); out["choppy calm"]=reg(ch[ch.agit=="calm"])
    out["choppy 10d"]=reg(ch,"ex10")
    out["rising agit"]=reg(G[(G.trend=="rising")&(G.agit=="agit")]); out["rising calm"]=reg(G[(G.trend=="rising")&(G.agit=="calm")])
    c2=ch.copy(); c2["q"]=pd.qcut(c2.z20,4,labels=False)
    t=c2.groupby("q").agg(n=("ex5","size"),lo=("z20","min"),hi=("z20","max"),m=("ex5","mean"),sd=("ex5","std")); t["t"]=t.m/(t.sd/np.sqrt(t.n))
    out["choppy z20 q"]=t.drop(columns="sd")
    out["choppy by window"]=ch.groupby("w").apply(lambda s: pd.Series(dict(n=len(s),slope=stats.linregress(s.z20,s.ex5).slope if len(s)>4 else np.nan)))
    out["choppy by coin"]=ch.groupby("coin").apply(lambda s: pd.Series(dict(n=len(s),slope=stats.linregress(s.z20,s.ex5).slope if len(s)>4 else np.nan)))
    # signed unusual move in z20 direction, day-clustered t
    s=ch[ch.z20.abs()>0].copy(); s["sg"]=np.sign(s.z20)*s.ex5
    d=s.groupby("day").sg.sum(); n=len(s)
    m=s.sg.mean(); se=np.sqrt((d-d.index.map(lambda x:0)).pow(2).sum()- 0)/n
    dd=s.groupby("day").apply(lambda x:(x.sg-m).sum())
    out["choppy signed move"]=f"mean {m:.2f}% strength {(s.sg/s.usual).mean():.3f} t_dayclust {m/(np.sqrt((dd**2).sum())/n):.2f} days {len(dd)} n {n}"
    a=G.copy(); a["sg"]=np.sign(a.z20)*a.ex5; ma=a.sg.mean(); da=a.groupby("day").apply(lambda x:(x.sg-ma).sum())
    out["all signed move"]=f"mean {ma:.2f}% strength {(a.sg/a.usual).mean():.3f} t_dayclust {ma/(np.sqrt((da**2).sum())/len(a)):.2f} days {len(da)} n {len(a)}"
    return out
