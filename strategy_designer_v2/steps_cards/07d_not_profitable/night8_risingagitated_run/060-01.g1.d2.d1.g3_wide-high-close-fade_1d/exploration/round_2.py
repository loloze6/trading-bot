def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wd in data["bars"].items():
        for w,b in wd.items():
            b=b.copy().reset_index(drop=True)
            c=b["close"];h=b["high"];l=b["low"]
            rng=(h-l)
            b["cl"]=(c-l)/rng.replace(0,np.nan)
            b["rm"]=rng/rng.rolling(20,min_periods=10).mean()
            b["r10"]=c/c.shift(10)-1
            b["r1"]=c/c.shift(1)-1
            for k in [1,2,3,5]:
                b["n%d"%k]=c.shift(-k)/c-1
            b["alloc"]=b["postRebalance_current_allocation"]
            b["coin"]=coin;b["w"]=w
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    B=pd.concat(rows,ignore_index=True)
    sig=B["alloc"]<0
    S=B[sig].dropna(subset=["n1"]).copy()
    out={}
    # horizon: short excess per grid
    dr={k:B.groupby("coin")["n%d"%k].mean() for k in [1,2,3,5]}
    hz=[]
    for k in [1,2,3,5]:
        x=-(S["n%d"%k]-S["coin"].map(dr[k]))
        x=x.dropna()
        hz.append({"h":k,"mean":x.mean(),"n":len(x),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out["horizon_short_ex"]=pd.DataFrame(hz)
    # cross r10 x rm
    S["r10q"]=np.where(S["r10"]< -0.15,"deep","notdeep")
    S["rmq"]=np.where(S["rm"]>0.75,"wide","narrow")
    S["sx"]=-(S["n1"]-S["coin"].map(dr[1]))
    g=S.groupby(["r10q","rmq"])["sx"].agg(["mean","count","std"]);g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["cross_r10_rm"]=g.reset_index()
    # condition alone: in-profile bars without signal, r10 notdeep & wide
    U=B[(B["regime"]=="unknown")].dropna(subset=["n1"]).copy()
    U["sx"]=-(U["n1"]-U["coin"].map(dr[1]))
    U["c"]=(U["r10"]>=-0.15)&(U["rm"]>0.75)
    g=U.groupby("c")["sx"].agg(["mean","count","std"]);g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["cond_alone_nosig"]=g.reset_index()
    # simulated book: per-filter daily pnl = alloc*n1 minus cost on changes, mean over coins
    cost=0.0019
    def book(mask,scale=1.0):
        a=B["alloc"].where(mask,0.0)*scale
        prev=a.groupby([B["coin"],B["w"]]).shift(1).fillna(0)
        pnl=a*B["n1"].fillna(0)-cost/2*(a-prev).abs()
        df=pd.DataFrame({"w":B["w"],"day":B["day"],"coin":B["coin"],"p":pnl})
        d=df.groupby(["w","day"])["p"].mean().reset_index()
        d["wn"]=d["w"].str[1:].astype(int);d=d.sort_values(["wn","day"])
        v=(1+d["p"]).cumprod();dd=(v/v.cummax()-1).min()
        yr=v.iloc[-1]**(365/len(d))-1
        return {"sharpe":d["p"].mean()/d["p"].std()*np.sqrt(365),"yearly":yr,"maxdd":dd,"calmar":yr/-dd,"active":(a!=0).mean()}
    m0=B["alloc"]<0
    res={"as_tested":book(m0),
         "notdeep_r10":book(m0&(B["r10"]>=-0.15)),
         "wide_only":book(m0&(B["rm"]>0.75)),
         "wide_notdeep":book(m0&(B["rm"]>0.75)&(B["r10"]>=-0.15)),
         "wide_notdeep_x2":book(m0&(B["rm"]>0.75)&(B["r10"]>=-0.15),2.0)}
    out["sim_books"]=pd.DataFrame(res).T
    # by window for wide_notdeep pnl sum
    S2=S[(S["rm"]>0.75)&(S["r10"]>=-0.15)]
    out["wn_by_window"]=S2.groupby("w")["sx"].agg(["mean","count"])
    out["deep_by_window"]=S[S["r10"]<-0.15].groupby("w")["sx"].agg(["mean","count"])
    return out
