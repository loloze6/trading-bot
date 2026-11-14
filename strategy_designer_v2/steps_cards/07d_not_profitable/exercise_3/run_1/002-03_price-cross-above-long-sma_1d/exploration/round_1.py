def explore(data):
    import pandas as pd, numpy as np
    out = {}
    # portfolio daily returns
    frames = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            x = d[["day","book_return","coin_return"]].copy(); x["coin"]=c; x["w"]=w
            frames.append(x)
    D = pd.concat(frames)
    D["wn"] = D["w"].str[1:].astype(int)
    P = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().reset_index().sort_values(["wn","day"])
    P = P.dropna(subset=["book_return"])
    eq = (1+P["book_return"]).cumprod(); dd = eq/eq.cummax()-1
    P["dd"]=dd.values
    out["book per window"] = P.groupby("wn").agg(book=("book_return",lambda r:(1+r).prod()-1),
        hold=("coin_return",lambda r:(1+r).prod()-1), mindd=("dd","min"), n=("book_return","size")).round(3)
    out["overall maxdd"] = float(dd.min())
    # bar-level state analysis
    rows=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.copy()
            cl=b["close"]; a=b["postRebalance_current_allocation"]
            b["g"]=a*(cl.shift(-1)/cl-1)
            b["r1"]=cl.shift(-1)/cl-1
            b["dist"]=b["debug_info.components.above_ma.last_history_value"]
            b["past20"]=cl/cl.shift(20)-1
            b["dd60"]=cl/cl.rolling(60,min_periods=10).max()-1
            b["vol20"]=cl.pct_change().rolling(20).std()
            b["fc"]=b["forecast"]; b["a"]=a; b["coin"]=c
            rows.append(b[["g","r1","dist","past20","dd60","vol20","fc","a","coin"]])
    B=pd.concat(rows); L=B[B["a"]>0].dropna()
    def tab(col,q=5):
        L["q"]=pd.qcut(L[col],q,duplicates="drop")
        t=L.groupby("q").agg(n=("g","size"),gain=("g","mean"),r1=("r1","mean"),sd=("g","std"),a=("a","mean"))
        t["sh"]=t["gain"]/t["sd"]*np.sqrt(365)
        return t.round(5)
    out["long by fc"]=tab("fc"); out["long by dist"]=tab("dist")
    out["long by past20"]=tab("past20"); out["long by dd60"]=tab("dd60"); out["long by vol20"]=tab("vol20")
    out["coin mean r1 all"]=float(B["r1"].mean())
    out["share long bars"]=float((B["a"]>0).mean())
    return out
