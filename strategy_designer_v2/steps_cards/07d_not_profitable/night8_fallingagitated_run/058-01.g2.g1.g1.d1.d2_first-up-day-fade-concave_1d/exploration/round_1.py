def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    # book daily returns: mean over coins per day, within windows
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["w","day"]).agg(book=("book_return","mean"), hold=("coin_return","mean")).reset_index()
    B["wn"] = B["w"].str[1:].astype(int)
    B = B.sort_values(["wn","day"]).dropna(subset=["book"])
    val = (1+B["book"]).cumprod().values
    peak = np.maximum.accumulate(val); ddn = val/peak-1
    B["dd"]=ddn
    # deepest fall: locate trough and its peak
    tr = int(np.argmin(ddn)); pk = int(np.argmax(val[:tr+1]))
    out["deepest_fall"] = pd.Series({"depth":ddn[tr],"days_peak_to_trough":tr-pk,
        "peak_window":B["w"].iloc[pk],"trough_window":B["w"].iloc[tr]})
    # per window stats
    g = B.groupby("w")
    out["by_window"] = pd.DataFrame({"n":g.size(),"book_sum":g["book"].sum(),"hold_sum":g["hold"].sum(),
        "worst_day":g["book"].min(),"best_day":g["book"].max()}).sort_values("book_sum")
    # worst book days
    wd = B.nsmallest(10,"book")[["w","book","hold"]].reset_index(drop=True)
    out["worst10_days"]=wd
    # case-level
    cr=[]
    for c in bars:
        for w, b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"]; r1=cl.shift(-1)/cl-1; r0=cl/cl.shift(1)-1; rp=r0.shift(1)
            r5=cl/cl.shift(5)-1; r3n=cl.shift(-3)/cl-1; r2n=cl.shift(-2)/cl-1
            sd30=r0.rolling(30,min_periods=15).std()
            rng=(b["high"]-b["low"])/cl/sd30
            a=b["postRebalance_current_allocation"]
            m=(a<0)
            x=pd.DataFrame({"coin":c,"w":w,"a":a,"r1":r1,"r2n":r2n,"r3n":r3n,"r0z":r0/sd30,"rpz":rp/sd30,"r5z":r5/sd30,
                            "rng":rng,"close_pos":(cl-b["low"])/(b["high"]-b["low"]),"fc":b["forecast"],
                            "gain":a*r1})[m]
            cr.append(x)
    C=pd.concat(cr).dropna(subset=["r1"])
    C["short_ret"]=-C["r1"]
    out["cases_n"]=len(C)
    def tab(col,q=4):
        cc=C.dropna(subset=[col]).copy()
        cc["bin"]=pd.qcut(cc[col],q,labels=False,duplicates="drop")
        gg=cc.groupby("bin")
        return pd.DataFrame({"lo":gg[col].min(),"hi":gg[col].max(),"n":gg.size(),"short_ret":gg["short_ret"].mean(),
            "t":gg["short_ret"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s)))),"gain_mean":gg["gain"].mean(),
            "gain_min":gg["gain"].min(),"short_2d":-gg["r2n"].mean(),"short_3d":-gg["r3n"].mean()})
    for col in ["rng","r0z","rpz","r5z","close_pos","a"]:
        out["by_"+col]=tab(col)
    # worst 15 case gains
    out["worst_cases"]=C.nsmallest(12,"gain")[["coin","w","a","r1","r0z","rpz","r5z","rng","close_pos"]].reset_index(drop=True)
    # same-day crowding: number of coins shorted that day vs book gain
    C["n_same"]=C.groupby(["w",C.index.map(lambda i:0)])["a"].transform("size")
    out["alloc_abs_desc"]=C["a"].abs().describe()
    return out
