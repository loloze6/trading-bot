def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    wins = sorted(days[coins[0]].keys(), key=lambda w: int(w[1:]))
    # book daily returns, mean over coins per day, per window
    book = []
    for w in wins:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day","book_return","coin_return"]].copy(); d["coin"]=c; frames.append(d)
        df = pd.concat(frames)
        g = df.groupby("day")[["book_return","coin_return"]].mean().dropna().reset_index()
        g["win"]=w; book.append(g)
    B = pd.concat(book, ignore_index=True)
    B["eq"]=(1+B["book_return"]).cumprod()
    B["peak"]=B["eq"].cummax(); B["dd"]=B["eq"]/B["peak"]-1
    # drawdown episodes
    ep=[]; inep=False
    for i,r in B.iterrows():
        if r["dd"]<0 and not inep: inep=True; s=i
        if inep and (r["dd"]==0 or i==len(B)-1):
            seg=B.loc[s:i]; ep.append((seg["dd"].min(), len(seg), seg["win"].iloc[0], seg["win"].iloc[-1], seg.loc[seg["dd"].idxmin(),"win"], (1+seg.loc[:seg["dd"].idxmin(),"coin_return"]).prod()-1))
            inep=False
    E=pd.DataFrame(ep,columns=["depth","ndays","win_start","win_end","win_trough","coin_chain_to_trough"]).sort_values("depth").head(8)
    yrs=len(B)/365; yr=B["eq"].iloc[-1]**(1/yrs)-1
    perwin=B.groupby("win").agg(book=("book_return",lambda x:(1+x).prod()-1),coin=("coin_return",lambda x:(1+x).prod()-1),ndays=("book_return","size"))
    perwin["book_mindd"]=B.groupby("win")["dd"].min()
    # bar-level states
    rows=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"]; r1=cl.pct_change()
            r72=cl/cl.shift(72)-1
            eff=(cl-cl.shift(72)).abs()/r1.abs().mul(cl.shift(1)).rolling(72).sum()
            r720=cl/cl.shift(720)-1
            vol=r1.rolling(72).std(); volr=vol/r1.rolling(720).std()
            hi=cl/cl.rolling(720).max()-1
            f72=cl.shift(-72)/cl-1
            a=b["postRebalance_current_allocation"]
            pg=a*(cl.shift(-1)/cl-1)
            d=pd.DataFrame({"coin":c,"win":w,"r72":r72,"eff":eff,"r720":r720,"volr":volr,"hi":hi,"f72":f72,"a":a,"pg":pg,"fc":b["forecast"],"grid":(np.arange(len(b))%72==0)})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D[D.grid].groupby("coin")["f72"].mean()
    D["ex"]=D["f72"]-D["coin"].map(mu)
    G=D[D.grid&(D.fc>0)].dropna(subset=["f72"])
    out={}
    for v in ["r720","volr","hi","r72","eff"]:
        q=pd.qcut(G[v],5,duplicates="drop")
        t=G.groupby(q).agg(n=("ex","size"),mean_f72=("f72","mean"),mean_ex=("ex","mean"),
            t_ex=("ex",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))),
            share_neg=("f72",lambda x:(x<-0.05).mean()))
        t.index=t.index.astype(str); out["grid_by_"+v]=t
        qa=pd.qcut(D.loc[D.a>0,v],5,duplicates="drop")
        H=D[D.a>0].groupby(qa)["pg"].agg(["sum","mean","size"]); H.index=H.index.astype(str)
        out["hourly_gain_by_"+v]=H
    return {"yearly":yr,"maxdd":B["dd"].min(),"episodes":E,"per_window":perwin,**out,
            "share_time_long":(D.a>0).mean()}
