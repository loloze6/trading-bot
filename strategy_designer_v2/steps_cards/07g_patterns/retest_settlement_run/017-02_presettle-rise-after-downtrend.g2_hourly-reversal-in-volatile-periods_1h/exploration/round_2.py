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
            d["fwd2"] = d["close"].shift(-2)/d["close"]-1
            d["vol24"] = d["r1"].rolling(24).std()
            d["vratio"] = d["vol24"]/d["vol24"].rolling(720, min_periods=240).mean()
            d["coin"]=c; d["win"]=w; d["pos"]=np.arange(len(d))
            d["hour"]=d["ts"].dt.hour; d["year"]=d["ts"].dt.year; d["month"]=d["ts"].dt.month
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["ex1"] = A["fwd1"]-A.groupby("coin")["fwd1"].transform("mean")
    A["ex2"] = A["fwd2"]-A.groupby("coin")["fwd2"].transform("mean")
    out = {}
    def tt(x):
        x=x.dropna(); return pd.Series({"mean_bp":x.mean()*1e4,"t":x.mean()/(x.std()/np.sqrt(len(x))),"n":len(x)})
    # evening hours 20-21 two-hour excess, at bar hour 20 (non-overlapping: one per day)
    E = A[A["hour"]==20]
    out["eve_by_year"] = E.groupby("year")["ex2"].apply(tt).unstack()
    out["eve_by_coin"] = E.groupby("coin")["ex2"].apply(tt).unstack()
    E2 = E.copy(); E2["summer"]=E2["month"].isin([4,5,6,7,8,9,10])
    out["eve_by_season"] = E2.groupby("summer")["ex2"].apply(tt).unstack()
    H13 = A[A["hour"]==13]
    out["h13_by_year"] = H13.groupby("year")["ex1"].apply(tt).unstack()
    H13 = H13.copy(); H13["summer"]=H13["month"].isin([4,5,6,7,8,9,10])
    out["h13_by_season"] = H13.groupby("summer")["ex1"].apply(tt).unstack()
    # 24h reversal, non-overlapping
    sub=[]
    for (c,w),d in A.groupby(["coin","win"]):
        d=d.reset_index(drop=True); cl=d["close"].values; h=24
        idx=np.arange(h,len(d)-h,h)
        past=cl[idx]/cl[idx-h]-1; fut=cl[idx+h]/cl[idx]-1
        v=d["vol24"].values[idx]*np.sqrt(h)
        sub.append(pd.DataFrame({"z":past/v,"fut":fut,"v":v,"coin":c,"win":w,
                                 "year":d["year"].values[idx],"vr":d["vratio"].values[idx]}))
    S=pd.concat(sub).dropna()
    S["fut_ex"]=S["fut"]-S.groupby("coin")["fut"].transform("mean")
    S["zc"]=S["z"].clip(-6,6)
    S["sig"]=-np.sign(S["z"])*S["fut_ex"]           # faded move, unusual
    S["sigtot"]=-np.sign(S["z"])*S["fut"]
    S["str"]=S["sig"]/S["v"]
    def slo(d):
        sl=stats.linregress(d["zc"],d["fut_ex"]); return pd.Series({"slope_bp":sl.slope*1e4,"t":sl.slope/sl.stderr,"n":len(d)})
    out["rev24_by_coin"]=S.groupby("coin").apply(slo)
    out["rev24_by_year"]=S.groupby("year").apply(slo)
    S["absq"]=pd.qcut(S["z"].abs(),5,labels=False)
    out["rev24_by_absz_quintile"]=S.groupby("absq").agg(fade_ex_bp=("sig",lambda x:x.mean()*1e4),
        fade_tot_bp=("sigtot",lambda x:x.mean()*1e4),strength=("str","mean"),n=("sig","size"),
        t=("sig",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))))
    S["vrq"]=pd.qcut(S["vr"],3,labels=False)
    out["rev24_by_volratio_tercile"]=S.groupby("vrq").apply(slo)
    out["rev24_overall"]=pd.Series({"fade_ex_bp":S["sig"].mean()*1e4,"fade_tot_bp":S["sigtot"].mean()*1e4,
                                    "strength":S["str"].mean(),"usual_move_bp":S.groupby("coin")["fut"].std().mean()*1e4,"n":len(S)})
    return out
