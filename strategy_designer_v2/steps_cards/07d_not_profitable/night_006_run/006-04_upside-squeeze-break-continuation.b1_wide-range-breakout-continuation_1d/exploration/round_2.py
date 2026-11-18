def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for c in data["bars"]:
        allr=[];all10=[]
        for w,b in data["bars"][c].items():
            r1=b["close"].shift(-1)/b["close"]-1; allr.append(r1.dropna())
            cl=b["close"].values; idx=np.arange(0,len(cl)-10,10)
            all10.append(pd.Series(cl[idx+10]/cl[idx]-1))
        cm=pd.concat(allr).mean(); cm10=pd.concat(all10).mean()
        for w,b in data["bars"][c].items():
            b=b.copy().reset_index(drop=True); b["coin"]=c; b["win"]=w
            b["r1"]=b["close"].shift(-1)/b["close"]-1
            for h in [3,5,10,20]:
                b["r%d"%h]=b["close"].shift(-h)/b["close"]-1
            b["cm"]=cm; b["cm10"]=cm10
            b["ret20"]=b["close"]/b["close"].shift(20)-1
            ma=b["close"].rolling(100).mean(); b["abovema"]=(b["close"]>ma).astype(float); b.loc[ma.isna(),"abovema"]=np.nan
            b["t"]=(b["regime"]=="trending").astype(int)
            # days since last breakout
            last=np.full(len(b),np.nan); lb=-999
            for i,v in enumerate(b["t"].values):
                if v: lb=i
                last[i]=i-lb if lb>=0 else np.nan
            b["since"]=last
            # greedy non-overlap
            sel=np.zeros(len(b),bool); nxt=0
            for i,v in enumerate(b["t"].values):
                if v and i>=nxt and i+10<len(b): sel[i]=True; nxt=i+10
            b["sel"]=sel
            rows.append(b)
    B=pd.concat(rows); out={}
    S=B[B["sel"]].copy(); S["ex10"]=S["r10"]-S["cm10"]
    out["nonoverlap breakout excess r10"]=pd.Series({"n":len(S),"mean ex10":S["ex10"].mean(),"t":S["ex10"].mean()/S["ex10"].std()*np.sqrt(len(S)),
        "mean r10":S["r10"].mean(),"coin mean10":S["cm10"].mean(),"share ex10>0":(S["ex10"]>0).mean()})
    # daily excess return by days since breakout (0 = breakout bar)
    x=B.dropna(subset=["since","r1"]).copy(); x["ex1"]=x["r1"]-x["cm"]; x["sc"]=x["since"].clip(upper=25)
    g=x.groupby(pd.cut(x["sc"],[-1,0,3,6,10,15,25]))
    out["daily excess by days since breakout"]=pd.DataFrame({"n":g.size(),"ex1":g["ex1"].mean(),"t":g["ex1"].mean()/g["ex1"].std()*np.sqrt(g.size())})
    # regime: above 100-day MA
    for col in ["abovema"]:
        y=S.dropna(subset=[col]); g=y.groupby(col)
        out["ex10 by "+col]=pd.DataFrame({"n":g.size(),"ex10":g["ex10"].mean(),"t":g["ex10"].mean()/g["ex10"].std()*np.sqrt(g.size())})
    y=S.dropna(subset=["debug_info.components.width.post_pipeline_value"])
    q=pd.qcut(y["debug_info.components.width.post_pipeline_value"],3,labels=["lo","mid","hi"]); g=y.groupby(q)
    out["ex10 by width third"]=pd.DataFrame({"n":g.size(),"ex10":g["ex10"].mean(),"t":g["ex10"].mean()/g["ex10"].std()*np.sqrt(g.size())})
    q=pd.qcut(S["ret20"],3,labels=["lo","mid","hi"]); g=S.groupby(q)
    out["ex10 by ret20 third"]=pd.DataFrame({"n":g.size(),"ex10":g["ex10"].mean(),"t":g["ex10"].mean()/g["ex10"].std()*np.sqrt(g.size())})
    g=S.groupby("coin"); out["ex10 by coin"]=pd.DataFrame({"n":g.size(),"ex10":g["ex10"].mean()})
    # drawdown of book
    D=[]
    for c in data["days"]:
        for w,d in data["days"][c].items():
            d=d.copy(); d["coin"]=c; d["win"]=w; D.append(d)
    D=pd.concat(D).dropna(subset=["book_return"])
    dd=D.groupby(["win","day"])["book_return"].mean()
    wins=sorted(dd.index.get_level_values(0).unique(),key=lambda s:int(s[1:]))
    ch=pd.concat([dd.loc[w] for w in wins]); eq=(1+ch.values).cumprod()
    out["book chain"]=pd.Series({"total":eq[-1]-1,"maxdd":(eq/np.maximum.accumulate(eq)-1).min(),"ndays":len(eq)})
    return out
