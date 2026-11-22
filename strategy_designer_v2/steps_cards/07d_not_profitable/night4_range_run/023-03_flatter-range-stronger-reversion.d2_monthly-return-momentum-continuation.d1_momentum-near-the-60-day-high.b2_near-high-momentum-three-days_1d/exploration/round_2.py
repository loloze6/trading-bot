import pandas as pd, numpy as np

def explore(data):
    out = {}
    bars = data["bars"]
    br = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy(); cl = b["close"]
            b["nxt"] = cl.shift(-1)/cl - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"]*b["nxt"]
            b["ret30"] = cl/cl.shift(30)-1
            b["ret3"] = cl/cl.shift(3)-1
            b["ret90"] = cl/cl.shift(90)-1
            b["dist60"] = cl/cl.rolling(60, min_periods=30).max()-1
            b["vol20"] = cl.pct_change().rolling(20).std()
            b["vol60"] = cl.pct_change().rolling(60).std()
            b["coin"] = c; b["win"] = w
            b["early"] = int(w[1:]) <= 8
            br.append(b)
    B = pd.concat(br).dropna(subset=["gain"])
    B["side"] = np.sign(B["pos"])
    A = B[B.pos != 0]
    def st(x):
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, "sum": x.sum()})
    out["early(w1-8) vs rest by side"] = A.groupby(["early","side"])["gain"].apply(st).unstack()
    out["mean |pos| early vs rest by side"] = A.groupby(["early","side"])["pos"].apply(lambda x: x.abs().mean()).unstack()
    L = A[A.side == 1].dropna(subset=["ret30","dist60"])
    L["r30q"] = pd.qcut(L["ret30"], 3, labels=["low","mid","high"])
    L["d60q"] = pd.qcut(L["dist60"], 3, labels=["far","mid","near"])
    out["long gain ret30 x dist60"] = L.groupby(["r30q","d60q"])["gain"].apply(st).unstack()
    out["long gain by dist60 tercile, early vs rest"] = L.groupby(["early","d60q"])["gain"].apply(st).unstack()
    # long near high: after a 3-day fall?
    N = L[L.d60q == "near"].dropna(subset=["ret3"])
    N["r3q"] = pd.qcut(N["ret3"], 4, labels=False)
    out["long near-high gain by ret3 quartile"] = N.groupby("r3q")["gain"].apply(st).unstack()
    # long gain by 90-day return (longer trend) and vol ratio
    L2 = L.dropna(subset=["ret90"])
    out["long gain by ret90 quintile"] = L2.groupby(pd.qcut(L2["ret90"],5,labels=False))["gain"].apply(st).unstack()
    L3 = L.dropna(subset=["vol20","vol60"]).copy()
    L3["vr"] = L3["vol20"]/L3["vol60"]
    out["long gain by vol20/vol60 quintile"] = L3.groupby(pd.qcut(L3["vr"],5,labels=False))["gain"].apply(st).unstack()
    out["long gain by vol60 quintile"] = L3.groupby(pd.qcut(L3["vol60"],5,labels=False))["gain"].apply(st).unstack()
    S = A[A.side == -1].dropna(subset=["ret30","dist60"])
    out["short gain by dist60 tercile"] = S.groupby(pd.qcut(S["dist60"],3,labels=["far","mid","near"]))["gain"].apply(st).unstack()
    # bars by side share by window early vs rest, with coin ret
    out["share long, early vs rest"] = B.groupby("early")["side"].apply(lambda s: (s==1).mean())
    return out
