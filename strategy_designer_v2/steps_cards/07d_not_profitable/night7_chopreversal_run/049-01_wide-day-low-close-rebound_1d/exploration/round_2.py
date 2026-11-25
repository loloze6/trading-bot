def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy().reset_index(drop=True)
            b["ret1"] = b["close"].shift(-1)/b["close"]-1
            b["r60"] = b["close"]/b["close"].shift(60)-1
            lr = np.log(b["close"]).diff()
            b["vol10"] = lr.rolling(10).std(); b["vol60"] = lr.rolling(60, min_periods=30).std()
            b["vr"]=b["vol10"]/b["vol60"]
            rng = b["high"]-b["low"]
            b["mult"] = rng/rng.shift(1).rolling(30, min_periods=20).mean()
            b["depth"] = (b["high"]-b["close"])/rng.replace(0,np.nan)
            b["raw"] = b["depth"]*b["mult"]
            b["xw"] = b["depth"]*(b["mult"]-1).clip(lower=0)
            b["pos"] = b["postRebalance_current_allocation"]
            b["scale"] = b["pos"]/b["forecast"].replace(0,np.nan)
            b["coin"]=coin; b["w"]=w; b["wn"]=int(w[1:])
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    B["ex"]=B["ret1"]-B.groupby("coin")["ret1"].transform("mean")
    B["scale"]=B.groupby(["coin","w"])["scale"].transform(lambda s: s.ffill().bfill())
    def book(posname):
        g=B.assign(gain=B[posname]*B["ret1"]).dropna(subset=["ret1"])
        d=g.groupby(["wn","day"])["gain"].mean().reset_index().sort_values(["wn","day"])
        v=(1+d["gain"]).cumprod(); dd=(v/v.cummax()-1).min()
        yr=v.iloc[-1]**(365/len(d))-1
        dmin=d.assign(v=v.values).groupby("wn")["gain"].sum()
        return {"mean":d["gain"].mean(),"sd":d["gain"].std(),"sharpe":d["gain"].mean()/d["gain"].std()*np.sqrt(365),
                "yr":yr,"maxdd":dd,"calmar":yr/abs(dd),"w14":dmin.get(14,np.nan),"w9":dmin.get(9,np.nan),"w7":dmin.get(7,np.nan),
                "share_in":(B[posname]>0).mean()}
    res={}
    res["tested"]=book("pos")
    # alt forecast: excess-width product, scaled to same mean position
    for name in ["raw","xw"]:
        f=B[name].fillna(0)
        f=f/f[f>0].quantile(0.95)*20
        f=f.clip(upper=20)
        B["p_"+name]=f*B["scale"]
        res[name]=book("p_"+name)
    # top-two-quintile only of tested forecast
    q=B["forecast"].quantile(0.6)
    B["p_top"]=np.where(B["forecast"]>=q,B["pos"],0)
    res["top40"]=book("p_top")
    # xw restricted to vr>1 (agitated short-term)
    B["p_xw_vr"]=np.where(B["vr"]>1,B["p_xw"],0)
    res["xw_vr"]=book("p_xw_vr")
    out["books"]=pd.DataFrame(res).T
    # graded check of xw: quintiles among xw>0, plus xw==0 bars
    X=B.dropna(subset=["ret1","xw"])
    X["xq"]=np.where(X["xw"]>0, pd.qcut(X["xw"].where(X["xw"]>0).rank(method="first"),4,labels=False), -1)
    g=X.groupby("xq")
    out["xw_grade"]=pd.DataFrame({"ex":g["ex"].mean(),"n":g.size(),"t":g["ex"].apply(lambda s:s.mean()/s.std()*np.sqrt(len(s)))})
    # condition check: vr>1 without signal (xw==0) vs with
    X["vrh"]=X["vr"]>1; X["sig"]=X["xw"]>0
    g=X.dropna(subset=["vr"]).groupby(["vrh","sig"])
    out["vr_vs_signal"]=pd.DataFrame({"ex":g["ex"].mean(),"n":g.size(),"t":g["ex"].apply(lambda s:s.mean()/s.std()*np.sqrt(len(s)))})
    # 60d trend profile with signal
    X["tr"]=pd.cut(X["r60"],[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    g=X.dropna(subset=["tr"]).groupby(["tr","sig"])
    out["trend60_signal"]=pd.DataFrame({"ex":g["ex"].mean(),"n":g.size(),"t":g["ex"].apply(lambda s:s.mean()/s.std()*np.sqrt(len(s)))})
    # wide day close near high (opposite side)
    X["hi"]=(1-X["depth"])*(X["mult"]-1).clip(lower=0)
    X["hq"]=np.where(X["hi"]>0, pd.qcut(X["hi"].where(X["hi"]>0).rank(method="first"),4,labels=False), -1)
    g=X.groupby("hq")
    out["wide_high_close_grade"]=pd.DataFrame({"ex":g["ex"].mean(),"n":g.size(),"t":g["ex"].apply(lambda s:s.mean()/s.std()*np.sqrt(len(s)))})
    return out
