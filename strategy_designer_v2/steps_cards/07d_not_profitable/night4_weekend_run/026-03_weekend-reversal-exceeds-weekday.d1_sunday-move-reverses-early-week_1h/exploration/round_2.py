def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].values
            n = len(b)
            for i in np.where((ts.dt.weekday == 6) & (ts.dt.hour == 23))[0]:
                if i - 72 < 0 or i + 48 >= n: continue
                f = b["forecast"].iloc[i]
                if not np.isfinite(f) or f == 0: continue
                r24 = c[i] / c[i-24] - 1
                sat = c[i-24] / c[i-48] - 1
                fri = c[i-48] / c[i-72] - 1
                fwd = c[i+48] / c[i] - 1
                vol = np.nanstd(np.diff(np.log(c[max(0,i-720):i+1])))*np.sqrt(24)
                al = b["postRebalance_current_allocation"].iloc[i]
                rows.append(dict(coin=coin, w=w, r24=r24, sat=sat, fri=fri, fwd=fwd, vol=vol, al=al,
                                 gain=-np.sign(r24)*fwd, pnl=al*fwd))
    d = pd.DataFrame(rows)
    tt = lambda x: x.mean()/x.std()*np.sqrt(len(x))
    # regressions of fwd on sunday move, split by saturday agreement
    def reg(sub, xcol):
        r = stats.linregress(sub[xcol], sub["fwd"]); return pd.Series({"n":len(sub),"slope":r.slope,"t":r.slope/r.stderr})
    d["agree"] = np.sign(d["sat"])==np.sign(d["r24"])
    out["slope_r24_by_satagree"] = d.groupby("agree").apply(lambda s: reg(s,"r24"))
    d["net"] = d["r24"]+d["sat"]
    d["sundiff"] = d["r24"]-d["sat"]
    out["slope_on_weekend48"] = reg(d,"net")
    out["slope_on_sun_minus_sat"] = reg(d,"sundiff")
    out["slope_on_sat"] = reg(d,"sat")
    # multiple regression fwd on r24 and sat
    X = np.column_stack([np.ones(len(d)), d["r24"], d["sat"]])
    beta, *_ = np.linalg.lstsq(X, d["fwd"].values, rcond=None)
    res = d["fwd"].values - X@beta
    s2 = res.var(ddof=3); cov = s2*np.linalg.inv(X.T@X)
    out["multi_r24_sat"] = pd.Series({"b_r24":beta[1],"t_r24":beta[1]/np.sqrt(cov[1,1]),
                                      "b_sat":beta[2],"t_sat":beta[2]/np.sqrt(cov[2,2])})
    # standardised by vol
    d["z"] = d["r24"]/d["vol"]
    d["zq"] = pd.qcut(d["z"].abs(),5,labels=False)
    out["gain_by_zq"] = d.groupby("zq").agg(n=("gain","size"),gain=("gain","mean"),t=("gain",tt),
                                             pnl=("pnl","mean"),alabs=("al",lambda x:x.abs().mean()))
    d["sq"] = pd.qcut(d["sundiff"]*-np.sign(d["r24"])*-1,5,labels=False)
    out["gain_by_sundiff_q_dirSun"] = d.groupby("sq").agg(n=("gain","size"),gain=("gain","mean"),t=("gain",tt))
    out["pnl_by_agree"] = d.groupby("agree").agg(pnl=("pnl","mean"),pnl_sum=("pnl","sum"))
    # drawdowns of the book chain
    days=[]
    for coin, ws in data["days"].items():
        for w, dd in ws.items():
            x=dd[["day","book_return"]].copy(); x["w"]=w; days.append(x)
    D=pd.concat(days).dropna()
    B=D.groupby(["w","day"])["book_return"].mean().reset_index()
    B["wn"]=B["w"].str[1:].astype(int); B=B.sort_values(["wn","day"]).reset_index(drop=True)
    eq=(1+B["book_return"]).cumprod(); dd_=eq/eq.cummax()-1
    out["maxdd"]=float(dd_.min())
    B["dd"]=dd_
    out["dd_worst_window"]=B.groupby("w")["dd"].min().sort_values().head(6)
    out["worst_days_weekday"]=B.nsmallest(40,"book_return").assign(wd=pd.to_datetime(B.nsmallest(40,"book_return")["day"]).dt.weekday)["wd"].value_counts()
    return out
