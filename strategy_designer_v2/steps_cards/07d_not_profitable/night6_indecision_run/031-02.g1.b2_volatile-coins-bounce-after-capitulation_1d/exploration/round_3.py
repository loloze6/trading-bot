import pandas as pd, numpy as np

def explore(data):
    out = {}
    bars = data["bars"]
    cs = []; allret = {}
    for c in bars:
        allret[c] = pd.concat([b["close"].pct_change().dropna() for b in bars[c].values()]).mean()
        for w, b in bars[c].items():
            b = b.copy().reset_index(drop=True)
            r = b["close"].pct_change(); sd = r.rolling(20).std()
            b["r1"] = r; b["z"] = r/sd
            b["n1"] = b["close"].shift(-1)/b["close"]-1
            b["n2"] = b["close"].shift(-2)/b["close"]-1
            b["r5"] = b["close"]/b["close"].shift(5)-1
            b["prior4"] = (1+b["r5"])/(1+r)-1
            b["r20"] = b["close"]/b["close"].shift(20)-1
            b["volrel"] = sd/sd.rolling(60, min_periods=20).mean()
            b["deep_prev"] = (b["z"].shift(1) <= -2) | (b["z"].shift(2) <= -2) | (b["z"].shift(3) <= -2)
            b["alloc"] = b["postRebalance_current_allocation"]
            b["case"] = b["regime"] == "mean_reversion"
            b["coin"] = c; b["wn"] = int(w[1:])
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["drift"] = allret[c]
            cs.append(b)
    A = pd.concat(cs, ignore_index=True)
    A["ex1"] = A["n1"] - A["drift"]
    C = A[A["case"] & A["n1"].notna()].copy()
    ncoins = 6; cost = 0.0019
    allday = A.groupby(["wn","day"]).size().index
    def book(x, size):
        g = size*x["n1"] - cost*size
        daily = g.groupby([x["wn"], x["day"]]).sum()/ncoins
        s = pd.Series(0.0, index=allday); s.loc[daily.index] = daily.values
        s = s.sort_index(); v = (1+s).cumprod(); mdd = (v/v.cummax()-1).min()
        yr = v.iloc[-1]**(365/len(s))-1
        return {"n": len(x), "yearly": yr, "maxdd": mdd, "calmar": yr/abs(mdd), "sharpe": s.mean()/s.std()*np.sqrt(365), "worstday": s.min()}
    res = {}
    res["actual"] = book(C, C["alloc"])
    res["cap1.0"] = book(C, C["alloc"].clip(upper=1.0))
    res["cap0.8"] = book(C, C["alloc"].clip(upper=0.8))
    res["flat0.55"] = book(C, pd.Series(0.55, index=C.index))
    x = C[C["deep_prev"]]; res["deep_prev"] = book(x, x["alloc"])
    x = C[~C["deep_prev"]]; res["no_deep_prev"] = book(x, x["alloc"])
    x = C[C["prior4"] < -0.03]; res["prior4<-3%"] = book(x, x["alloc"])
    x = C[C["prior4"] >= -0.03]; res["prior4>=-3%"] = book(x, x["alloc"])
    out["sim"] = pd.DataFrame(res).T
    C["p4b"] = pd.qcut(C["prior4"], 3).astype(str)
    r = C.groupby("p4b").agg(n=("ex1","size"), mean=("ex1","mean"), sd=("ex1","std"), n2=("n2","mean"))
    r["t"] = r["mean"]/(r["sd"]/np.sqrt(r["n"])); out["by prior4"] = r
    r = C.groupby("deep_prev").agg(n=("ex1","size"), mean=("ex1","mean"), sd=("ex1","std"))
    r["t"] = r["mean"]/(r["sd"]/np.sqrt(r["n"])); out["by deep_prev"] = r
    g = A[A["n1"].notna() & ~A["case"] & A["deep_prev"]]["ex1"]
    out["deep_prev alone"] = pd.Series({"n": len(g), "mean": g.mean(), "t": g.mean()/(g.std()/np.sqrt(len(g)))})
    return out
