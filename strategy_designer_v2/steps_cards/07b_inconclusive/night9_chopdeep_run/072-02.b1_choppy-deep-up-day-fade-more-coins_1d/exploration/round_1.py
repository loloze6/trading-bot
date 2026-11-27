def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            hi=c.rolling(20,min_periods=20).max()
            sd=r.rolling(20,min_periods=20).std()
            depth=(hi-c)/hi/sd
            tr60=(c/c.shift(60)-1)*100
            vol30=r.rolling(30,min_periods=30).std()
            volmed=vol30.rolling(90,min_periods=30).median()
            d=pd.DataFrame({"coin":coin,"w":w,"year":pd.to_datetime(b["timestamp"]).dt.year,
                "r":r,"depth":depth,"tr60":tr60,"agit":(vol30>volmed),
                "fc":b["forecast"].astype(float),"pos":b["postRebalance_current_allocation"].astype(float),
                "regime":b["regime"]})
            for h in [1,2,3,5]:
                d[f"f{h}"]=c.shift(-h)/c-1
            d["i"]=np.arange(len(d))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for h in [1,2,3,5]:
        D[f"x{h}"]=D[f"f{h}"]-D.groupby("coin")["f1"].transform("mean")*h
    out={}
    act=D[D.fc<0].copy()
    def terc(s,col,key="depth"):
        s=s.dropna(subset=[col,key])
        q=pd.qcut(s[key].rank(method="first"),3,labels=["shallow","mid","deep"])
        g=s.groupby(q)[col].agg(["mean","count"])
        t=stats.ttest_ind(s.loc[q=="deep",col],s.loc[q=="shallow",col],equal_var=False).statistic
        return g, t
    # active bars by forecast third, horizons
    res={}
    for h in [1,2,3,5]:
        s=act.dropna(subset=[f"x{h}"])
        q=pd.qcut(s["fc"].rank(method="first"),3,labels=["deep","mid","shallow"])
        res[h]={"deep":s.loc[q=="deep",f"x{h}"].mean(),"mid":s.loc[q=="mid",f"x{h}"].mean(),"shallow":s.loc[q=="shallow",f"x{h}"].mean(),
            "t":stats.ttest_ind(s.loc[q=="deep",f"x{h}"],s.loc[q=="shallow",f"x{h}"],equal_var=False).statistic,"n":len(s)}
    out["active_by_h(overlapping h>1)"]=pd.DataFrame(res).T
    # recomputed choppy days, up vs down
    ch=D[(D.tr60.abs()<=10)].dropna(subset=["r","depth","x1"])
    res={}
    for nm,s in [("up",ch[ch.r>0]),("down",ch[ch.r<=0]),("all",ch)]:
        g,t=terc(s,"x1"); res[nm]=list(g["mean"])+[t,len(s)]
    out["choppy_recomp_x1_terc"]=pd.DataFrame(res,index=["shallow","mid","deep","t","n"]).T
    # all days regardless profile
    al=D.dropna(subset=["r","depth","x1","tr60"])
    res={}
    for nm,s in [("rising",al[al.tr60>10]),("falling",al[al.tr60<-10]),("choppy_agit",ch[ch.agit]),("choppy_calm",ch[~ch.agit]),("all",al)]:
        g,t=terc(s,"x1"); res[nm]=list(g["mean"])+[t,len(s)]
    out["profiles_x1_terc_all_days"]=pd.DataFrame(res,index=["shallow","mid","deep","t","n"]).T
    # active by coin: corr fc with x1
    def ct(s):
        s=s.dropna(subset=["x1"]); 
        if len(s)<20: return pd.Series({"n":len(s)})
        rr=np.corrcoef(s.fc,s.x1)[0,1]; return pd.Series({"n":len(s),"corr_fc_x1":rr,"t":rr*np.sqrt((len(s)-2)/(1-rr**2)),"mean_x1":s.x1.mean()})
    out["active_by_coin"]=act.groupby("coin").apply(ct)
    out["active_by_year"]=act.groupby("year").apply(ct)
    out["active_by_agit"]=act.groupby("agit").apply(ct)
    return out
