import numpy as np, pandas as pd

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    wins = sorted({w for c in coins for w in bars[c]}, key=lambda s: int(s[1:]))
    # book daily
    rows = []
    for c in coins:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().reset_index().sort_values(["wn","day"])
    B = B.dropna()
    v = (1+B["book_return"]).cumprod(); peak = v.cummax(); dd = v/peak-1
    B["dd"] = dd.values
    yr = v.iloc[-1]**(365/len(B))-1
    out["book summary"] = pd.Series({"days":len(B),"yearly":yr,"maxdd":dd.min(),"calmar":yr/-dd.min(),
        "sharpe":B.book_return.mean()/B.book_return.std()*np.sqrt(365)})
    # drawdown episodes
    B["peakpos"] = (v==peak).values
    ep = (B["peakpos"]).cumsum().values
    B["ep"] = ep
    E = B.groupby("ep").agg(depth=("dd","min"), ndays=("dd","size"),
                           w_first=("wn","min"), w_last=("wn","max"),
                           coin_ret=("coin_return", lambda x: (1+x).prod()-1))
    out["deepest falls"] = E.sort_values("depth").head(8)
    # per window
    W = B.groupby("wn").agg(book=("book_return", lambda x:(1+x).prod()-1),
                            hold=("coin_return", lambda x:(1+x).prod()-1),
                            worst_dd=("dd","min"))
    out["per window"] = W
    # bar-level features
    feats = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.copy()
            cl = b["close"]; r = cl.pct_change()
            b["r1"] = r
            b["vol20"] = r.rolling(20).std()
            b["z"] = r/b["vol20"]
            b["r90"] = cl/cl.shift(90)-1
            b["r30"] = cl/cl.shift(30)-1
            b["r10p"] = cl/cl.shift(10)-1
            b["dd60"] = cl/cl.rolling(60).max()-1
            b["fwd10"] = cl.shift(-10)/cl-1
            b["gain"] = b["postRebalance_current_allocation"]*(cl.shift(-1)/cl-1)
            b["pos"] = np.arange(len(b))
            b["coin"] = c; b["wn"] = int(w[1:])
            feats.append(b)
    F = pd.concat(feats)
    # drift per coin
    grid = F[F.pos % 10 == 0]
    drift = grid.groupby("coin")["fwd10"].mean()
    F["un10"] = F["fwd10"] - F["coin"].map(drift)
    F["cell"] = F.pos//10
    cases = F[F.forecast >= 2].groupby(["coin","wn","cell"]).head(1).dropna(subset=["un10"])
    out["n cases"] = len(cases)
    def grp(col, q=4):
        x = cases.dropna(subset=[col]).copy()
        x["b"] = pd.qcut(x[col], q, labels=False, duplicates="drop")
        g = x.groupby("b").agg(lo=(col,"min"), hi=(col,"max"), n=("un10","size"),
                               un=("un10","mean"), tot=("fwd10","mean"),
                               t=("un10", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))))
        return g
    out["cases by r90"] = grp("r90")
    out["cases by vol20"] = grp("vol20")
    out["cases by z"] = grp("z")
    out["cases by r30"] = grp("r30")
    out["cases by dd60"] = grp("dd60")
    # daily gain by r90 quintile of held bars
    H = F[F.postRebalance_current_allocation.abs() > 0].dropna(subset=["r90","gain"]).copy()
    H["b"] = pd.qcut(H["r90"], 5, labels=False)
    out["held bar gain by r90"] = H.groupby("b").agg(lo=("r90","min"), hi=("r90","max"), n=("gain","size"),
        mean_gain=("gain","mean"), sd=("gain","std"), alloc=("postRebalance_current_allocation","mean"))
    H["vb"] = pd.qcut(H["vol20"], 5, labels=False)
    out["held bar gain by vol20"] = H.groupby("vb").agg(lo=("vol20","min"), hi=("vol20","max"), n=("gain","size"),
        mean_gain=("gain","mean"), sd=("gain","std"))
    out["coin share held"] = F.groupby("coin").apply(lambda x: pd.Series({"held": (x.postRebalance_current_allocation.abs()>0).mean(),
        "mean_gain": x.gain.mean(), "sd": x.gain.std()}))
    return out
