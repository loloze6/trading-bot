def explore(data):
    import numpy as np, pandas as pd
    H=5
    ev=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=pd.Series(b["close"].astype(float).values)
            n=len(c)
            if n<80: continue
            r=c.pct_change()
            z=10*r/r.abs().rolling(60,min_periods=20).mean()
            newhi=c>=c.rolling(21).max()-1e-12
            newlo=c<=c.rolling(21).min()+1e-12
            vol=r.rolling(20).std()
            volrank=vol.rolling(250,min_periods=60).rank(pct=True)
            fwd=c.shift(-H)/c-1
            ts=pd.to_datetime(b["timestamp"])
            ma50=c.rolling(50).mean()
            bv=pd.Series(b["postRebalance_total_value"].astype(float).values)
            br=bv.pct_change()
            dfw=pd.DataFrame({"coin":coin,"w":w,"i":range(n),"r":r,"z":z,"newhi":newhi,"newlo":newlo,
                "volrank":volrank,"fwd":fwd,"wd":ts.dt.weekday,"yr":ts.dt.year,
                "above50":c>ma50,"r1n":r.shift(-1),"r3n":c.shift(-3)/c-1,"br":br,"r_prev":r.shift(1)})
            dfw["ex"]=dfw["fwd"]-dfw["fwd"].mean()
            dfw["ex3"]=dfw["r3n"]-dfw["r3n"].mean()
            ev.append(dfw)
    d=pd.concat(ev).dropna(subset=["z"])
    def tt(x):
        x=pd.Series(x).dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    def merged(mask,col="ex",h=H):
        out=[]
        for (coin,w),g in d[mask].groupby(["coin","w"]):
            last=-99
            for i,ex in zip(g["i"],g[col]):
                if i-last>h and not np.isnan(ex): out.append(ex); last=i
        return tt(out)
    res={}
    m=d.newlo&(d.z<=-10)
    res["newlo z<=-10 by coin"]=pd.DataFrame({c:merged(m&(d.coin==c)) for c in d.coin.unique()}).T
    res["newlo z<=-10 by year"]=pd.DataFrame({y:merged(m&(d.yr==y)) for y in sorted(d.yr.unique())}).T
    res["newlo z<=-10 above/below ma50, 3bar"]=pd.DataFrame({"below50_5":merged(m&~d.above50),"above50_5":merged(m&d.above50),
        "all_3bar":merged(m,"ex3",3),"newlo_z>-10":merged(d.newlo&(d.z>-10)),"z<=-10 not newlo":merged((~d.newlo)&(d.z<=-10))}).T
    res["newlo z<=-10 by volrank"]=pd.DataFrame({str(q):merged(m&(d.volrank>q[0])&(d.volrank<=q[1])) for q in [(0,.33),(.33,.66),(.66,1)]}).T
    # weekday next-day: Friday->Saturday? wd is bar's weekday, r1n is next day's return
    d["r1n_dm"]=d["r1n"]-d.groupby(["coin","w"])["r1n"].transform("mean")
    f=d.wd==4
    res["next1d after Thu bar (wd3) & Fri bar (wd4) by coin"]=pd.DataFrame({c:pd.concat([tt(d[(d.wd==3)&(d.coin==c)].r1n_dm).add_prefix("thu_"),tt(d[f&(d.coin==c)].r1n_dm).add_prefix("fri_")]) for c in d.coin.unique()}).T
    res["next1d after Fri bar by year"]=pd.DataFrame({y:tt(d[f&(d.yr==y)].r1n_dm) for y in sorted(d.yr.unique())}).T
    res["next1d demeaned by weekday"]=d.groupby("wd")["r1n_dm"].apply(tt).unstack()
    res["newhi z>=10 lowmid vol by coin"]=pd.DataFrame({c:merged(d.newhi&(d.z>=10)&(d.volrank<=.66)&(d.coin==c)) for c in d.coin.unique()}).T
    res["newhi z>=10 lowmid vol by year"]=pd.DataFrame({y:merged(d.newhi&(d.z>=10)&(d.volrank<=.66)&(d.yr==y)) for y in sorted(d.yr.unique())}).T
    # book's largest daily gains/losses: coin's prior 1-day move
    bb=d.dropna(subset=["br"])
    bb=bb[bb.br!=0]
    q=bb.br.quantile([.02,.98])
    res["book extreme days"]=pd.DataFrame({"worst2%":tt(bb[bb.br<=q.iloc[0]].r_prev),"best2%":tt(bb[bb.br>=q.iloc[1]].r_prev),
        "worst_wd_share_fri_sat":pd.Series({"n":0,"mean":bb[bb.br<=q.iloc[0]].wd.isin([4,5]).mean(),"t":np.nan})}).T
    return res
