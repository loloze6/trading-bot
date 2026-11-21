def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    res=[]; comp=[]
    for h in [5,10,20]:
        rows=[]
        for coin,wins in data["bars"].items():
            for w,df in wins.items():
                df=df.reset_index(drop=True)
                c=df["close"].astype(float)
                fh=c.shift(-h)/c-1
                g=df.index[df.index%h==0]
                d=pd.DataFrame({"coin":coin,"fc":df.loc[g,"forecast"].values,"regime":df.loc[g,"regime"].values,
                                "mom28":(c/c.shift(28)-1).loc[g].values,"fh":fh.loc[g].values,
                                "year":pd.to_datetime(df.loc[g,"timestamp"]).dt.year.values})
                rows.append(d)
        D=pd.concat(rows,ignore_index=True).dropna(subset=["fh"])
        D["ex"]=D["fh"]-D.groupby("coin")["fh"].transform("mean")
        for reg,sub in [("trending",D[D.regime=="trending"]),("all",D)]:
            s=sub.dropna(subset=["mom28"])
            z=s.groupby("coin")["mom28"].transform(lambda v:(v-v.mean())/v.std())
            lr=stats.linregress(z,s.ex)
            res.append({"h":h,"regime":reg,"n":len(s),"slope_bps_per_sd":lr.slope*1e4,"t":lr.slope/lr.stderr,
                        "spearman":stats.spearmanr(z,s.ex)[0]})
            if reg=="all":
                yr=[]
                for y,ss in s.assign(z=z).groupby("year"):
                    l=stats.linregress(ss.z,ss.ex); yr.append(l.slope/l.stderr)
                res[-1]["years_pos_t"]=int(np.sum(np.array(yr)>0)); res[-1]["years"]=len(yr)
        T=D[(D.regime=="trending")&(D.fc!=0)]
        lr=stats.linregress(T.fc,T.ex)
        comp.append({"h":h,"n":len(T),"t":lr.slope/lr.stderr,"signed_mean":(np.sign(T.fc)*T.ex).mean()})
    out["mom28_by_h"]=pd.DataFrame(res)
    out["composite_by_h"]=pd.DataFrame(comp)
    # sign flips of composite: share of forecast sign changes per 30 bars on trending
    fl=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            f=df["forecast"][df["regime"]=="trending"]
            f=f[f!=0]
            if len(f)>2: fl.append(((np.sign(f).diff()!=0).sum()-1)/len(f))
    out["composite_sign_change_rate"]=pd.Series({"mean":np.mean(fl)})
    return out
