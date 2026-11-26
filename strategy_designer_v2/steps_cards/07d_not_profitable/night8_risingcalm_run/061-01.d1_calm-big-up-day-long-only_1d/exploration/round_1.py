def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # book daily returns pooled across coins per day (by window)
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d.copy(); dd["coin"] = c; dd["win"] = w
            rows.append(dd[["day","book_return","coin_return","coin","win"]])
    D = pd.concat(rows)
    D["wn"] = D["win"].str[1:].astype(int)
    book = D.groupby(["wn","day"])["book_return"].mean().dropna().reset_index().sort_values(["wn","day"])
    v = (1+book["book_return"]).cumprod()
    dd = v/v.cummax()-1
    book["dd"] = dd.values
    out["dd_min_by_window"] = book.groupby("wn")["dd"].min()
    # per-window book stats
    g = book.groupby("wn")["book_return"]
    out["window_stats"] = pd.DataFrame({"mean":g.mean(),"sd":g.std(),"n":g.count(),
        "chain":g.apply(lambda s:(1+s).prod()-1)})
    # per coin per bar features
    feats=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.copy().reset_index(drop=True)
            cl=b["close"]
            r1=cl.pct_change()
            b["tr60"]=cl/cl.shift(60)-1
            b["r5"]=cl.shift(-5)/cl-1
            b["r1f"]=cl.shift(-1)/cl-1
            b["ret5p"]=cl/cl.shift(5)-1
            b["ret20p"]=cl/cl.shift(20)-1
            b["pos"]=b["postRebalance_current_allocation"]
            b["gain"]=b["pos"]*b["r1f"]
            b["coin"]=c; b["wn"]=int(w[1:]); b["i"]=np.arange(len(b))
            b["calm"]=b["regime"]!="chop"
            feats.append(b[["coin","wn","i","forecast","tr60","r5","r1f","ret5p","ret20p","pos","gain","calm"]])
    F=pd.concat(feats)
    F["trend"]=pd.cut(F["tr60"],[-np.inf,-0.1,0.1,np.inf],labels=["falling","choppy","rising"])
    held=F[F["pos"].abs()>1e-9]
    out["gain_by_trend_held"]=held.groupby("trend")["gain"].agg(["mean","std","count","sum"])
    out["gain_by_window_trend"]=held.groupby(["wn","trend"])["gain"].sum().unstack()
    # grid 5-bar, calm, signal vs no signal, by trend
    G=F[(F["i"]%5==0)&F["calm"]].dropna(subset=["r5","tr60"])
    G["sig"]=G["forecast"]>0
    drift=F[F["i"]%5==0].groupby("coin")["r5"].mean()
    G["ex"]=G["r5"]-G["coin"].map(drift)
    out["grid_calm_trend_sig"]=G.groupby(["trend","sig"])["ex"].agg(["mean","std","count"])
    # forecast terciles by trend
    S=G[G["sig"]].copy()
    S["fq"]=pd.qcut(S["forecast"],3,labels=["lo","mid","hi"])
    out["grid_sig_trend_fq"]=S.groupby(["trend","fq"])["ex"].agg(["mean","count"]).unstack()
    # trailing 20d return condition
    S["p20"]=pd.cut(S["ret20p"],[-np.inf,-0.05,0.05,np.inf],labels=["down","flat","up"])
    G["p20"]=pd.cut(G["ret20p"],[-np.inf,-0.05,0.05,np.inf],labels=["down","flat","up"])
    out["grid_calm_p20_sig"]=G.groupby(["p20","sig"])["ex"].agg(["mean","count"]).unstack()
    # deepest drawdown episodes: held gain by trend during days dd<-0.15
    worst=book.nsmallest(1,"dd")
    out["worst_dd"]=worst
    return out
