def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    drift={}
    for coin,wins in data["bars"].items():
        allr=[]
        for w,b in wins.items():
            c=b["close"].values
            for i in range(0,len(c)-H,H): allr.append(c[i+H]/c[i]-1)
        drift[coin]=np.mean(allr)
    rows=[]; pos=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd20=r.rolling(20).std()
            z20=np.log(c/c.shift(20))/(sd20*np.sqrt(20))
            r1z=r/sd20.shift(1)
            ts=pd.to_datetime(b["timestamp"])
            fwd=c.shift(-H)/c-1
            al=b["postRebalance_current_allocation"].fillna(0)
            nxt=c.shift(-1)/c-1
            for i in range(len(b)-1):
                pos.append(dict(reg=b["regime"].iloc[i],al=al.iloc[i],g=al.iloc[i]*nxt.iloc[i],
                    zs=np.sign(z20.iloc[i]) if pd.notna(z20.iloc[i]) else np.nan,
                    fs=np.sign(b["forecast"].iloc[i])))
            for i in range(0,len(b)-H,H):
                rows.append(dict(coin=coin,day=ts.iloc[i].normalize(),z20=z20[i],r1z=r1z[i],
                    ex=fwd[i]-drift[coin],reg=b["regime"].iloc[i],fc=b["forecast"].iloc[i],
                    wd=ts.iloc[i].dayofweek,yr=ts.iloc[i].year))
    df=pd.DataFrame(rows).dropna(subset=["z20","ex"])
    def pooled_slope(d,col):
        d=d.dropna(subset=[col,"ex"]); p=d.groupby("day")[[col,"ex"]].mean()
        if len(p)<20: return "n/a"
        s=stats.linregress(p[col],p["ex"]); return f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} days {len(p)}"
    def pooled_mean(x,day):
        p=pd.Series(x.values,index=day.values).groupby(level=0).sum()
        # t of summed-per-day deviations
        n=len(x); m=x.mean(); dev=(pd.Series(x.values-m,index=day.values)).groupby(level=0).sum()
        se=np.sqrt((dev**2).sum())/n; return m, m/se, len(dev)
    ch=df[df.reg=="unknown"].copy(); nc=df[df.reg!="unknown"].copy()
    out={}
    out["pooled slopes"]=pd.Series({"z20 choppy":pooled_slope(ch,"z20"),"z20 nonchoppy":pooled_slope(nc,"z20"),
        "z20 all":pooled_slope(df,"z20"),"r1z all":pooled_slope(df,"r1z"),"r1z choppy":pooled_slope(ch,"r1z"),
        "r1z nonchoppy":pooled_slope(nc,"r1z"),"fc choppy":pooled_slope(ch[ch.fc!=0],"fc"),
        "z20 choppy 2018-19":pooled_slope(ch[ch.yr<=2019],"z20"),"z20 choppy 2020-21":pooled_slope(ch[ch.yr>=2020],"z20"),
        "z20 nonchoppy 2018-19":pooled_slope(nc[nc.yr<=2019],"z20"),"z20 nonchoppy 2020-21":pooled_slope(nc[nc.yr>=2020],"z20")})
    a=ch[ch.fc!=0]
    out["choppy: sign(forecast)==sign(z20) share"]=float((np.sign(a.fc)==np.sign(a.z20)).mean())
    res={}
    for nm,s in [("by z20 sign",np.sign(ch.z20)),("by forecast sign",np.sign(ch.fc))]:
        m=ch[s!=0]; ss=s[s!=0]; x=m.ex*ss
        mm,t,nd=pooled_mean(x,m.day); res[nm]=f"dir ex {mm:.4f} t {t:.2f} days {nd} n {len(x)}"
    for sd in [-1,1]:
        m=ch[np.sign(ch.z20)==sd]; mm,t,nd=pooled_mean(m.ex*sd,m.day); res[f"z20 side {sd}"]=f"dir ex {mm:.4f} t {t:.2f} days {nd}"
        m=ch[np.sign(ch.fc)==sd]; mm,t,nd=pooled_mean(m.ex*sd,m.day); res[f"fc side {sd}"]=f"dir ex {mm:.4f} t {t:.2f} days {nd}"
    out["choppy directional"]=pd.Series(res)
    # r1z top quintile pooled
    q=df.r1z.quantile([0.2,0.8]); res={}
    for nm,m in [("r1z top20% all",df[df.r1z>=q.iloc[1]]),("r1z bot20% all",df[df.r1z<=q.iloc[0]]),
                 ("r1z top20% nonchoppy",nc[nc.r1z>=q.iloc[1]]),("r1z top20% choppy",ch[ch.r1z>=q.iloc[1]])]:
        mm,t,nd=pooled_mean(m.ex,m.day); res[nm]=f"ex {mm:.4f} t {t:.2f} days {nd} n {len(m)}"
    out["one-day move tails"]=pd.Series(res)
    # weekday pooled
    res={}
    for wd,m in df.groupby("wd"):
        mm,t,nd=pooled_mean(m.ex,m.day); res[wd]=f"ex {mm:.4f} t {t:.2f} days {nd}"
    out["weekday pooled"]=pd.Series(res)
    # nonchoppy z20 quintiles pooled
    nc["b"]=pd.qcut(nc.z20,5,labels=False); res={}
    for bq,m in nc.groupby("b"):
        mm,t,nd=pooled_mean(m.ex,m.day); res[bq]=f"z {m.z20.mean():.2f} ex {mm:.4f} t {t:.2f} days {nd}"
    out["nonchoppy z20 quint pooled"]=pd.Series(res)
    P=pd.DataFrame(pos); P=P[P.al!=0].copy(); P["aside"]=np.sign(P.al)
    out["book gain by alloc side x z20 sign"]=P.groupby(["aside","zs"])["g"].agg(["size","mean","sum"]).round(5)
    return out
