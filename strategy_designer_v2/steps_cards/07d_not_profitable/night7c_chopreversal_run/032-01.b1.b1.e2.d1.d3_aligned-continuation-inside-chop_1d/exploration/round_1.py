def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    wins = sorted({w for c in coins for w in bars[c].keys()}, key=lambda s:int(s[1:]))
    # book daily
    rows=[]
    for w in wins:
        frames=[]
        for c in coins:
            if w in days[c]:
                d=days[c][w][["day","book_return","coin_return"]].copy(); d["coin"]=c; frames.append(d)
        df=pd.concat(frames)
        g=df.groupby("day")[["book_return","coin_return"]].mean().reset_index(); g["w"]=w
        rows.append(g.iloc[1:] if len(g)>1 else g)
    book=pd.concat(rows,ignore_index=True).dropna()
    book["val"]=(1+book["book_return"]).cumprod()
    book["peak"]=book["val"].cummax(); book["dd"]=book["val"]/book["peak"]-1
    # per window
    pw=book.groupby("w").agg(mean=("book_return","mean"),sum=("book_return","sum"),hold=("coin_return","sum"),n=("book_return","size"))
    def mdd(x):
        v=(1+x).cumprod(); return (v/v.cummax()-1).min()
    pw["mdd"]=book.groupby("w")["book_return"].apply(mdd)
    out["per_window"]=pw.loc[wins]
    out["global_mdd"]=float(book["dd"].min())
    # deepest fall episode: from peak to trough
    i_tr=book["dd"].idxmin(); pk=book.loc[:i_tr,"val"].idxmax()
    ep=book.loc[pk:i_tr]
    out["deepest_fall_windows"]=ep.groupby("w").agg(n=("book_return","size"),book=("book_return","sum"),hold=("coin_return","sum"))
    # bar-level
    B=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.copy().reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            b["ret1"]=cl.shift(-1)/cl-1
            b["pos"]=b["postRebalance_current_allocation"]
            b["gain"]=b["pos"]*b["ret1"]
            ch=cl.diff().abs()
            b["er"]=(cl-cl.shift(30)).abs()/ch.rolling(30).sum()
            b["r7"]=cl/cl.shift(7)-1; b["r30"]=cl/cl.shift(30)-1
            b["vol30"]=r.rolling(30).std(); b["vol90"]=r.rolling(90).std()
            b["volratio"]=b["vol30"]/b["vol90"]
            b["fwd7"]=cl.shift(-7)/cl-1
            b["coin"]=c; b["w"]=w; b["i"]=np.arange(len(b))
            B.append(b)
    B=pd.concat(B,ignore_index=True)
    drift=B[B["i"]%7==0].groupby("coin")["fwd7"].mean()
    B["fwd7a"]=B["fwd7"]-B["coin"].map(drift)
    held=B[B["pos"].abs()>1e-6].dropna(subset=["gain"])
    held["side"]=np.where(held["pos"]>0,"long","short")
    out["gain_by_side"]=held.groupby("side")["gain"].agg(["mean","sum","count","std"])
    held["chop_now"]=(held["regime"]=="chop")
    out["gain_by_chopnow"]=held.groupby(["chop_now","side"])["gain"].agg(["mean","sum","count"])
    held["volq"]=pd.qcut(held["volratio"],4,labels=False)
    out["gain_by_volratio_q"]=held.groupby(["volq"])["gain"].agg(["mean","sum","count"])
    held["absr30"]=pd.qcut(held["r30"].abs(),4,labels=False)
    out["gain_by_absr30_q"]=held.groupby("absr30")["gain"].agg(["mean","sum","count"])
    out["gain_by_coin"]=held.groupby(["coin","side"])["gain"].sum().unstack()
    held["absf"]=pd.qcut(held["forecast"].abs().replace(0,np.nan),4,labels=False,duplicates="drop")
    out["gain_by_absforecast_q"]=held.groupby("absf")["gain"].agg(["mean","sum","count"])
    # deepest fall: what was held
    epdays=set(zip(ep["w"],ep["day"]))
    B["day"]=pd.to_datetime(B["timestamp"]).dt.floor("D")
    he=held.copy(); he["day"]=pd.to_datetime(he["timestamp"]).dt.floor("D")
    m=[ (a,b) in epdays for a,b in zip(he["w"],he["day"])]
    hep=he[m]
    out["fall_held_by_side"]=hep.groupby(["side","chop_now"])["gain"].agg(["mean","sum","count"])
    out["fall_held_volratio_mean"]=float(hep["volratio"].mean()); out["all_held_volratio_mean"]=float(held["volratio"].mean())
    # grid signal cases: fwd7 signed by forecast direction by side
    G=B[(B["i"]%7==0)&(B["forecast"]!=0)].dropna(subset=["fwd7a"])
    G["s"]=np.sign(G["forecast"]); G["sig"]=G["s"]*G["fwd7a"]
    G["side"]=np.where(G["s"]>0,"long","short")
    def tt(x): return pd.Series({"mean":x.mean(),"n":len(x),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out["cases_by_side"]=G.groupby("side")["sig"].apply(tt).unstack()
    G["vq"]=pd.qcut(G["volratio"],3,labels=False)
    out["cases_by_volratio"]=G.groupby("vq")["sig"].apply(tt).unstack()
    G["erq"]=pd.qcut(G["er"],3,labels=False)
    out["cases_by_er"]=G.groupby("erq")["sig"].apply(tt).unstack()
    return out
