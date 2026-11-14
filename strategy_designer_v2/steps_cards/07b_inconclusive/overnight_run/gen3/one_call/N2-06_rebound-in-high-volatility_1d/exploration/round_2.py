def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df.copy().reset_index(drop=True)
            d["nxt"]=d["close"].shift(-1)/d["close"]-1
            d["ret"]=d["close"].pct_change()
            d["sd20"]=d["ret"].rolling(20,min_periods=15).std()
            d["vp"]=d["sd20"].rolling(100,min_periods=40).apply(lambda x:(x[:-1]<x[-1]).mean() if len(x)>1 else np.nan,raw=True)
            d["ret5"]=d["close"]/d["close"].shift(5)-1
            d["ret5z"]=d["ret5"]/(d["sd20"]*np.sqrt(5))
            d["coin"]=coin; d["w"]=w
            rows.append(d[["coin","w","forecast","regime","nxt","ret","sd20","vp","ret5","ret5z"]])
    a=pd.concat(rows).dropna(subset=["nxt","forecast","sd20"])
    cm=a.groupby("coin")["nxt"].mean()
    a["ex"]=a["nxt"]-a["coin"].map(cm)
    a["exz"]=a["ex"]/a["sd20"]
    a["up"]=(a["nxt"]>0).astype(float)-a["coin"].map(a.groupby("coin")["nxt"].apply(lambda s:(s>0).mean()))
    thr=a.forecast.quantile(0.9)
    top=a[(a.forecast>=thr)&(a.forecast>0)].copy()
    def summ(g):
        n=len(g)
        return pd.Series({"n":n,"mean_ex":g.ex.mean(),"t":g.ex.mean()/(g.ex.std()/np.sqrt(n)),
                          "mean_exz":g.exz.mean(),"tz":g.exz.mean()/(g.exz.std()/np.sqrt(n)),"netup":g.up.mean(),
                          "med_ex":g.ex.median(),"sd_ex":g.ex.std()})
    out={}
    out["top_regime"]=top.groupby("regime").apply(summ)
    top["vpb"]=pd.cut(top.vp,[-0.01,0.25,0.5,0.75,0.9,1.01])
    out["top_by_vp_bucket"]=top.groupby("vpb").apply(summ)
    top["r5b"]=pd.cut(top.ret5z,[-99,-2.5,-1.5,-0.5,99])
    out["top_by_ret5z"]=top.groupby(["r5b","regime"]).apply(summ)
    top["r5neg"]=top.ret5<-0.1
    out["top_by_5d_regime"]=top.groupby(["r5neg","regime"]).apply(summ)
    # by window halves to check stability of 5d-drop effect
    sub=top[top.ret5z<-1.5]
    out["deep_by_coin"]=sub.groupby("coin").apply(summ)
    wn=sub.w.str[1:].astype(int)
    sub=sub.assign(wg=pd.cut(wn,[0,6,12,18,24],labels=["w1-6","w7-12","w13-18","w19-24"]))
    out["deep_by_wgroup"]=sub.groupby("wg").apply(summ)
    return out
