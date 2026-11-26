def explore(data):
    import numpy as np, pandas as pd
    rows=[]; dayrows=[]; allret=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; r=c.pct_change(); allret.append(r.dropna())
            sd30=r.rolling(30,min_periods=20).std()
            b["ret1"]=r; b["sd30"]=sd30
            b["gb"]=(b["high"]-c)/c/sd30
            b["r3s"]=(c/c.shift(3)-1)/(sd30*np.sqrt(3))
            b["r10s"]=(c/c.shift(10)-1)/(sd30*np.sqrt(10))
            b["uplow20"]=(c/c.rolling(20,min_periods=10).min()-1)/sd30
            b["ret60"]=c/c.shift(60)-1
            b["f1"]=c.shift(-1)/c-1
            b["pos"]=b["postRebalance_current_allocation"]
            b["gain"]=b["pos"]*b["f1"]
            b["coin"]=coin; b["w"]=w
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
        for w,d in data["days"][coin].items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; dayrows.append(d)
    B=pd.concat(rows,ignore_index=True)
    drift=pd.concat(allret).mean()
    B["u1"]=-(B["f1"]-drift)
    prof=B[B["regime"].isin(["trending","unknown"])].copy()
    cases=B[(B["regime"]=="trending")&(B["forecast"]<0)].copy()
    held=B[B["pos"].abs()>0].dropna(subset=["gain"]).copy()
    out={}
    def grp(df,col,val,q=4):
        df=df.dropna(subset=[col,val]).copy()
        df["q"]=pd.qcut(df[col].rank(method="first"),q,labels=False)
        g=df.groupby("q")[val]
        return pd.DataFrame({"lo":df.groupby("q")[col].min(),"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size())),"sum":g.sum()})
    for col in ["r3s","r10s","uplow20","ret60"]:
        out["cases_u1_by_"+col]=grp(cases,col,"u1")
        out["held_gain_by_"+col]=grp(held,col,"gain")
    # condition alone: in-profile non-signal bars with r3s<-0.25 vs signal bars with it
    nos=prof[~prof.index.isin(cases.index)]
    out["cond_r3s_neg"]=pd.DataFrame({
        "both":[cases.loc[cases.r3s<-0.25,"u1"].mean(),(cases.r3s<-0.25).sum()],
        "cond_alone":[nos.loc[nos.r3s<-0.25,"u1"].mean(),(nos.r3s<-0.25).sum()],
        "signal_rest":[cases.loc[cases.r3s>=-0.25,"u1"].mean(),(cases.r3s>=-0.25).sum()]},index=["mean_u1","n"])
    out["cond_uplow_low"]=pd.DataFrame({
        "both":[cases.loc[cases.uplow20<2,"u1"].mean(),(cases.uplow20<2).sum()],
        "cond_alone":[nos.loc[nos.uplow20<2,"u1"].mean(),(nos.uplow20<2).sum()],
        "signal_rest":[cases.loc[cases.uplow20>=2,"u1"].mean(),(cases.uplow20>=2).sum()]},index=["mean_u1","n"])
    out["alloc"]=held["pos"].abs().describe()
    # deepest fall days w14 and w11 losses
    D=pd.concat(dayrows,ignore_index=True)
    bk=D.groupby(["w","day"])["book_return"].mean().reset_index()
    bk["wn"]=bk["w"].str[1:].astype(int); bk=bk.sort_values(["wn","day"]).reset_index(drop=True)
    eq=(1+bk["book_return"].fillna(0)).cumprod(); bk["dd"]=(eq/eq.cummax()-1).values
    t=bk["dd"].idxmin(); p=int(np.argmax(eq.values[:t+1]))
    fall_days=set(zip(bk.loc[p:t,"w"],bk.loc[p:t,"day"]))
    fh=held[[ (a,b) in fall_days for a,b in zip(held.w,held.day)]]
    out["fall_held"]=fh.groupby("coin")[["gain","pos","r3s","r10s","uplow20","ret60","gb"]].agg(["mean"]).round(4)
    out["fall_held_n"]=fh.groupby("coin").size()
    w11=held[held.w=="w11"]
    out["w11_held"]=w11[["gain","pos","r3s","r10s","uplow20","ret60","gb"]].mean()
    out["lose_vs_win"]=held.assign(win=held.gain>0).groupby("win")[["r10s","uplow20","ret60"]].mean()
    return out
