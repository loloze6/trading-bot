def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    drift = {}
    rows = []
    for coin, wins in bars.items():
        for h in [3,5]:
            rs=[]
            for w,df in wins.items():
                c=df["close"].values
                for i in range(0,len(c)-h,h):
                    rs.append(c[i+h]/c[i]-1)
            drift[(coin,h)]=(np.mean(rs),np.std(rs))
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            o,hi,lo,c=df["open"],df["high"],df["low"],df["close"]
            rng=hi-lo
            rr=rng/rng.rolling(20).mean()
            fl=1-(c-o).abs()/rng.replace(0,np.nan)
            pe5=c/c.shift(5)-1
            ts=pd.to_datetime(df["timestamp"])
            cv=c.values
            for i in range(len(df)):
                if np.isnan(rr[i]) or np.isnan(pe5[i]) or np.isnan(fl[i]): continue
                if pe5[i]<=0: continue
                if rr[i]>=1.5 and fl[i]>=0.9: grp="wide_flat"
                elif rr[i]<1.0 and fl[i]>=0.9: grp="narrow_flat"
                elif rr[i]>=1.5: grp="wide_body"
                else: grp="other_uprun"
                r={"coin":coin,"win":w,"grp":grp,"pe5":pe5[i],"rr":rr[i],"year":ts[i].year,
                   "day":ts[i].floor("D"),"cell3":i//3,"cell5":i//5}
                for h in [3,5]:
                    if i+h<len(df):
                        ret=cv[i+h]/cv[i]-1; d,s=drift[(coin,h)]
                        r[f"unu{h}"]=ret-d; r[f"str{h}"]=(ret-d)/s
                rows.append(r)
    X=pd.DataFrame(rows)
    def ct(x,days):
        x=np.asarray(x,float);m=x.mean();e=x-m
        S=pd.Series(e).groupby(np.asarray(days)).sum()
        se=np.sqrt((S**2).sum())/len(x)
        return m,(m/se if se>0 else np.nan),len(x),pd.Series(days).nunique()
    out={}
    res=[]
    for h in [3,5]:
        Y=X.groupby(["coin","win",f"cell{h}","grp"]).first().reset_index().dropna(subset=[f"unu{h}"])
        for g,s in Y.groupby("grp"):
            m,t,n,nd=ct(s[f"unu{h}"],s["day"])
            res.append({"h":h,"grp":g,"unu":m,"t":t,"n":n,"days":nd,"strength":s[f"str{h}"].mean()})
        W=Y[Y.grp=="wide_flat"]; O=Y[Y.grp=="other_uprun"]
        tt=__import__("scipy").stats.ttest_ind(W[f"unu{h}"],O[f"unu{h}"],equal_var=False)
        out[f"wide_flat_minus_other_h{h}"]=pd.Series({"diff":W[f"unu{h}"].mean()-O[f"unu{h}"].mean(),"welch_t":tt.statistic})
        W2=W[W.year!=2021]; m,t,n,nd=ct(W2[f"unu{h}"],W2["day"])
        out[f"wide_flat_ex2021_h{h}"]=pd.Series({"unu":m,"t":t,"n":n})
        W3=W[W.coin!="ETHUSD"]; m,t,n,nd=ct(W3[f"unu{h}"],W3["day"])
        out[f"wide_flat_exETH_h{h}"]=pd.Series({"unu":m,"t":t,"n":n})
        # grading by pe5 within wide_flat and other
        g=[]
        for grp in ["wide_flat","other_uprun"]:
            s=Y[Y.grp==grp].copy(); s["q"]=pd.qcut(s.pe5,3,labels=False)
            for q,ss in s.groupby("q"):
                m,t,n,nd=ct(ss[f"unu{h}"],ss["day"]); g.append({"grp":grp,"pe5_terc":q,"unu":m,"t":t,"n":n})
        out[f"pe5_grading_h{h}"]=pd.DataFrame(g)
        out[f"spearman_wideflat_pe5_unu_h{h}"]=W[["pe5",f"unu{h}"]].corr(method="spearman").iloc[0,1]
    out["by_group"]=pd.DataFrame(res)
    return out
