def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    coins = list(data["bars"].keys())
    # ---- book daily returns, mean over coins per day, per window
    wins = sorted({w for c in coins for w in data["days"][c].keys()}, key=lambda s: int(s[1:]))
    chain = []
    for w in wins:
        frames = []
        for c in coins:
            if w in data["days"][c]:
                d = data["days"][c][w][["day","book_return"]].copy(); d["coin"]=c; frames.append(d)
        df = pd.concat(frames)
        m = df.groupby("day")["book_return"].mean().dropna().reset_index()
        m["w"]=w; chain.append(m)
    ch = pd.concat(chain, ignore_index=True)
    ch["val"] = (1+ch["book_return"]).cumprod()
    ch["peak"] = ch["val"].cummax(); ch["dd"] = ch["val"]/ch["peak"]-1
    out["deepest fall"] = ch["dd"].min()
    out["dd by window (min dd, sum ret)"] = ch.groupby("w").agg(mindd=("dd","min"), ret=("book_return","sum"), n=("book_return","size")).T
    # episodes: from peak to trough
    ep=[]; i=0; vals=ch["val"].values; dd=ch["dd"].values
    peak_i=0
    in_dd=False
    for k in range(len(ch)):
        if dd[k]==0:
            if in_dd:
                seg=dd[start:k]; t=start+int(np.argmin(seg)); ep.append((start-1,t,seg.min(),k))
                in_dd=False
        else:
            if not in_dd: start=k; in_dd=True
    if in_dd:
        seg=dd[start:]; t=start+int(np.argmin(seg)); ep.append((start-1,t,seg.min(),len(ch)))
    ep=sorted(ep,key=lambda x:x[2])[:5]
    out["top falls (window of peak, window of trough, depth, days peak->trough)"] = pd.DataFrame(
        [(ch["w"].iloc[max(a,0)], ch["w"].iloc[t], d, t-a) for a,t,d,e in ep], columns=["w_peak","w_trough","depth","days"])
    ch["inDD"]=False
    for a,t,d,e in ep[:3]:
        ch.loc[max(a,0)+1:t,"inDD"]=True
    # ---- per coin bar features
    rows=[]
    for c in coins:
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            a=b["postRebalance_current_allocation"].fillna(0)
            gain=a*(cl.shift(-1)/cl-1)
            f=b["forecast"].fillna(0)
            rng=((b["high"]-b["low"])/b["close"])
            sr = np.log(cl/cl.shift(3))/rng.rolling(30).mean()
            vol10=r.rolling(10).std(); vol60=r.rolling(60).std()
            ret60=cl/cl.shift(60)-1
            r3=cl/cl.shift(3)-1
            hi20=cl/cl.rolling(20).max()-1
            fwd3=cl.shift(-3)/cl-1
            day=pd.to_datetime(b["timestamp"]).dt.floor("D")
            inprof=b["debug_info.components.scaled_rise.last_history_value"].notna()
            dfc=pd.DataFrame(dict(coin=c,w=w,pos=np.arange(len(b)),day=day.values,a=a,gain=gain,f=f,
                vr=vol10/vol60,ret60=ret60,r3=r3,hi20=hi20,fwd3=fwd3,inprof=inprof,rng=rng/rng.rolling(30).mean(),r1=r))
            rows.append(dfc)
    B=pd.concat(rows,ignore_index=True)
    # drift per coin: mean 3-bar return on grid
    G=B[B.pos%3==0].copy()
    drift=G.groupby("coin")["fwd3"].mean()
    G["ex"]=G["fwd3"]-G["coin"].map(drift)
    # book days in falls: which coin/state
    B["dayn"]=pd.to_datetime(B["day"])
    ch["day"]=pd.to_datetime(ch["day"])
    Bm=B.merge(ch[["day","w","inDD"]],left_on=["dayn","w"],right_on=["day","w"],how="left")
    held=Bm[Bm.a>0]
    out["held bars: in falls vs not"] = held.groupby("inDD").agg(n=("gain","size"),gain=("gain","mean"),a=("a","mean"),f=("f","mean"),vr=("vr","mean"),ret60=("ret60","mean"),hi20=("hi20","mean"),r3=("r3","mean"))
    # held gains by buckets
    held=held.copy()
    held["vrq"]=pd.qcut(held["vr"],4,labels=False,duplicates="drop")
    held["r60b"]=pd.cut(held["ret60"],[-9,0.1,0.3,0.6,1.0,99])
    held["fq"]=pd.qcut(held["f"],4,labels=False,duplicates="drop")
    for k in ["vrq","r60b","fq"]:
        g=held.groupby(k)["gain"]
        out["held gain by "+k]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"std":g.std(),"sum":g.sum(),"min":g.min()})
    # grid: in profile, forecast>0 vs condition alone
    Gp=G[G.inprof].copy()
    Gp["sig"]=Gp.f>0
    Gp["vrq"]=pd.qcut(Gp["vr"],4,labels=False,duplicates="drop")
    Gp["r60b"]=pd.cut(Gp["ret60"],[-9,0.1,0.3,0.6,1.0,99])
    for k in ["vrq","r60b"]:
        g=Gp.groupby([k,"sig"])["ex"]
        out["grid ex3 by "+k+" x signal"]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size())),"p10":g.quantile(0.1)})
    Gs=Gp[Gp.sig].copy(); Gs["fq"]=pd.qcut(Gs["f"],4,labels=False,duplicates="drop")
    g=Gs.groupby("fq")["ex"]
    out["grid ex3 by forecast quartile"]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size())),"p10":g.quantile(0.1)})
    out["by year book"]=ch.assign(y=ch.day.dt.year).groupby("y")["book_return"].agg(["mean","std","size","min"])
    return out
