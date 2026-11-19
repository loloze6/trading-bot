def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=72
    out={}
    hr=[];g=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float); r=c.pct_change()
            ts=pd.to_datetime(b["timestamp"])
            sd=r.rolling(480).std()
            hr.append(pd.DataFrame({"coin":coin,"w":w,"yr":ts.dt.year,"h":ts.dt.hour,"wd":ts.dt.weekday,"r":r,"rs":r/sd.shift(1)}))
            z24=(c/c.shift(24)-1)/(sd*np.sqrt(24)); vr=v.rolling(24).mean()/v.rolling(480).mean()
            sc=(c/c.shift(240)-1)/(sd*np.sqrt(240))
            fwd=c.shift(-H)/c-1
            idx=np.arange(0,len(b)-H,H)
            g.append(pd.DataFrame({"coin":coin,"w":w,"yr":ts.dt.year.values[idx],"z24":z24.values[idx],"vr":vr.values[idx],"sc":sc.values[idx],"fwd":fwd.values[idx]}))
    hh=pd.concat(hr).dropna()
    hh["late"]=hh.h.isin([21,22])
    def wt(a,b_): 
        return stats.ttest_ind(a,b_,equal_var=False).statistic
    pc=[]
    for coin,x in hh.groupby("coin"):
        pc.append([coin,x[x.late].rs.mean(),x[~x.late].rs.mean(),wt(x[x.late].rs,x[~x.late].rs),
                   x[x.wd==5].rs.mean(),wt(x[x.wd==5].rs,x[x.wd!=5].rs)])
    out["late_hours_sat_by_coin_scaled"]=pd.DataFrame(pc,columns=["coin","late","other","t_late","sat","t_sat"])
    py=[]
    for y,x in hh.groupby("yr"):
        py.append([y,x[x.late].rs.mean(),wt(x[x.late].rs,x[~x.late].rs),x[x.wd==5].rs.mean(),wt(x[x.wd==5].rs,x[x.wd!=5].rs),len(x)])
    out["late_sat_by_year"]=pd.DataFrame(py,columns=["yr","late","t_late","sat","t_sat","n"])
    # late hours by window sign count
    wl=hh.groupby("w").apply(lambda x: x[x.late].rs.mean()-x[~x.late].rs.mean())
    out["late_minus_other_windows_pos_share"]=pd.Series({"pos_share":(wl>0).mean(),"n":len(wl),"t":wl.mean()/(wl.std()/np.sqrt(len(wl)))})
    # hour 21+22 scaled return by hour neighbours, per day-weekday
    x=hh[hh.late]; out["late_by_weekday"]=x.groupby("wd").rs.agg(["mean","size"])
    G=pd.concat(g).dropna(); G["ex"]=G.fwd-G.groupby("coin").fwd.transform("mean")
    G["qz"]=G.groupby("coin").z24.transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    G["qv"]=G.groupby("coin").vr.transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["z24_q_by_coin"]=G.pivot_table(index="coin",columns="qz",values="ex",aggfunc="mean")
    out["vr_q_by_coin"]=G.pivot_table(index="coin",columns="qv",values="ex",aggfunc="mean")
    out["z24_q_by_year"]=G.pivot_table(index="yr",columns="qz",values="ex",aggfunc="mean")
    out["vr_q_by_year"]=G.pivot_table(index="yr",columns="qv",values="ex",aggfunc="mean")
    # vr within sc top half vs bottom half
    G["sch"]=G.sc>G.groupby("coin").sc.transform("median")
    out["vr_q_by_sc_half"]=G.pivot_table(index="sch",columns="qv",values="ex",aggfunc="mean")
    # spearman of z24 and vr with ex per coin
    sp=[]
    for coin,x in G.groupby("coin"):
        sp.append([coin,stats.spearmanr(x.vr,x.ex)[0],stats.spearmanr(x.z24.abs(),x.ex)[0],len(x)])
    out["spearman"]=pd.DataFrame(sp,columns=["coin","vr","absz24","n"])
    return out
