import numpy as np
import pandas as pd

def explore(data):
    bars = data["bars"]; out = {}
    rb = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy(); cl = b["close"]
            b["r1"] = cl.shift(-1) / cl - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["r1"]
            hi = cl.rolling(30).max(); lo = cl.rolling(30).min()
            b["rpos"] = (cl - (hi + lo) / 2) / ((hi - lo) / 2)
            b["width"] = (hi - lo) / ((hi + lo) / 2)
            b["ret30"] = cl / cl.shift(30) - 1
            b["fwd10"] = cl.shift(-10) / cl - 1
            b["i"] = np.arange(len(b)); b["coin"] = c; b["wn"] = int(w[1:])
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rb.append(b[["coin","wn","i","day","pos","gain","r1","rpos","width","ret30","fwd10","forecast"]])
    B = pd.concat(rb)
    # long-only and short-only books (gain per bar, averaged over coins per day)
    B["gL"] = B["gain"].where(B["pos"] > 0, 0.0); B["gS"] = B["gain"].where(B["pos"] < 0, 0.0)
    B["hold"] = B["r1"]
    d = B.groupby(["wn","day"])[["gain","gL","gS","hold"]].mean().dropna()
    def stat(x):
        eq = (1 + x).cumprod(); dd = (eq / eq.cummax() - 1).min()
        yr = eq.iloc[-1] ** (365 / len(x)) - 1
        return pd.Series({"mean": x.mean(), "sharpe": x.mean()/x.std()*np.sqrt(365), "maxdd": dd, "calmar": yr/abs(dd)})
    out["books_split"] = pd.DataFrame({k: stat(d[k]) for k in ["gain","gL","gS","hold"]}).T
    out["short_gain_by_window"] = d.groupby("wn")[["gL","gS","hold"]].mean()
    # grid: graded effect by rpos bins, and by width on each side
    G = B[B["i"] % 10 == 0].dropna(subset=["fwd10","rpos","width"]).copy()
    G["ex"] = G["fwd10"] - G.groupby("coin")["fwd10"].transform("mean")
    G["rbin"] = pd.cut(G["rpos"], [-1.01,-0.6,-0.2,0.2,0.6,1.01])
    f = lambda x: pd.Series({"n": len(x), "ex": x["ex"].mean(), "t": x["ex"].mean()/x["ex"].std()*np.sqrt(len(x)), "raw": x["fwd10"].mean()})
    out["fwd10_by_rpos"] = G.groupby("rbin").apply(f)
    G["wid"] = pd.qcut(G["width"], 3, labels=["narrow","mid","wide"])
    G["half"] = np.where(G["rpos"] > 0, "upper", "lower")
    out["fwd10_by_half_x_width"] = G.groupby(["half","wid"]).apply(f)
    U = G[G["rpos"] > 0]
    out["upper_corr_rpos_ex"] = float(U[["rpos","ex"]].corr().iloc[0,1])
    U2 = U.copy(); U2["wt"] = U2["width"] * U2["rpos"]
    out["upper_corr_rposXwidth_ex"] = float(U2[["wt","ex"]].corr().iloc[0,1])
    return out
