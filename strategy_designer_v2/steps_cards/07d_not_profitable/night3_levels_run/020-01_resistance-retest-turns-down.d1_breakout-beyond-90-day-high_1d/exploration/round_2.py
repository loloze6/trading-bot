def explore(data):
    import numpy as np, pandas as pd
    out = {}
    pos_rows=[]; prox=[]; ddc=[]; fall=[]
    drift={}
    for coin, wins in data["bars"].items():
        for h in (5,10,20):
            rs=[]
            for w,b in wins.items():
                c=b["close"].values
                rs+=[c[i+h]/c[i]-1 for i in range(0,len(c)-h,h)]
            drift[(coin,h)]=(np.mean(rs),np.std(rs))
    for coin, wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(c)
            pos=b["postRebalance_current_allocation"].fillna(0).values
            f=b["forecast"].fillna(0).values
            vol=b["sizing_realised_vol"].values
            on=np.abs(pos)>1e-6
            pos_rows.append({"coin":coin,"pos_when_in":pos[on].mean() if on.any() else np.nan,
                             "f_when_in":f[on].mean() if on.any() else np.nan,
                             "share_in_with_f0":(on&(f<=0)).sum()/max(on.sum(),1)})
            # recomputed: distance to prior 90-close high (within window), and days since last new high
            s=pd.Series(c)
            hi=s.shift(1).rolling(90,min_periods=30).max().values
            dist=c/hi-1
            newhigh=dist>0
            last=-10**9; since=np.full(n,np.nan)
            for i in range(n):
                if newhigh[i]: last=i
                since[i]=i-last if last>-10**8 else np.nan
            r1=np.append(c[1:]/c[:-1]-1,np.nan)
            g=pos*r1
            ret20=np.full(n,np.nan); ret20[20:]=c[20:]/c[:-20]-1
            for h in (20,):
                for i in range(0,n-h,h):
                    if np.isnan(dist[i]): continue
                    m,sd=drift[(coin,h)]
                    prox.append({"coin":coin,"dist":dist[i],"since":since[i],
                                 "u":(c[i+h]/c[i]-1)-m,"ret20":ret20[i]})
            # gain by days since last new high when in position
            for i in range(n-1):
                if on[i] and not np.isnan(since[i]):
                    fall.append({"since":since[i],"g":g[i],"pos":pos[i],"dist":dist[i]})
    out["position_when_in"]=pd.DataFrame(pos_rows).groupby("coin").mean()
    P=pd.DataFrame(prox).dropna(subset=["dist","u"])
    P["dq"]=pd.cut(P["dist"],[-1,-0.5,-0.3,-0.15,-0.05,0,0.05,0.15,5])
    g=P.groupby("dq")["u"]
    out["u20_by_distance_to_90d_high"]=pd.DataFrame({"mean":g.mean(),"n":g.count(),
        "t":g.mean()/(g.std()/np.sqrt(g.count()))})
    P2=P[P["since"].notna()].copy()
    P2["sq"]=pd.cut(P2["since"],[-1,0,5,10,20,40,1000])
    g=P2.groupby("sq")["u"]
    out["u20_by_days_since_new_high"]=pd.DataFrame({"mean":g.mean(),"n":g.count(),
        "t":g.mean()/(g.std()/np.sqrt(g.count()))})
    F=pd.DataFrame(fall)
    F["sq"]=pd.cut(F["since"],[-1,0,2,5,10,20,1000])
    out["inposition_gain_by_days_since_high"]=F.groupby("sq").agg(mean_g=("g","mean"),n=("g","count"),
        mean_pos=("pos","mean"),mean_dist=("dist","mean"))
    # daily book: worst day returns, how much loss comes from days in position after the breakout faded
    allb=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            allb.append(d["book_return"].dropna().values)
    a=np.concatenate(allb)
    out["book_daily"]=pd.Series({"mean":a.mean(),"sd":a.std(),"n":len(a),"share_nonzero":(np.abs(a)>1e-9).mean()})
    return out
