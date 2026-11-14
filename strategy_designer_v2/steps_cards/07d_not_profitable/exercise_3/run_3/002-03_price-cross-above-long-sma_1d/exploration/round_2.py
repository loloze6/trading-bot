def explore(data):
    import pandas as pd, numpy as np
    out = {}
    B = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            cl = b["close"]
            b["r1"] = cl.shift(-1) / cl - 1
            a = b["postRebalance_current_allocation"]
            b["a"] = a
            b["gain"] = a * b["r1"]
            b["dist"] = b["debug_info.components.above_ma.last_history_value"]
            b["past20"] = cl / cl.shift(20) - 1
            b["fwd20"] = cl.shift(-20) / cl - 1
            b["dd60"] = cl / cl.rolling(60).max() - 1
            b["dd20"] = cl / cl.rolling(20).max() - 1
            b["sma20"] = cl / cl.rolling(20).mean() - 1
            b["sma50"] = cl / cl.rolling(50).mean() - 1
            b["coin"] = c; b["wn"] = int(w[1:]); b["pos"] = np.arange(len(b))
            b["t"] = np.arange(len(b))
            b["ts"] = b["timestamp"]
            B.append(b[["coin","wn","pos","ts","forecast","a","r1","gain","dist","past20","fwd20","dd60","dd20","sma20","sma50"]])
    B = pd.concat(B).dropna(subset=["gain"])
    def chain(df, col):
        P = df.groupby(["wn","ts"])[col].mean().reset_index().sort_values(["wn","ts"])
        eq = (1+P[col]).cumprod(); dd = eq/eq.cummax()-1
        ann = eq.iloc[-1]**(365/len(P))-1
        return P, dd, ann
    P, dd, ann = chain(B, "gain")
    P["dd"] = dd.values
    out["approx_book"] = f"ann {ann:.3f} maxdd {dd.min():.3f} calmar {ann/-dd.min():.3f}"
    # deepest fall episode: from peak to trough
    i_tr = dd.values.argmin(); eqv = (1+P["gain"]).cumprod().values
    i_pk = int(np.argmax(eqv[:i_tr+1]))
    ep = P.iloc[i_pk:i_tr+1]
    out["episode_windows"] = ep.groupby("wn").agg(days=("gain","size"), ret=("gain", lambda x:(1+x).prod()-1)).round(3)
    keys = set(zip(ep["wn"], ep["ts"]))
    E = B[[k in keys for k in zip(B["wn"], B["ts"])]]
    out["episode_by_coin"] = E.groupby("coin").agg(sumgain=("gain","sum"), meana=("a","mean"), coinret=("r1","sum"), dist=("dist","mean"), dd60=("dd60","mean"), sma20=("sma20","mean")).round(3)
    # variants
    A = B[B["a"]>0]
    for col in ["sma20","sma50","dd20"]:
        q = pd.qcut(A[col], 5, duplicates="drop")
        g = A.groupby(q)["gain"].agg(["count","mean","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
        out["gain_by_"+col] = g.round(5)
    res = {}
    for name, m in {
        "base": pd.Series(1.0, index=B.index),
        "only_close_above_sma20": (B["sma20"]>0).astype(float),
        "only_close_above_sma50": (B["sma50"]>0).astype(float),
        "scale_by_1+dd60": (1+2*B["dd60"]).clip(lower=0).fillna(1),
        "only_past20_pos": (B["past20"]>0).astype(float),
        "cap_forecast_half": (np.minimum(B["forecast"],10)/B["forecast"].replace(0,np.nan)).fillna(0),
    }.items():
        B["v"] = B["gain"]*m
        _, d2, a2 = chain(B, "v")
        res[name] = {"ann": round(a2,4), "maxdd": round(d2.min(),4), "calmar": round(a2/-d2.min(),3), "active": round(float(((B["a"]*m)>0).mean()),3)}
    out["variants"] = pd.DataFrame(res).T
    # by coin, by window drawdown approx
    out["by_coin"] = B.groupby("coin").agg(sum=("gain","sum"), mean=("gain","mean"), std=("gain","std")).round(4)
    return out
