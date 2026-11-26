import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    # book daily returns
    rows = []
    for c in coins:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["w"]=w; dd["coin"]=c
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"]).agg(br=("book_return","mean"), cr=("coin_return","mean")).reset_index().sort_values(["wn","day"])
    B = B.dropna(subset=["br"])
    val = (1+B["br"]).cumprod().values
    peak = np.maximum.accumulate(val); dd = val/peak-1
    B["dd"] = dd; B["val"]=val
    # find top drawdown episodes
    eps=[]; i=0; n=len(B)
    trough_idx = []
    in_dd=False
    start=None
    for k in range(n):
        if dd[k]<0 and not in_dd: in_dd=True; start=k-1 if k>0 else 0
        if dd[k]==0 and in_dd:
            seg = dd[start:k]; t = start+int(np.argmin(seg)); eps.append((start,t,k,dd[t])); in_dd=False
    if in_dd:
        seg=dd[start:]; t=start+int(np.argmin(seg)); eps.append((start,t,n-1,dd[t]))
    eps = sorted(eps,key=lambda e:e[3])[:6]
    B["year"]=pd.to_datetime(B["day"]).dt.year
    ep_tab=[]
    for (s,t,e,m) in eps:
        seg = B.iloc[s:t+1]
        ep_tab.append({"depth":m,"days_to_trough":t-s,"days_recover":e-t,"window":"w%d"%B.iloc[t]["wn"],"year":B.iloc[t]["year"],
                       "coin_cum_during":(1+seg["cr"]).prod()-1})
    out["deepest_falls"]=pd.DataFrame(ep_tab)
    # case-level: Thursday-close bars
    cases=[]
    for c in coins:
        for w, b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"].values
            ts=pd.to_datetime(b["timestamp"])
            r1 = pd.Series(cl).pct_change()
            vol20 = r1.rolling(20).std().values
            r14 = pd.Series(cl).pct_change(14).values
            r60 = pd.Series(cl).pct_change(60).values
            hi60 = pd.Series(cl).rolling(60,min_periods=30).max().values
            lo60 = pd.Series(cl).rolling(60,min_periods=30).min().values
            alloc=b["postRebalance_current_allocation"].values
            for t in range(len(b)-2):
                if b.loc[t,"regime"]!="trending": continue
                fwd = cl[t+2]/cl[t]-1
                cases.append({"coin":c,"wn":int(w[1:]),"year":ts[t].year,"fc":b.loc[t,"forecast"],"alloc":alloc[t],
                              "fwd":fwd,"r14":r14[t],"r60":r60[t],"vol20":vol20[t],
                              "pos60":(cl[t]-lo60[t])/(hi60[t]-lo60[t]) if hi60[t]>lo60[t] else np.nan,
                              "pnl":alloc[t]*fwd})
    C=pd.DataFrame(cases)
    C["side"]=np.where(C["fc"]>0,"long",np.where(C["fc"]<0,"short","flat"))
    g=C.groupby("side").agg(n=("fwd","size"),mean_fwd=("fwd","mean"),mean_pnl=("pnl","mean"),sum_pnl=("pnl","sum"),mean_absalloc=("alloc",lambda x: x.abs().mean()))
    out["by_side"]=g
    C["fq"]=pd.qcut(C["fc"],5,labels=False,duplicates="drop")
    out["by_forecast_q"]=C.groupby("fq").agg(n=("fwd","size"),fc=("fc","mean"),fwd=("fwd","mean"),pnl=("pnl","mean"),sd_pnl=("pnl","std"))
    C["vq"]=C.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x,3,labels=False,duplicates="drop"))
    C["dirfwd"]=np.sign(C["fc"])*C["fwd"]
    out["by_vol_tercile"]=C.groupby(["vq","side"]).agg(n=("fwd","size"),dirfwd=("dirfwd","mean"),pnl=("pnl","mean"),sd_pnl=("pnl","std"))
    C["trend60"]=np.where(C["r60"]>0,"up60","down60")
    out["by_trend60_side"]=C.groupby(["trend60","side"]).agg(n=("fwd","size"),dirfwd=("dirfwd","mean"),pnl=("pnl","mean"),sd_pnl=("pnl","std"),worst=("pnl","min"))
    out["by_year"]=C.groupby("year").agg(n=("fwd","size"),dirfwd=("dirfwd","mean"),pnl=("pnl","mean"))
    # drawdown attribution: days in deepest 3 falls, side held
    deep_days=set()
    for (s,t,e,m) in eps[:3]:
        for k in range(s+1,t+1): deep_days.add((B.iloc[k]["wn"],B.iloc[k]["day"]))
    rows=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.copy(); b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["wn"]=int(w[1:]); rows.append(b[["wn","day","postRebalance_current_allocation","previous_allocation","close"]].assign(coin=c))
    A=pd.concat(rows)
    dd_day_type = type(B["day"].iloc[0])
    A["day"]=A["day"].astype(B["day"].dtype) if B["day"].dtype!=object else A["day"].dt.strftime("%Y-%m-%d")
    A["in_fall"]=[ (w,d) in deep_days for w,d in zip(A["wn"],A["day"])]
    A["side_prev"]=np.sign(A["previous_allocation"])
    out["fall_days_held_side"]=A[A["in_fall"]].groupby("side_prev").size()
    out["n_fall_days"]=len(deep_days)
    out["C_overall"]=pd.Series({"n":len(C),"pnl_mean":C["pnl"].mean(),"pnl_t":stats.ttest_1samp(C["pnl"].dropna(),0).statistic,"dirfwd":C["dirfwd"].mean()})
    return out
