def explore(data):
    import pandas as pd, numpy as np
    out = {}
    # book daily series
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"]).agg(br=("book_return","mean"), cr=("coin_return","mean")).reset_index().sort_values(["wn","day"])
    B = B.dropna(subset=["br"])
    eq = (1+B["br"]).cumprod()
    peak = eq.cummax(); dd = eq/peak-1
    B["dd"] = dd.values
    out["max_dd"] = float(dd.min())
    out["ann_ret"] = float(eq.iloc[-1]**(365/len(B))-1)
    # drawdown by window: worst dd within window and window return
    g = B.groupby("wn").agg(book=("br", lambda x:(1+x).prod()-1), hold=("cr", lambda x:(1+x).prod()-1), minbr=("br","min"), days=("br","size"))
    out["by_window"] = g.round(4)
    # top episodes of chained dd
    B["ep"] = (B["dd"]==0).cumsum()
    ep = B.groupby("ep").agg(depth=("dd","min"), length=("dd","size"), wstart=("wn","first"), wend=("wn","last"), coin_move=("cr", lambda x:(1+x).prod()-1))
    out["top_episodes"] = ep.sort_values("depth").head(8).round(4)
    # bar-level conditional gain
    R = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            r = b["close"].pct_change()
            b["fwd"] = b["close"].shift(-1)/b["close"]-1
            b["gain"] = b["postRebalance_current_allocation"]*b["fwd"]
            b["ret10"] = b["close"]/b["close"].shift(10)-1
            b["ret30"] = b["close"]/b["close"].shift(30)-1
            b["vol20"] = r.rolling(20).std()
            b["vol_ratio"] = b["vol20"]/r.rolling(60).std()
            b["dd20"] = b["close"]/b["close"].rolling(20).max()-1
            b["coin"]=c
            R.append(b[["gain","fwd","postRebalance_current_allocation","forecast","ret10","ret30","vol20","vol_ratio","dd20","debug_info.bars_in_regime","coin"]])
    R = pd.concat(R)
    L = R[R["postRebalance_current_allocation"]>0].dropna(subset=["gain"])
    out["n_long_bars"] = len(L)
    for col in ["forecast","ret10","ret30","vol20","vol_ratio","dd20","debug_info.bars_in_regime","postRebalance_current_allocation"]:
        x = L.dropna(subset=[col])
        try:
            q = pd.qcut(pd.to_numeric(x[col],errors="coerce"),5,duplicates="drop")
        except Exception as e:
            continue
        out["by_"+col] = x.groupby(q, observed=True)["gain"].agg(["mean","std","count", lambda s:(s<-0.05).mean()]).round(5)
    return out
