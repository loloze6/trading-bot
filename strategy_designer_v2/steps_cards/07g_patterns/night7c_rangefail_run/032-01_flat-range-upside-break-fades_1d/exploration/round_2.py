def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    rows=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float); hi=df["high"].astype(float); lo=df["low"].astype(float)
            n=len(df)
            ch=c.diff().abs()
            er=((c-c.shift(60)).abs()/ch.rolling(60).sum()).rolling(5).mean()
            ph=hi.shift(1).rolling(60).max()
            dup=c/ph-1
            r1=c.pct_change(); vol20=r1.rolling(20).std()
            ts=pd.to_datetime(df["timestamp"]).dt.normalize()
            f={h:c.shift(-h)/c-1 for h in (1,3,5,10)}
            for i in range(n):
                rows.append((coin,w,i,ts.iloc[i],er.iloc[i],dup.iloc[i],r1.iloc[i],vol20.iloc[i],f[1].iloc[i],f[3].iloc[i],f[5].iloc[i],f[10].iloc[i]))
    d=pd.DataFrame(rows,columns=["coin","w","i","day","er","dup","r1","vol20","f1","f3","f5","f10"])
    for h in (1,3,5,10):
        g=d[d.i%h==0].dropna(subset=[f"f{h}"])
        dr=g.groupby("coin")[f"f{h}"].mean(); us=g.groupby("coin")[f"f{h}"].std()
        d[f"u{h}"]=d[f"f{h}"]-d.coin.map(dr); d[f"s{h}"]=d[f"u{h}"]/d.coin.map(us)
    def tday(x,day):
        ds=x.groupby(day).sum(); 
        return ds.mean()/(ds.std(ddof=1)/np.sqrt(len(ds))) if len(ds)>2 else np.nan
    # A: trendless upside breakouts, long side, 10d, case per grid cell
    d["cell10"]=d.i//10
    up=d[(d.dup>0)&(d.er<=0.3)].dropna(subset=["f10"]).groupby(["coin","w","cell10"]).head(1).copy()
    up["dupv"]=up.dup/up.vol20
    out["A_all"]=pd.Series({"n":len(up),"days":up.day.nunique(),"mean_u":up.u10.mean(),"t_day":tday(up.u10,up.day),"strength":up.s10.mean(),"total":up.f10.mean(),"hit":(up.u10>0).mean()})
    out["A_by_window"]=up.groupby("w").agg(n=("u10","size"),mean_u=("u10","mean"))
    out["A_by_coin"]=up.groupby("coin").agg(n=("u10","size"),mean_u=("u10","mean"),hit=("u10",lambda x:(x>0).mean()))
    up["erq"]=pd.qcut(up.er,3,labels=False)
    out["A_by_er_tercile"]=up.groupby("erq").agg(n=("u10","size"),er=("er","mean"),mean_u=("u10","mean"))
    up["vq"]=pd.qcut(up.dupv,3,labels=False)
    out["A_by_overshoot_volunits"]=up.groupby("vq").agg(n=("u10","size"),dupv=("dupv","mean"),mean_u=("u10","mean"))
    out["A_spearman_er_u"]=pd.Series(stats.spearmanr(up.er,up.u10),index=["rho","p"])
    # horizons for the same events (other grids)
    res={}
    for h in (3,5):
        d[f"cell{h}"]=d.i//h
        e=d[(d.dup>0)&(d.er<=0.3)].dropna(subset=[f"f{h}"]).groupby(["coin","w",f"cell{h}"]).head(1)
        res[h]=pd.Series({"n":len(e),"mean_u":e[f"u{h}"].mean(),"t_day":tday(e[f"u{h}"],e.day)})
    out["A_other_horizons"]=pd.DataFrame(res).T
    # B: next-day reversal graded by z of today's return
    dd=d.dropna(subset=["r1","vol20","u1"]).copy()
    dd["z"]=dd.r1/dd.vol20
    dd["y"]=-np.sign(dd.z)*dd.u1  # reversal side
    dd["zb"]=pd.cut(dd.z.abs(),[0,0.5,1,2,99])
    out["B_rev_by_absz"]=dd.groupby("zb",observed=True).apply(lambda s:pd.Series({"n":len(s),"mean":s.y.mean(),"t_day":tday(s.y,s.day)}))
    dn=dd[dd.z<-1]
    out["B_down_by_window"]=dn.groupby("w").agg(n=("u1","size"),mean=("u1","mean"))
    out["B_down_by_coin"]=dn.groupby("coin").apply(lambda s:pd.Series({"n":len(s),"mean":s.u1.mean(),"t_day":tday(s.u1,s.day)}))
    out["B_down_all"]=pd.Series({"n":len(dn),"days":dn.day.nunique(),"mean":dn.u1.mean(),"t_day":tday(dn.u1,dn.day),"strength":dn.s1.mean()})
    out["B_corr_z_u1_bycoin"]=dd.groupby("coin").apply(lambda s:pd.Series(stats.spearmanr(s.z,s.u1),index=["rho","p"]))
    # 3-day reversal after 3-day fall, non-overlapping
    d["r3"]=d.groupby(["coin","w"]).r1.transform(lambda x:(1+x).rolling(3).apply(np.prod,raw=True)-1)
    g3=d[d.i%3==0].dropna(subset=["r3","u3","vol20"]).copy()
    g3["z3"]=g3.r3/(g3.vol20*np.sqrt(3))
    g3["zq"]=pd.cut(g3.z3,[-99,-2,-1,0,1,2,99])
    out["C_3d_after_3d_z"]=g3.groupby("zq",observed=True).apply(lambda s:pd.Series({"n":len(s),"mean":s.u3.mean(),"t_day":tday(s.u3,s.day)}))
    return out
