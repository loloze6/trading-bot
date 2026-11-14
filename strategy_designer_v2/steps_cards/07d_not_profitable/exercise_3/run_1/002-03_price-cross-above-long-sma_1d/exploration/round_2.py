def explore(data):
    import pandas as pd, numpy as np
    out = {}
    frames=[]
    for c, ws in data["days"].items():
        for w, d in ws.items():
            x=d[["day","book_return","coin_return"]].copy(); x["coin"]=c; x["wn"]=int(w[1:])
            frames.append(x)
    D=pd.concat(frames)
    P=D.groupby(["wn","day"])[["book_return","coin_return"]].mean().reset_index().sort_values(["wn","day"]).dropna(subset=["book_return"]).reset_index(drop=True)
    eq=(1+P["book_return"]).cumprod(); peak=eq.cummax(); dd=eq/peak-1
    P["dd"]=dd
    # deepest fall episode: from peak to trough
    it=int(dd.idxmin()); ip=int(eq.iloc[:it+1].idxmax())
    out["deepest fall windows (peak,trough)"]=f"{P.loc[ip,'wn']},{P.loc[it,'wn']}, days {it-ip}"
    days_set=set(zip(P.loc[ip+1:it,"wn"],P.loc[ip+1:it,"day"]))
    D["infall"]=[(a,b) in days_set for a,b in zip(D["wn"],D["day"])]
    out["coin contribution in deepest fall"]=D[D["infall"]].groupby("coin").agg(sum_book=("book_return","sum"),sum_coin=("coin_return","sum"),n=("book_return","size")).round(3)
    # bar states, per-coin gain by state at prior close, on long bars
    rows=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl=b["close"]; a=b["postRebalance_current_allocation"]
            r=cl.pct_change()
            t=pd.DataFrame({"g":a*(cl.shift(-1)/cl-1),"a":a,"coin":c,"wn":int(w[1:]),
              "past20":cl/cl.shift(20)-1,"past60":cl/cl.shift(60)-1,
              "dd60":cl/cl.rolling(60,min_periods=10).max()-1,
              "fcchg20":b["forecast"]-b["forecast"].shift(20),
              "dist":b["debug_info.components.above_ma.last_history_value"],
              "dist_chg20":b["debug_info.components.above_ma.last_history_value"]-b["debug_info.components.above_ma.last_history_value"].shift(20)})
            rows.append(t)
    B=pd.concat(rows); L=B[B["a"]>0].dropna()
    for col in ["past60","fcchg20","dist_chg20"]:
        q=pd.qcut(L[col],5,duplicates="drop")
        t=L.groupby(q).agg(n=("g","size"),gain=("g","mean"),sd=("g","std"),worst1pct=("g",lambda s:s.quantile(0.01)),a=("a","mean"))
        t["sh"]=t["gain"]/t["sd"]*np.sqrt(365); out["long by "+col]=t.round(5)
    # where are the worst 5% long-bar losses: state shares
    thr=L["g"].quantile(0.05); W=L[L["g"]<=thr]
    out["worst5% vs all: share past20<0, dd60<-0.1, dist_chg20<0"]=pd.DataFrame({
      "worst":[ (W.past20<0).mean(),(W.dd60<-0.1).mean(),(W.dist_chg20<0).mean(), W.a.mean()],
      "all":[ (L.past20<0).mean(),(L.dd60<-0.1).mean(),(L.dist_chg20<0).mean(), L.a.mean()]},
      index=["past20<0","dd60<-0.1","distchg<0","alloc"]).round(3)
    # what-if: zero gain when past20<0 (daily mean over pooled per-bar gains, rough)
    for name,mask in [("all",L.index==L.index),("past20>=0",L.past20>=0),("dist_chg20>=0",L.dist_chg20>=0)]:
        s=L[mask]["g"]; out["gain sum share "+name]=round(float(s.sum()/L["g"].sum()),3)
    out["loss sum share past20<0"]=round(float(L[L.past20<0]["g"].clip(upper=0).sum()/L["g"].clip(upper=0).sum()),3)
    out["deepest-fall long-bar states"]=B[(B.a>0)].assign(key=list(zip(B[B.a>0].wn,B[B.a>0].wn))).groupby("wn").agg(gain=("g","sum"),past20=("past20","mean"),dd60=("dd60","mean")).loc[[16,17,18]].round(3)
    return out
