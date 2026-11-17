import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    br=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.copy()
            r=b.close.pct_change()
            b["r"]=r
            b["nxt"]=b.close.shift(-1)/b.close-1
            b["f3"]=b.close.shift(-3)/b.close-1
            b["pos"]=b.postRebalance_current_allocation
            b["gain"]=b.pos*b.nxt
            b["r20"]=b.close/b.close.shift(20)-1
            b["ma50"]=b.close/b.close.rolling(50).mean()-1
            b["vol30"]=r.rolling(30).std()
            b["vol90"]=r.rolling(90).std()
            b["volratio"]=b.vol30/b.vol90
            b["day"]=pd.to_datetime(b.timestamp).dt.floor("D")
            b["coin"]=c; b["wn"]=int(w[1:])
            b["grid"]=(np.arange(len(b))%3==0)
            br.append(b)
    X=pd.concat(br)
    # book daily from days + bar states
    rows=[]
    for c, ws in data["days"].items():
        for w, d in ws.items():
            t=d[["day","book_return","coin_return"]].copy(); t["coin"]=c; t["wn"]=int(w[1:]); rows.append(t)
    D=pd.concat(rows)
    D["day"]=pd.to_datetime(D["day"]).dt.floor("D")
    S=X[["coin","wn","day","pos","volratio","ma50","r20","forecast"]].copy()
    S["day"]=S["day"]+pd.Timedelta(days=1)  # state at previous close
    D=D.merge(S,on=["coin","wn","day"],how="left")
    B=D.groupby(["wn","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean"),pos=("pos","mean"),
        vr=("volratio","mean"),ma=("ma50","mean"),r20=("r20","mean")).dropna(subset=["br"]).reset_index().sort_values(["wn","day"])
    eq=(1+B.br).cumprod(); B["dd"]=(eq/eq.cummax()-1).values
    B["indd"]=B.dd< -0.10
    out["book days by deep drawdown (<-10%)"]=B.groupby("indd").agg(n=("br","size"),br=("br","mean"),cr=("cr","mean"),pos=("pos","mean"),vr=("vr","mean"),ma=("ma","mean"),r20=("r20","mean"))
    # book daily return by mean ma50 state quartile
    B["maq"]=pd.qcut(B.ma,4,labels=False)
    out["book days by mean ma50 q"]=B.groupby("maq").agg(lo=("ma","min"),hi=("ma","max"),n=("br","size"),br=("br","mean"),sd=("br","std"),cr=("cr","mean"),pos=("pos","mean"))
    B["vrq"]=pd.qcut(B.vr,4,labels=False)
    out["book days by mean volratio q"]=B.groupby("vrq").agg(lo=("vr","min"),hi=("vr","max"),n=("br","size"),br=("br","mean"),sd=("br","std"),cr=("cr","mean"),pos=("pos","mean"))
    # worst book days
    w=B.nsmallest(60,"br")
    out["worst 60 book days"]=pd.Series({"mean br":w.br.mean(),"mean cr":w.cr.mean(),"pos":w.pos.mean(),"ma":w.ma.mean(),"r20":w.r20.mean(),"vr":w.vr.mean(),
        "all pos":B.pos.mean(),"all ma":B.ma.mean(),"all r20":B.r20.mean()})
    # grid: f3 excess on forecast>0, by trend state ma50 sign and forecast
    G=X[X.grid].dropna(subset=["f3","ma50"]).copy()
    G["ex"]=G.f3-G.groupby("coin").f3.transform("mean")
    G["up"]=np.where(G.ma50>0,"above50","below50")
    P=G[G.forecast>0].copy()
    P["fq"]=pd.qcut(P.forecast,3,labels=False)
    out["grid ex3 by trend x forecast tercile"]=P.groupby(["up","fq"]).agg(n=("ex","size"),ex=("ex","mean"),t=("ex",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    def slope(df):
        if len(df)<30: return pd.Series({"n":len(df)})
        s=stats.linregress(df.forecast,df.ex)
        return pd.Series({"n":len(df),"slope":s.slope,"t":s.slope/s.stderr})
    G["vrh"]=np.where(G.volratio>G.volratio.median(),"vol rising","vol calm")
    out["slope by trend"]=G.groupby("up").apply(slope)
    out["slope by volratio"]=G.dropna(subset=["volratio"]).groupby("vrh").apply(slope)
    G["r20s"]=np.where(G.r20>0,"m up","m down")
    out["slope by r20 sign"]=G.dropna(subset=["r20"]).groupby("r20s").apply(slope)
    # held bar gain by trend
    H=X[X.pos>0].dropna(subset=["ma50"])
    out["held gain by ma50 sign"]=H.groupby(H.ma50>0).agg(n=("gain","size"),gain=("gain","mean"),sd=("gain","std"),pos=("pos","mean"))
    return out
