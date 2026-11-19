import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []; samp = []; days_all = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            alloc = b["postRebalance_current_allocation"].fillna(0).values
            r1 = np.r_[c[1:]/c[:-1]-1, np.nan]
            gross = alloc*r1
            pv = b["total_portfolio_value"].values; pr = b["postRebalance_total_value"].values
            fee = (pv-pr)/pv
            past = np.r_[np.full(72,np.nan), c[72:]/c[:-72]-1]
            fwd = np.r_[c[72:]/c[:-72]-1, np.full(72,np.nan)]
            up = b.get("debug_info.components.move_up.post_pipeline_value", pd.Series(np.nan,index=b.index)).fillna(0).values
            dn = b.get("debug_info.components.move_down.post_pipeline_value", pd.Series(np.nan,index=b.index)).fillna(0).values
            side = np.where(up>0,"up",np.where(dn>0,"down","none"))
            rows.append(pd.DataFrame({"coin":coin,"w":w,"gross":gross,"fee":fee,"side":side,"alloc":alloc}))
            idx = np.arange(0,len(b),72)
            samp.append(pd.DataFrame({"coin":coin,"w":w,"fc":b["forecast"].values[idx],"past":past[idx],"fwd":fwd[idx],"side":side[idx]}))
        for w, d in data["days"][coin].items():
            dd = d.copy(); dd["coin"]=coin; dd["w"]=w; days_all.append(dd)
    R = pd.concat(rows); S = pd.concat(samp).dropna(subset=["fwd"]); D = pd.concat(days_all)
    cm = S.groupby("coin")["fwd"].mean(); S["ex"] = S["fwd"]-S["coin"].map(cm)
    out["hourly gross/fee by side (mean*1e4, share)"] = R.groupby("side").agg(gross=("gross",lambda x: x.mean()*1e4), fee=("fee",lambda x: x.mean()*1e4), share=("gross","size"), alloc=("alloc","mean"))
    out["hourly gross/fee total *1e4"] = pd.Series({"gross":R["gross"].mean()*1e4,"fee":R["fee"].mean()*1e4})
    out["by coin gross/fee *1e4"] = R.groupby("coin").agg(gross=("gross",lambda x: x.mean()*1e4), fee=("fee",lambda x: x.mean()*1e4))
    S["q"] = pd.qcut(S["fc"].rank(method="first"),5,labels=False)
    out["fwd excess by forecast quintile and side"] = S.groupby(["side","q"]).agg(n=("ex","size"),ex=("ex","mean"),fc=("fc","mean"),past=("past","mean"))
    S["pq"] = pd.qcut(S["past"].rank(method="first"),10,labels=False)
    g = S.groupby("pq").agg(n=("ex","size"),past=("past","mean"),ex=("ex","mean"),sd=("ex","std"))
    g["t"]=g["ex"]/(g["sd"]/np.sqrt(g["n"])); out["fwd excess by signed past-return decile"]=g
    D["year"]=pd.to_datetime(D["day"]).dt.year
    out["book vs coin daily by year"] = D.groupby("year").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("book_return","size"))
    return out
