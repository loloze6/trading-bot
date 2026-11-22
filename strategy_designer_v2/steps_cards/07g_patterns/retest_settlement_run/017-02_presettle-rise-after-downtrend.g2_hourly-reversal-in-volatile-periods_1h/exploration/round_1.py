def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            d = df[["timestamp","close","volume"]].copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d["r1"] = d["close"].pct_change()
            d["fwd1"] = d["close"].shift(-1)/d["close"]-1
            d["vol24"] = d["r1"].rolling(24).std()
            d["ret24"] = d["close"]/d["close"].shift(24)-1
            d["fwd2"] = d["close"].shift(-2)/d["close"]-1
            d["past2"] = d["close"]/d["close"].shift(2)-1
            d["relvol"] = d["volume"]/d["volume"].rolling(168).median()
            d["coin"]=c; d["win"]=w; d["pos"]=np.arange(len(d))
            d["hour"]=d["ts"].dt.hour; d["wd"]=d["ts"].dt.weekday
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["dmean"] = A.groupby("coin")["fwd1"].transform("mean")
    A["ex1"] = A["fwd1"]-A["dmean"]
    out = {}
    # hour of day excess next-hour return (fwd from close of hour h -> hour h+1)
    g = A.groupby("hour")["ex1"]
    out["by_hour"] = pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count(),
                                   "relvol":A.groupby("hour")["relvol"].median()})
    g = A.groupby("wd")["ex1"]
    out["by_weekday"] = pd.DataFrame({"mean_bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    # settlement: bar starting 22 closes 23:00; past2 at bar hour 23 (close 00:00) covers 22:00-00:00; fwd2 after
    A["trend_sign"] = np.sign(A["ret24"].shift(2))
    res=[]
    for hset,name in [((23,7,15),"settle"),((3,11,19),"off4"),((19,3,11),"x")][:2]:
        s = A[A["hour"].isin(hset)].dropna(subset=["past2","fwd2","ret24"])
        sp = -s["past2"]*np.sign(s["ret24"]-s["past2"])
        sf = s["fwd2"]*np.sign(s["ret24"]-s["past2"])
        res.append({"set":name,"pre_against_bp":sp.mean()*1e4,"t_pre":stats.ttest_1samp(sp,0).statistic,
                    "post_with_bp":sf.mean()*1e4,"t_post":stats.ttest_1samp(sf,0).statistic,"n":len(s)})
    out["settlement"]=pd.DataFrame(res)
    # reversal at longer horizons, non-overlapping, z by vol24
    res=[]
    for h in [1,4,12,24,72]:
        sub=[]
        for (c,w),d in A.groupby(["coin","win"]):
            d=d.reset_index(drop=True)
            cl=d["close"].values
            idx=np.arange(h,len(d)-h,h)
            past=cl[idx]/cl[idx-h]-1; fut=cl[idx+h]/cl[idx]-1
            v=d["vol24"].values[idx]*np.sqrt(h)
            sub.append(pd.DataFrame({"z":past/v,"fut":fut,"coin":c,"v":v}))
        S=pd.concat(sub).dropna()
        S["fut_ex"]=S["fut"]-S.groupby("coin")["fut"].transform("mean")
        sl=stats.linregress(S["z"].clip(-6,6),S["fut_ex"])
        q=pd.qcut(S["z"],5,labels=False)
        m=S.groupby(q)["fut_ex"].mean()*1e4
        top=S[q==4]["fut_ex"]; bot=S[q==0]["fut_ex"]
        res.append({"h":h,"n":len(S),"slope_t":sl.slope/sl.stderr,"q0_bp":m[0],"q2_bp":m[2],"q4_bp":m[4],
                    "t_q4_minus_q0":stats.ttest_ind(top,bot,equal_var=False).statistic})
    out["reversal_by_h"]=pd.DataFrame(res)
    # by coin per hour slope
    res=[]
    for c,d in A.dropna(subset=["r1","ex1","vol24"]).groupby("coin"):
        z=(d["r1"]/d["vol24"]).clip(-6,6); sl=stats.linregress(z,d["ex1"])
        res.append({"coin":c,"slope_bp":sl.slope*1e4,"t":sl.slope/sl.stderr})
    out["h1_by_coin"]=pd.DataFrame(res)
    return out
