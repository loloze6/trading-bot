def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    wins = sorted({w for c in bars for w in bars[c]}, key=lambda s:int(s[1:]))
    # book daily
    dr = []
    for w in wins:
        frames = []
        for c in days:
            if w in days[c]:
                d = days[c][w][["day","book_return","coin_return"]].copy(); d["coin"]=c; frames.append(d)
        f = pd.concat(frames)
        g = f.groupby("day")[["book_return","coin_return"]].mean().reset_index()
        g["w"]=w; dr.append(g)
    dr = pd.concat(dr, ignore_index=True).dropna()
    v = (1+dr.book_return).cumprod(); peak=v.cummax(); dd=v/peak-1
    dr["dd"]=dd.values
    # episodes: find deepest troughs
    eps=[]; d2=dd.copy()
    used=np.zeros(len(dd),bool)
    ddv=dd.values; vv=v.values
    for k in range(4):
        m=np.where(used,0,ddv); i=int(np.argmin(m))
        if m[i]>=0: break
        j=i
        while j>0 and ddv[j-1]<0: j-=1
        s=j-1 if j>0 else 0
        e=i
        while e+1<len(ddv) and ddv[e+1]<0: e+=1
        used[s:e+1]=True
        eps.append({"depth":ddv[i],"start_w":dr.w.iloc[s],"trough_w":dr.w.iloc[i],"days_to_trough":i-s,
                    "coin_ret_during":float((1+dr.coin_return.iloc[s+1:i+1]).prod()-1),
                    "book_ret_during":float((1+dr.book_return.iloc[s+1:i+1]).prod()-1)})
    eps=pd.DataFrame(eps)
    # bar level
    rows=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b.close; r=np.log(cl).diff()
            pos=b.postRebalance_current_allocation.fillna(0)
            nxt=cl.shift(-1)/cl-1
            r7=cl/cl.shift(7)-1; r30=cl/cl.shift(30)-1
            er=(np.log(cl)-np.log(cl.shift(30))).abs()/r.abs().rolling(30).sum()
            vol=r.rolling(30).std()
            f7=cl.shift(-7)/cl-1
            df=pd.DataFrame({"coin":c,"w":w,"pos":pos,"gain":pos*nxt,"fc":b.forecast,"r7":r7,"r30":r30,"er":er,
                             "vol":vol,"f7":f7,"regime":b.regime,"i":np.arange(len(b)),"ttrend":(r7.abs()/(vol*np.sqrt(7)))})
            rows.append(df)
    B=pd.concat(rows,ignore_index=True)
    B["side"]=np.sign(B.pos)
    bys=B.groupby("side").gain.agg(["count","mean","sum"])
    byw=B.groupby("w").gain.agg(["mean","sum"])
    inpos=B[B.pos!=0].copy()
    inpos["volq"]=pd.qcut(inpos.vol,3,labels=["lo","mid","hi"])
    inpos["erq"]=pd.qcut(inpos.er,3,labels=["lo","mid","hi"])
    inpos["r30q"]=pd.qcut(inpos.r30.abs(),3,labels=["lo","mid","hi"])
    inpos["fcq"]=pd.qcut(inpos.fc.abs().rank(method="first"),3,labels=["lo","mid","hi"])
    res={"episodes":eps,"by_side":bys,"by_window":byw}
    for k in ["volq","erq","r30q","fcq"]:
        t=inpos.groupby(k).gain.agg(["count","mean","std","sum"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
        res["gain_by_"+k]=t
    res["side_x_volq"]=inpos.groupby(["side","volq"]).gain.agg(["count","mean","sum"])
    # gain in deepest episode windows by side
    res["eps_windows_side"]=B[B.w.isin(eps.trough_w)].groupby(["w","side"]).gain.agg(["count","sum"])
    res["mean_abs_pos"]=float(inpos.pos.abs().mean())
    return res
