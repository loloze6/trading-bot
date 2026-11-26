def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        # coin drift per horizon over all windows' grids
        drift={}
        for h in (3,7,14):
            rs=[]
            for w,df in wins.items():
                c=df["close"].values
                for i in range(0,len(c)-h,h):
                    rs.append(c[i+h]/c[i]-1)
            drift[h]=np.mean(rs) if rs else np.nan
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"]
            r1=c.pct_change()
            sd=r1.rolling(30,min_periods=20).std()
            past=c/c.shift(7)-1
            z=past/(sd*np.sqrt(7))
            inprof=(df["regime"]=="unknown")
            n=len(df)
            for h in (3,7,14):
                for i in range(0,n-h,h):
                    if np.isnan(z.iloc[i]): continue
                    fwd=c.iloc[i+h]/c.iloc[i]-1
                    rows.append(dict(coin=coin,win=w,h=h,i=i,z=z.iloc[i],prof=bool(inprof.iloc[i]),
                        fc=df["forecast"].iloc[i],ex=fwd-drift[h],fwd=fwd,year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    d=pd.DataFrame(rows)
    out={}
    def summ(g):
        return pd.Series(dict(n=len(g),mean_ex=g.ex.mean(),t=g.ex.mean()/(g.ex.std()/np.sqrt(len(g))) if len(g)>2 else np.nan,
                              spear=stats.spearmanr(g.z,g.ex)[0] if len(g)>3 else np.nan))
    d["zb"]=pd.cut(d.z,[-99,-1.5,-0.75,0,0.75,1.5,99])
    out["prof_by_zbucket_h"]=d[d.prof].groupby(["h","zb"]).apply(summ)
    out["outside_by_zbucket_h7"]=d[(~d.prof)&(d.h==7)].groupby("zb").apply(summ)
    p7=d[(d.prof)&(d.h==7)&(d.z>0)]
    out["prof_rise_h7_by_coin"]=p7.groupby("coin").apply(summ)
    out["prof_rise_h7_by_year"]=p7.groupby("year").apply(summ)
    out["prof_rise_h7_fcpos"]=summ(d[(d.prof)&(d.h==7)&(d.fc>0)])
    out["prof_all_h_side_signed"]=d[d.prof].assign(s=np.sign(d.z)).groupby(["h","s"]).apply(lambda g: summ(g.assign(ex=g.ex*g.s)))
    return out
