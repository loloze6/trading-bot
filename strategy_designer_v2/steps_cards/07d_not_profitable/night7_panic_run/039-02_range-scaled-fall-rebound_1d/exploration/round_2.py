def explore(data):
    import numpy as np, pandas as pd
    res = {}
    recs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            cl = b["close"]; r1 = cl.pct_change()
            rng = ((b["high"]-b["low"])/cl).rolling(30).mean()
            sc = r1/rng
            fwd = cl.shift(-1)/cl-1
            vol10 = r1.rolling(10).std(); vol60 = r1.rolling(60).std()
            vol30 = r1.rolling(30).std(); vol90 = r1.rolling(90, min_periods=60).std()
            rr = (b["high"]-b["low"])/cl
            rngratio = rr.rolling(5).mean()/rng
            dfb = pd.DataFrame({"coin":c,"wn":int(w[1:]),"ts":b["timestamp"],"r1":r1,"sc":sc,"fwd":fwd,
                "vr":vol10/vol60,"vr30":vol30/vol90,"rngratio":rngratio,
                "r20":cl/cl.shift(20)-1,"alloc":b["postRebalance_current_allocation"],
                "pos":np.arange(len(b))})
            recs.append(dfb)
    X = pd.concat(recs, ignore_index=True)
    mu = X.groupby("coin")["fwd"].mean()
    X["ex"] = X["fwd"]-X["coin"].map(mu)
    X["day"] = pd.to_datetime(X["ts"]).dt.floor("D")
    X["gain"] = (X["alloc"]*X["fwd"]).fillna(0)
    dn = X[(X.r1<0)&X.fwd.notna()&X.sc.notna()]
    thr = (-dn.sc).quantile(0.6)
    def book(mask, name):
        g = X["gain"].where(mask, 0.0)
        # turnover cost approx: change in alloc * 0.0019/2 per side
        a = X["alloc"].where(mask,0.0).fillna(0)
        da = a.groupby([X.coin,X.wn]).diff().abs().fillna(a.abs())
        net = g - da*0.00095
        B = pd.DataFrame({"wn":X.wn,"day":X.day,"net":net,"hold":X.fwd}).groupby(["wn","day"]).mean().sort_index()
        r = B["net"]
        v=(1+r).cumprod(); mdd=(v/v.cummax()-1).min()
        yr = v.iloc[-1]**(365/len(r))-1
        pw = B.groupby("wn")["net"].sum()
        return pd.Series({"mean":r.mean(),"sharpe":r.mean()/r.std()*np.sqrt(365),"yearly":yr,"mdd":mdd,
            "calmar":yr/abs(mdd),"worst_win":pw.min(),"win9":pw.get(9,np.nan),"in_share":(mask&(X.alloc.abs()>0)).mean()})
    base = pd.Series(True,index=X.index)
    out = {"all": book(base,"all"),
           "vr_gt1": book(X.vr>1,"vr"),
           "vr30_gt1": book(X.vr30>1,""),
           "rngratio_gt1": book(X.rngratio>1,""),
           "top40": book((-X.sc)>=thr,""),
           "top40_vr_gt1": book(((-X.sc)>=thr)&(X.vr>1),""),
           "excl_r20_m20_m10": book(~X.r20.between(-0.2,-0.1),"")}
    res["books_approx_after_cost"] = pd.DataFrame(out).T
    # condition alone check: bars with vr>1 but not down day / down but small; vs both
    def s(df): 
        return pd.Series({"n":len(df),"ex":df.ex.mean(),"t":df.ex.mean()/df.ex.std()*np.sqrt(len(df))})
    Y = X.dropna(subset=["fwd","sc","vr"])
    big = (Y.r1<0)&((-Y.sc)>=thr)
    res["cond_check_vr"] = pd.DataFrame({
        "vr>1 & bigfall": s(Y[(Y.vr>1)&big]),
        "vr>1 & no down": s(Y[(Y.vr>1)&(Y.r1>=0)]),
        "vr>1 & small down": s(Y[(Y.vr>1)&(Y.r1<0)&~big]),
        "vr<=1 & bigfall": s(Y[(Y.vr<=1)&big]),
        "vr<=1 & any": s(Y[(Y.vr<=1)])}).T
    # grading within vr>1: slope by scaled-fall quintile
    d2 = Y[(Y.r1<0)].copy(); d2["q"]=pd.qcut(-d2.sc,5,labels=False)
    d2["hv"]=d2.vr>1
    res["ex_by_q_and_hv"] = d2.groupby(["hv","q"]).ex.agg(["size","mean"]).unstack(0)
    # worst episode w9: gain by vr state
    w9 = X[X.wn.isin([8,9])]
    res["w8_9_gain_by_vr"] = w9.groupby(w9.vr>1)["gain"].agg(["sum","count"])
    res["w8_9_gain_by_q"] = w9[w9.r1<0].assign(big=lambda d:(-d.sc)>=thr).groupby("big")["gain"].agg(["sum","count"])
    return res
