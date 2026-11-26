def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            v30=r.rolling(30,min_periods=20).std()
            vol=r.rolling(20,min_periods=15).std().shift(1)
            tr60=c/c.shift(60)-1
            d={"coin":coin,"w":w,"i":np.arange(len(b)),"ts":pd.to_datetime(b["timestamp"]),
               "r":r,"z":r/vol,"tr60":tr60,"v30":v30,
               "pos":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)}
            for L in (10,20,30):
                hi=c.rolling(L).max(); lo=c.rolling(L).min()
                d[f"rp{L}"]=(c-lo)/(hi-lo).replace(0,np.nan)
            for h in (1,3,5):
                d[f"f{h}"]=c.shift(-h)/c-1
            rows.append(pd.DataFrame(d))
    D=pd.concat(rows,ignore_index=True)
    D["day"]=D.ts.dt.floor("D"); D["yr"]=D.ts.dt.year
    for h in (1,3,5):
        mu=D[D.i%h==0].groupby("coin")[f"f{h}"].mean(); D[f"x{h}"]=D[f"f{h}"]-D.coin.map(mu)
    med=D.groupby("coin").v30.transform("median")
    D["agit"]=np.where(D.v30>med,"agit","calm")
    D["trb"]=pd.cut(D.tr60,[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    def tt(s,days):
        g=pd.DataFrame({"s":s,"d":days}).dropna()
        if len(g)<8: return (np.nan,np.nan,len(g),0)
        m=g.s.mean(); ds=(g.s-m).groupby(g.d).sum()
        se=np.sqrt((ds**2).sum())/len(g)
        return (m,m/se if se>0 else np.nan,len(g),len(ds))
    out={}
    CC=D[(D.trb=="chop")&(D.agit=="calm")]
    res=[]
    for L in (10,20,30):
        for h in (3,5):
            g=CC[CC.i%h==0].copy(); g["s"]=(g[f"rp{L}"]-0.5)*2  # -1 bottom, +1 top
            g=g.dropna(subset=["s",f"x{h}"])
            m,t,n,nd=tt(g[f"x{h}"]*np.sign(g.s)*g.s.abs()/g.s.abs().mean(),g.day)
            sl=np.polyfit(g.s,g[f"x{h}"],1)[0]
            res.append([L,h,n,nd,m*100,t,sl*100])
    out["chopcalm_momentum_signed_rpos"]=pd.DataFrame(res,columns=["L","h","n","days","mean%_cont","t","slope%"])
    g=CC[CC.i%3==0].copy(); g["s"]=np.sign(g.rp20-0.5)
    res=[]
    for a,q in g.groupby("yr"):
        m,t,n,nd=tt(q.x3*q.s,q.day); res.append([a,n,m*100,t])
    out["chopcalm_rp20_cont_next3_by_year"]=pd.DataFrame(res,columns=["yr","n","mean%","t"])
    # compare other profiles signed continuation
    res=[]
    for (a,b_),q in D[D.i%3==0].groupby(["trb","agit"],observed=True):
        q=q.dropna(subset=["rp20","x3"]); s=(q.rp20-0.5)*2
        m,t,n,nd=tt(q.x3*s,q.day); res.append([a,b_,n,m*100,t])
    out["all_profiles_rp20_cont_next3"]=pd.DataFrame(res,columns=["trend","agit","n","mean%","t"])
    # falling agitated short side: up days by close position in bar
    FA=D[(D.trb=="fall")&(D.agit=="agit")&(D.z>0)].copy()
    FA["pb"]=pd.cut(FA.pos,[-0.01,0.33,0.66,1.01])
    res=[]
    for a,q in FA.groupby("pb",observed=True):
        m,t,n,nd=tt(q.x1,q.day); res.append([str(a),n,nd,m*100,t])
    out["fallagit_upday_next1_by_closepos"]=pd.DataFrame(res,columns=["closepos","n","days","mean%","t"])
    return out
