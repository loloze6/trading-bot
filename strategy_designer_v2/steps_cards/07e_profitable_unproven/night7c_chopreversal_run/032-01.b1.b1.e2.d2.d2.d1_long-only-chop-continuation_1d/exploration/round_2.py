def explore(data):
    import numpy as np, pandas as pd
    bars, days, trades = data["bars"], data["days"], data["trades"]
    out = {}
    recs = []
    for c in bars:
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            cl = b["close"]
            er = (cl - cl.shift(30)).abs() / cl.diff().abs().rolling(30).sum()
            r7 = cl/cl.shift(7)-1; r30 = cl/cl.shift(30)-1
            vol = cl.pct_change().rolling(30).std()
            z7 = r7/(vol*np.sqrt(7))
            day = pd.to_datetime(b["timestamp"]).dt.floor("D")
            for h in [3,7,14]:
                fwd = cl.shift(-h)/cl-1
                idx = np.arange(0, len(b), h)
                recs.append(pd.DataFrame({"h":h,"fwd":fwd.iloc[idx].values,"fc":b["forecast"].iloc[idx].values,
                    "er":er.iloc[idx].values,"r7":r7.iloc[idx].values,"r30":r30.iloc[idx].values,
                    "z7":z7.iloc[idx].values,"vol":vol.iloc[idx].values,"day":day.iloc[idx].values,"coin":c,"w":w}))
    R = pd.concat(recs).dropna(subset=["fwd","er","z7"])
    R["mu"] = R.groupby(["h","coin"])["fwd"].transform("mean")
    R["u"] = R.fwd - R.mu
    def ct(x, d):
        s = pd.DataFrame({"u":x,"d":d}).groupby("d")["u"].sum()
        D=len(s); n=len(x)
        if D<3: return np.nan
        se = np.sqrt((s**2).sum()*D/(D-1))/n
        return x.mean()/se
    def summ(df):
        return pd.Series({"mean":df.u.mean(),"n":len(df),"days":df.day.nunique(),"t_day":ct(df.u.values,df.day.values)})
    # signed z7 momentum in chop, both sides, graded by z7 quintile, h=7
    for h in [7,14]:
        a = R[(R.h==h)&(R.er<=0.3)].copy()
        a["q"]=pd.qcut(a.z7,5,labels=False)
        out[f"chop_er30_h{h}_by_z7_quintile"]=a.groupby("q").apply(summ)
        a["s"]=np.sign(a.z7)*a.u
        out[f"chop_h{h}_signed_momentum"]=pd.Series({"mean":a.s.mean(),"t_day":ct(a.s.values,a.day.values),"n":len(a)})
    # ER tercile x z7 tercile h=7, signed momentum
    a = R[R.h==7].copy()
    a["qer"]=pd.qcut(a.er,3,labels=["chop","mid","eff"])
    a["s"]=np.sign(a.z7)*a.u
    out["h7_signed_mom_by_er"]=a.groupby("qer").apply(lambda d: pd.Series({"mean":d.s.mean(),"t_day":ct(d.s.values,d.day.values),"n":len(d)}))
    # r30 sign within chop up7
    c7 = a[(a.er<=0.3)&(a.r7>0)]
    out["chop_up7_by_r30sign"]=c7.groupby(c7.r30>0).apply(summ)
    c7d = a[(a.er<=0.3)&(a.r7<0)]
    out["chop_down7_by_r30sign"]=c7d.groupby(c7d.r30>0).apply(summ)
    # by window, chop signed momentum
    out["chop_h7_signed_mom_by_window"]=a[a.er<=0.3].groupby("w")["s"].agg(["mean","count"])
    # vol level: within chop, signed momentum by vol tercile
    cc = a[a.er<=0.3].copy(); cc["qv"]=pd.qcut(cc.vol,3,labels=["lowvol","midvol","hivol"])
    out["chop_h7_signed_mom_by_vol"]=cc.groupby("qv").apply(lambda d: pd.Series({"mean":d.s.mean(),"t_day":ct(d.s.values,d.day.values),"n":len(d)}))
    # trades: profit without top 10, by year
    T = pd.concat([trades[c][w].assign(coin=c,w=w) for c in trades for w in trades[c] if len(trades[c][w])])
    p = T.net_profit_loss_percent.sort_values(ascending=False)
    out["trades_trim"]=pd.Series({"mean_all":p.mean(),"mean_wo_top10":p.iloc[10:].mean(),"mean_wo_top20":p.iloc[20:].mean()})
    # book daily: share of window with positive book mean
    D = pd.concat([days[c][w].assign(coin=c,w=w) for c in days for w in days[c]]).dropna(subset=["book_return"])
    bk = D.groupby(["w","day"])["book_return"].mean()
    out["book_by_window"]=bk.groupby(level=0).agg(["mean","std","count"])
    return out
