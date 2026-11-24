def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    drift={}; usual={}
    for coin,wins in data["bars"].items():
        r2=[]
        for w,b in wins.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-2,2)
            r2+=list(c[idx+2]/c[idx]-1)
        drift[coin]=float(np.mean(r2)); usual[coin]=float(np.std(r2,ddof=1))
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"])
            c=b["close"].astype(float)
            ret=c.pct_change()
            vr=ret.rolling(20).std()/ret.rolling(60).std()
            r14=c/c.shift(14)-1
            vol20=ret.rolling(20).std()
            fwd=c.shift(-2)/c-1
            f1=c.shift(-1)/c-1
            f2=c.shift(-2)/c.shift(-1)-1
            pos=np.arange(len(b))
            df=pd.DataFrame({"coin":coin,"day":ts.dt.floor("D").values,"wd":ts.dt.weekday.values,
                             "fc":b["forecast"].values,"vr":vr.values,"r14":r14.values,
                             "z14":(r14/(vol20*np.sqrt(14))).values,
                             "fwd":fwd.values,"f1":f1.values,"f2":f2.values,"grid":(pos%2==0)})
            df=df.dropna(subset=["fwd","r14","vr"])
            df["unus"]=df.fwd-drift[coin]
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    def slope(x,col):
        x=x.dropna(subset=[col,"unus"])
        xs=x[col]-x[col].mean(); y=x.unus-x.unus.mean()
        bta=(xs*y).sum()/(xs**2).sum()
        e=y-bta*xs
        s=(xs*e).groupby(x.day).sum()
        se=np.sqrt((s**2).sum())/(xs**2).sum()
        rho,p=stats.spearmanr(x[col],x.unus)
        hi=x[x[col]>=x[col].median()].unus; lo=x[x[col]<x[col].median()].unus
        tw=stats.ttest_ind(hi,lo,equal_var=False).statistic
        return pd.Series({"n":float(len(x)),"days":float(x.day.nunique()),"slope_t":bta/se,"spearman":rho,
                          "hi_minus_lo":hi.mean()-lo.mean(),"welch_t":tw})
    out={}
    fri=d[d.wd==4]
    out["fri_all_r14"]=slope(fri,"r14")
    out["fri_all_z14"]=slope(fri,"z14")
    out["fri_volhi_z14"]=slope(fri[fri.vr>1],"z14")
    out["fri_vollo_z14"]=slope(fri[fri.vr<=1],"z14")
    out["fri_up_z14"]=slope(fri[fri.r14>0],"z14")
    out["fri_cases_fc"]=slope(fri[fri.fc>=2],"fc")
    out["fri_cases_z14"]=slope(fri[fri.fc>=2],"z14")
    g=d[d.grid]
    out["grid_by_wd_z14"]=g.groupby("wd").apply(lambda x: slope(x,"z14"))
    out["grid_all_z14"]=slope(g,"z14")
    c=fri[fri.fc>=2]
    out["cases_sat_sun_split"]=pd.Series({"sat_mean":c.f1.mean(),"sun_mean":c.f2.mean(),
        "sat_t":stats.ttest_1samp(c.f1,0).statistic,"sun_t":stats.ttest_1samp(c.f2,0).statistic})
    out["corr_fc_z14_cases"]=float(np.corrcoef(c.fc,c.z14)[0,1])
    return out
