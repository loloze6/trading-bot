def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # rebuild book daily chain with episode labels
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["coin"]=c; dd["wn"]=int(w[1:])
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["wn","day"]).agg(br=("book_return","mean")).reset_index().sort_values(["wn","day"]).dropna()
    eq=(1+B["br"]).cumprod(); B["dd"]=(eq/eq.cummax()-1).values
    B["ep"]=(B["dd"]==0).cumsum()
    depth=B.groupby("ep")["dd"].min()
    deep=depth[depth<-0.12].index
    B["deep"]=B["ep"].isin(deep)
    # bar features per coin
    R=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.copy(); r=b["close"].pct_change()
            b["fwd"]=b["close"].shift(-1)/b["close"]-1
            b["gain"]=b["postRebalance_current_allocation"]*b["fwd"]
            b["ret10"]=b["close"]/b["close"].shift(10)-1
            b["ret30"]=b["close"]/b["close"].shift(30)-1
            b["ret60"]=b["close"]/b["close"].shift(60)-1
            b["vol_ratio"]=r.rolling(20).std()/r.rolling(60).std()
            b["fwd10"]=b["close"].shift(-10)/b["close"]-1
            b["pos"]=np.arange(len(b))
            b["wn"]=int(w[1:]); b["coin"]=c
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D") if "timestamp" in b else None
            R.append(b)
    R=pd.concat(R)
    L=R[R["postRebalance_current_allocation"]>0].dropna(subset=["gain"])
    # mark deep-episode days
    B["day"]=pd.to_datetime(B["day"]).dt.floor("D")
    L=L.copy(); L["day"]=L["day"].dt.tz_localize(None) if L["day"].dt.tz is not None else L["day"]
    Bd=B[["wn","day","deep"]].copy(); Bd["day"]=Bd["day"].dt.tz_localize(None) if Bd["day"].dt.tz is not None else Bd["day"]
    L=L.merge(Bd,on=["wn","day"],how="left")
    out["gain_by_deep"]=L.groupby("deep")["gain"].agg(["sum","mean","count"]).round(5)
    for col in ["ret30","ret60","vol_ratio","ret10"]:
        x=L.dropna(subset=[col])
        q=pd.qcut(x[col],5)
        out["sumgain_"+col]=x.groupby(q,observed=True)["gain"].agg(["sum","mean","count",lambda s:s[s<0].sum()]).round(4)
    # non-overlapping 10-day grid, trending, forecast>0: fwd10 by ret30/ret60 tercile and forecast slope inside
    G=R[(R["pos"]%10==0)&(R["regime"]=="trending")].dropna(subset=["fwd10","ret30","ret60"])
    cm=R[R["pos"]%10==0].groupby("coin")["fwd10"].mean()
    G=G.assign(ex=G["fwd10"]-G["coin"].map(cm))
    res=[]
    for col in ["ret30","ret60","vol_ratio"]:
        g=G.dropna(subset=[col])
        g=g.assign(t=pd.qcut(g[col],3,labels=["lo","mid","hi"]))
        for t,s in g.groupby("t",observed=True):
            sl=stats.linregress(s["forecast"],s["ex"])
            res.append([col,t,len(s),s["ex"].mean(),s.loc[s.forecast>10,"ex"].mean(),sl.slope,sl.slope/sl.stderr])
    out["grid_by_state"]=pd.DataFrame(res,columns=["state","tercile","n","mean_ex","ex_fc>10","slope","t"]).round(4)
    return out
