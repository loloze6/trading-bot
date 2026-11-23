def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"]).agg(book=("book_return","mean"), hold=("coin_return","mean"), n=("coin","count")).reset_index().sort_values(["wn","day"]).reset_index(drop=True)
    B = B.dropna(subset=["book"]).reset_index(drop=True)
    v = (1+B["book"]).cumprod(); dd = v/v.cummax()-1
    B["dd"]=dd.values; B["v"]=v.values
    pw = B.groupby("wn").agg(book_sum=("book","sum"), hold_sum=("hold","sum"), days=("book","count"),
                             worst_day=("book","min"),
                             maxfall=("book", lambda x: ((1+x).cumprod()/(1+x).cumprod().cummax()-1).min()))
    out["per_window"]=pw.round(4)
    i = B["dd"].idxmin()
    pk = B.loc[:i,"v"].idxmax()
    out["deepest_fall"]=pd.Series({"depth":B.loc[i,"dd"],"trough_window":B.loc[i,"wn"],"peak_window":B.loc[pk,"wn"],"days":i-pk,
                                   "hold_sum_in_fall":B.loc[pk:i,"hold"].sum(),"book_sum_in_fall":B.loc[pk:i,"book"].sum()})
    # top 5 drawdown episodes
    B["ep"]=(B["dd"]==0).cumsum()
    ep=B.groupby("ep").agg(depth=("dd","min"),wn_start=("wn","first"),wn_end=("wn","last"),days=("dd","count"),hold=("hold","sum"))
    out["top_falls"]=ep.sort_values("depth").head(8).round(4).reset_index(drop=True)
    cs=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            ts=pd.to_datetime(b["timestamp"],utc=True)
            dfc=pd.DataFrame({"coin":c,"w":w,"sun":ts.dt.dayofweek==6,"r":r,
                              "vr":r.rolling(20).std()/r.rolling(60).std(),
                              "ret20":cl/cl.shift(20)-1,"ret60":cl/cl.shift(60)-1,"ret5":cl/cl.shift(5)-1,
                              "fwd":cl.shift(-3)/cl-1,"fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],
                              "vol20":r.rolling(20).std(),"vlr":b["volume"]/b["volume"].rolling(20).mean(),
                              "dist":cl/cl.rolling(60).max()-1})
            cs.append(dfc[dfc["sun"]])
    C=pd.concat(cs).dropna(subset=["fwd","ret20"])
    C["wn"]=C["w"].str[1:].astype(int)
    act=C[C["fc"]>0].copy()
    out["n_active"]=len(act)
    def grp(df,col,q=5):
        g=pd.qcut(df[col],q,duplicates="drop")
        t=df.groupby(g,observed=True)["fwd"].agg(["count","mean","std"])
        t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
        t["share_below_-10pct"]=df.groupby(g,observed=True)["fwd"].apply(lambda x:(x<-0.10).mean())
        t["mean_alloc"]=df.groupby(g,observed=True)["alloc"].mean()
        return t.round(4).reset_index(drop=True).assign(lo=[iv.left for iv in g.cat.categories][:len(t)])
    for col in ["ret20","ret60","ret5","vr","r","vol20","fc","vlr","dist"]:
        out["act_by_"+col]=grp(act,col)
    nosig=C[(C["ret20"]<0)&(C["r"]>0)]
    out["nosig_by_ret60"]=grp(nosig,"ret60")
    out["nosig_by_vr"]=grp(nosig,"vr")
    out["nosig_by_dist"]=grp(nosig,"dist")
    out["act_by_window"]=act.groupby("wn")["fwd"].agg(["count","mean","min"]).round(4)
    return out
