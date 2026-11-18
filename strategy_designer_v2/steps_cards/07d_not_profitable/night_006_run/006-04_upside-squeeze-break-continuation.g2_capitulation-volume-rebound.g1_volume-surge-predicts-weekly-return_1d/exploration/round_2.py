def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            r = b["close"].shift(-1)/b["close"]-1
            a = b["postRebalance_current_allocation"]
            f = b["forecast"]
            r5 = b["close"]/b["close"].shift(5)-1
            r30 = b["close"]/b["close"].shift(30)-1
            fwd7 = b["close"].shift(-7)/b["close"]-1
            rows.append(pd.DataFrame({"coin":c,"w":w,"pos":b.index,"r":r,"a":a,"g":a*r,"f":f,"r5":r5,"r30":r30,"fwd7":fwd7}))
    D = pd.concat(rows, ignore_index=True)
    S = D[D["pos"]%7==0].dropna(subset=["f","fwd7","r30","r5"]).copy()
    S["ex"] = S["fwd7"]-S["coin"].map(S.groupby("coin")["fwd7"].mean())
    # interaction regression: ex on f, z(r30), f*z(r30)
    z30 = (S.r30-S.r30.mean())/S.r30.std()
    X = np.column_stack([np.ones(len(S)), S.f, z30, S.f*z30])
    y = S.ex.values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X@beta
    s2 = res@res/(len(y)-4)
    se = np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["interact_r30"] = pd.DataFrame({"beta":beta,"t":beta/se},index=["const","f","z30","f*z30"])
    z5 = (S.r5-S.r5.mean())/S.r5.std()
    X = np.column_stack([np.ones(len(S)), S.f, z5, S.f*z5])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X@beta; s2 = res@res/(len(y)-4)
    se = np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["interact_r5"] = pd.DataFrame({"beta":beta,"t":beta/se},index=["const","f","z5","f*z5"])
    # slope of f within r30 terciles
    S["r30t"] = pd.qcut(S.r30,3,labels=False)
    rr=[]
    for k,g in S.groupby("r30t"):
        sl = stats.linregress(g.f, g.ex)
        rr.append({"r30t":k,"n":len(g),"slope":sl.slope,"t":sl.slope/sl.stderr,"r30_mean":g.r30.mean()})
    out["slope_by_r30t"] = pd.DataFrame(rr)
    # book drawdowns: pooled daily, chained in window order
    bk=[]
    for c in days:
        for w,d in days[c].items():
            dd=d[["day","book_return","coin_return"]].copy(); dd["w"]=w; dd["coin"]=c; bk.append(dd)
    B=pd.concat(bk).dropna()
    P=B.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    P["wn"]=P.w.str[1:].astype(int); P=P.sort_values(["wn","day"]).reset_index(drop=True)
    eq=(1+P.book_return).cumprod(); dd=eq/eq.cummax()-1
    P["dd"]=dd
    trough=dd.idxmin(); peak=eq[:trough+1].idxmax()
    seg=P.loc[peak+1:trough]
    out["deepest_fall"]=pd.Series({"depth":dd.min(),"days":len(seg),"book_sum":seg.book_return.sum(),"hold_sum":seg.coin_return.sum(),"windows":str(sorted(seg.wn.unique()))})
    # book daily return by sign of position mix: mean allocation per day
    D2=D.copy()
    # losing days decomposition: share of book loss from shorts in up days
    P["hold_up"]=P.coin_return>0
    out["book_by_holdup"]=P.groupby("hold_up").agg(n=("book_return","size"),book=("book_return","mean"),hold=("coin_return","mean"))
    # gain by r30 tercile and side at bar level
    D["r30t"]=pd.qcut(D.r30,3,labels=False); D["side"]=np.sign(D.a)
    out["bar_gain_r30_side"]=D.groupby(["r30t","side"]).agg(n=("g","size"),gain=("g","mean"),r=("r","mean"))
    return out
