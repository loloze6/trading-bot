def explore(data):
    import pandas as pd, numpy as np
    out={}
    # coin mean daily return over all windows, per coin
    cm1={}
    for c in data["bars"]:
        r=[]
        for w,b in data["bars"][c].items():
            cl=b["close"].values; r+=list(cl[1:]/cl[:-1]-1)
        cm1[c]=np.mean(r)
    rows=[]; held=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            cl=b["close"].values; f=b["forecast"].fillna(0).values
            al=b["postRebalance_current_allocation"].fillna(0).values
            n=len(cl)
            # position gain per bar
            for i in range(n-1):
                if abs(al[i])>1e-9:
                    held.append({"coin":c,"gain":al[i]*(cl[i+1]/cl[i]-1),"mkt":al[i]*cm1[c],"days_after_signal":0 if f[i]<0 else 1})
            last=-99
            for i in range(n):
                if f[i]<0 and i-last>=5:
                    last=i
                    d={"coin":c,"f":f[i]}
                    for k in range(1,11):
                        d[f"d{k}"]=cl[i+k]/cl[i+k-1]-1-cm1[c] if i+k<n else np.nan
                    d["x2to5"]=cl[i+5]/cl[i+1]-1-4*cm1[c] if i+5<n else np.nan
                    d["x1to5"]=cl[i+5]/cl[i+1]-1-4*cm1[c] if i+5<n else np.nan
                    d["x2to5b"]=cl[i+5]/cl[i+2]-1-3*cm1[c] if i+5<n else np.nan
                    d["x1to10"]=cl[i+10]/cl[i+1]-1-9*cm1[c] if i+10<n else np.nan
                    rows.append(d)
    ev=pd.DataFrame(rows)
    def t(x):
        x=x.dropna(); return pd.Series({"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))),"n":len(x)})
    out["daily_excess_path"]=pd.DataFrame({k:t(ev[k]) for k in [f"d{k}" for k in range(1,11)]}).T
    out["from_day1_close"]=pd.DataFrame({k:t(ev[k]) for k in ["x1to5","x2to5b","x1to10"]}).T
    ev["fq"]=pd.qcut(ev["f"].rank(method="first"),2,labels=["strong","weak"])
    out["path_by_forecast"]=ev.groupby("fq")[["d1","d2","d3","d4","d5","x1to5"]].mean()
    h=pd.DataFrame(held)
    out["held_bars"]=h.groupby("days_after_signal").agg(n=("gain","size"),gain=("gain","mean"),mkt=("gain",lambda s: 0)).assign(mkt=h.groupby("days_after_signal")["mkt"].mean())
    out["held_total"]=pd.Series({"n":len(h),"mean_gain":h["gain"].mean(),"mean_mkt_part":h["mkt"].mean(),"win":(h["gain"]>0).mean()})
    return out
