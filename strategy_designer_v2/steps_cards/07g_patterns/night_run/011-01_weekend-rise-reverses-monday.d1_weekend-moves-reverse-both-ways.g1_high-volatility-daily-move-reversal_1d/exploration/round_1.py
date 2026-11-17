def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df.copy()
            d["ts"]=pd.to_datetime(d["timestamp"])
            d=d.sort_values("ts").reset_index(drop=True)
            c=d["close"]
            d["r"]=c.pct_change()
            d["f1"]=c.shift(-1)/c-1
            d["vol"]=d["r"].rolling(20,min_periods=15).std()
            d["z"]=d["r"]/d["vol"]
            d["r2"]=c/c.shift(2)-1
            d["f2"]=c.shift(-2)/c-1
            d["vrel"]=d["volume"]/d["volume"].rolling(20,min_periods=15).mean()
            d["volpct"]=d["vol"]/d["vol"].rolling(60,min_periods=30).mean()
            d["wd"]=d["ts"].dt.weekday
            d["coin"]=coin; d["w"]=w
            d["alloc"]=d["postRebalance_current_allocation"]
            rows.append(d[["coin","w","wd","r","f1","z","vol","r2","f2","vrel","volpct","regime","alloc","forecast"]])
    A=pd.concat(rows)
    mu=A.groupby("coin")["r"].mean()
    A["f1x"]=A["f1"]-A["coin"].map(mu)
    A["f2x"]=A["f2"]-2*A["coin"].map(mu)
    out={}
    def tab(g):
        s=g.agg(["mean","count","std"]); s["t"]=s["mean"]/(s["std"]/np.sqrt(s["count"])); return s.drop(columns="std")
    B=A.dropna(subset=["z","f1x"]).copy()
    B["zq"]=pd.qcut(B["z"],5,labels=False)
    B["mr"]=(B["regime"]=="mean_reversion")
    out["f1x by z quintile x regime"]=tab(B.groupby(["mr","zq"])["f1x"])
    out["f1x by weekday"]=tab(B.groupby("wd")["f1x"])
    # reversal coefficient by weekday of the move: -corr(z, f1x)
    rc=B.groupby("wd").apply(lambda g: pd.Series({"slope":np.polyfit(g["z"],g["f1x"]/g["vol"],1)[0],"n":len(g),"corr":g["z"].corr(g["f1x"])}))
    rc["t_corr"]=rc["corr"]*np.sqrt(rc["n"]-2)/np.sqrt(1-rc["corr"]**2)
    out["next-day vs today z by weekday of today"]=rc
    # weekend 2-day move (Sat+Sun, read at Sunday bar wd=6) vs next 2 days
    W=A[(A["wd"]==6)].dropna(subset=["r2","f2x","vol"]).copy()
    W["z2"]=W["r2"]/(W["vol"]*np.sqrt(2))
    W["q"]=pd.qcut(W["z2"],3,labels=False)
    out["weekend z2 tercile -> next 2d excess"]=tab(W.groupby("q")["f2x"])
    W2=A[(A["wd"]==2)].dropna(subset=["r2","f2x","vol"]).copy()
    W2["z2"]=W2["r2"]/(W2["vol"]*np.sqrt(2)); W2["q"]=pd.qcut(W2["z2"],3,labels=False)
    out["Tue+Wed z2 tercile -> next 2d excess"]=tab(W2.groupby("q")["f2x"])
    # volume relative interaction among big moves
    Bb=B[B["z"].abs()>1].copy()
    Bb["rev"]=-np.sign(Bb["z"])*Bb["f1x"]
    Bb["vq"]=pd.qcut(Bb["vrel"],3,labels=False)
    out["|z|>1 reversal by rel volume tercile"]=tab(Bb.groupby("vq")["rev"])
    B["vlq"]=pd.qcut(B["volpct"],3,labels=False)
    B["rev"]=-np.sign(B["z"])*B["f1x"]
    out["reversal by vol-level tercile (vol/60d mean)"]=tab(B.groupby("vlq")["rev"])
    # book
    D=[]
    for coin,ws in data["days"].items():
        for w,df in ws.items():
            x=df.copy(); x["wd"]=pd.to_datetime(x["day"]).dt.weekday; x["coin"]=coin; x["w"]=w; D.append(x)
    D=pd.concat(D)
    bd=D.groupby(["w","day"]).agg(b=("book_return","mean"),c=("coin_return","mean"),wd=("wd","first")).dropna()
    out["book daily by weekday"]=tab(bd.groupby("wd")["b"])
    out["book corr with coins"]=float(bd["b"].corr(bd["c"]))
    bd["bq"]=pd.qcut(bd["c"],5,labels=False)
    out["book by market-day quintile"]=tab(bd.groupby("bq")["b"])
    out["alloc mean by regime"]=A.groupby("regime")["alloc"].agg(["mean",lambda s:s.abs().mean(),"count"])
    return out
