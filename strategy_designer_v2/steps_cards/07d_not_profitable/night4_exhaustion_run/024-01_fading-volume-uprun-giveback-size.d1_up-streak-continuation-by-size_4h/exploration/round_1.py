def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    # book daily returns: mean over coins per (window, day)
    rows = []
    for c in coins:
        for w, d in days[c].items():
            t = d[["day","book_return","coin_return"]].copy()
            t["window"] = w; t["coin"] = c
            # mean allocation that day
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            al = b.groupby("day")["postRebalance_current_allocation"].mean()
            t["day"] = pd.to_datetime(t["day"])
            t = t.merge(al.rename("alloc").reset_index(), on="day", how="left")
            rows.append(t)
    D = pd.concat(rows)
    D["wn"] = D["window"].str[1:].astype(int)
    bk = D.groupby(["wn","day"]).agg(book=("book_return","mean"), coin=("coin_return","mean"), alloc=("alloc","mean")).reset_index().sort_values(["wn","day"])
    bk = bk.dropna(subset=["book"])
    eq = (1+bk["book"]).cumprod().values
    peak = np.maximum.accumulate(eq)
    dd = eq/peak-1
    bk["dd"] = dd
    # identify drawdown episodes
    i_trough = int(np.argmin(dd))
    out["deepest dd"] = float(dd.min())
    # episodes: from peak to trough
    ep = []
    peak_i = 0
    cur_min = 0; cur_min_i = 0; in_dd=False
    for i in range(len(eq)):
        if eq[i] >= peak[i] - 1e-15 and dd[i] == 0:
            if in_dd:
                ep.append((peak_i, cur_min_i, cur_min))
            in_dd=False; peak_i=i; cur_min=0
        else:
            in_dd=True
            if dd[i] < cur_min: cur_min=dd[i]; cur_min_i=i
    if in_dd: ep.append((peak_i, cur_min_i, cur_min))
    ep = sorted(ep, key=lambda x: x[2])[:6]
    res=[]
    for p,tr,m in ep:
        seg = bk.iloc[p+1:tr+1]
        pre = bk.iloc[max(0,p-30):p+1]
        res.append({"depth":m,"days":tr-p,"windows":",".join(sorted(set("w"+seg["wn"].astype(str)))),
                    "coin_cum_during":float((1+seg["coin"]).prod()-1),
                    "book_cum_during":float((1+seg["book"]).prod()-1),
                    "mean_alloc_during":float(seg["alloc"].mean()),
                    "coin_cum_30d_before":float((1+pre["coin"]).prod()-1)})
    out["deepest falls"] = pd.DataFrame(res)
    # yearly
    bk["year"]=pd.to_datetime(bk["day"]).dt.year
    out["by year"] = bk.groupby("year").agg(book_mean=("book","mean"),coin_mean=("coin","mean"),alloc=("alloc","mean"),n=("book","size"))
    out["by window"] = bk.groupby("wn").agg(book=("book",lambda x:(1+x).prod()-1),coin=("coin",lambda x:(1+x).prod()-1),alloc=("alloc","mean"))
    # grid cases with features
    cases=[]
    for c in coins:
        allr=[]
        for w,b in bars[c].items():
            cl=b["close"].values
            idx=np.arange(0,len(cl)-18,18)
            allr.append(cl[idx+18]/cl[idx]-1)
        drift=np.concatenate(allr).mean()
        for w,b in bars[c].items():
            cl=b["close"].values; v=b["volume"].values; f=b["forecast"].values
            r1=np.r_[np.nan, cl[1:]/cl[:-1]-1]
            n=len(cl)
            for i in range(0,n-18,18):
                if not (f[i]>0) or i<180: continue
                # streak length
                L=0
                while i-L>=1 and r1[i-L]>0: L+=1
                if L==0: continue
                vs=v[i-L+1:i+1]
                vfade = np.polyfit(np.arange(L),vs,1)[0]/np.mean(v[i-180:i]) if L>=2 else np.nan
                vratio = vs.mean()/np.mean(v[i-180:i])
                cases.append({"coin":c,"f":f[i],"ex":cl[i+18]/cl[i]-1-drift,"tot":cl[i+18]/cl[i]-1,
                              "L":L,"ret30":cl[i]/cl[i-180]-1,"ret7":cl[i]/cl[i-42]-1,
                              "vratio":vratio,"vfade":vfade,"alloc":b["postRebalance_current_allocation"].values[i],
                              "vol30":np.nanstd(r1[i-180:i])})
    C=pd.DataFrame(cases)
    out["n cases"]=len(C)
    def grp(col,q=3):
        g=pd.qcut(C[col].rank(method="first"),q,labels=False)
        return C.groupby(g).agg(mean_col=(col,"mean"),ex=("ex","mean"),tot=("tot","mean"),sd=("ex","std"),n=("ex","size"),worst5=("tot",lambda x:x.quantile(0.05)))
    for col in ["ret30","ret7","vratio","vol30","L","f"]:
        out["by "+col]=grp(col)
    C2=C.dropna(subset=["vfade"])
    g=pd.qcut(C2["vfade"].rank(method="first"),3,labels=False)
    out["by vfade"]=C2.groupby(g).agg(m=("vfade","mean"),ex=("ex","mean"),tot=("tot","mean"),n=("ex","size"))
    return out
