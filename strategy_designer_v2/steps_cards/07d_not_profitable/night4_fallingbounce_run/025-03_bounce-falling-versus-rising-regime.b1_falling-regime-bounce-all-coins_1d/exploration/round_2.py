import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b["timestamp"])
            b["day"] = b["ts"].dt.floor("D")
            b["ret1"] = b["close"].pct_change()
            b["next"] = b["close"].shift(-1) / b["close"] - 1
            b["fwd5"] = b["close"].shift(-5) / b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["next"]
            b["ret90"] = b["close"] / b["close"].shift(90) - 1
            b["ret30"] = b["close"] / b["close"].shift(30) - 1
            b["ret10"] = b["close"] / b["close"].shift(10) - 1
            b["off_low90"] = b["close"] / b["close"].rolling(90).min() - 1
            b["coin"] = coin; b["wn"] = int(w[1:])
            b["side"] = np.sign(b["pos"].fillna(0))
            b["i"] = np.arange(len(b))
            b["bv_ret"] = b["postRebalance_total_value"].pct_change()
            rows.append(b)
    B = pd.concat(rows)
    # book chain and the deepest episode: decompose losses by side
    book = B.dropna(subset=["bv_ret"]).groupby(["wn","day"])["bv_ret"].mean().sort_index()
    eq = (1+book).cumprod(); dd = eq/eq.cummax()-1
    trough = dd.idxmin(); peak = eq.loc[:trough].idxmax()
    lo = book.index.get_loc(peak); hi = book.index.get_loc(trough)
    ep_idx = book.index[lo:hi+1]
    Bi = B.set_index(["wn","day"])
    E = Bi[Bi.index.isin(ep_idx)]
    gl = E["gain"].where(E["side"]>0,0); gs = E["gain"].where(E["side"]<0,0)
    gd = pd.DataFrame({"long":gl,"short":gs}).groupby(level=[0,1]).mean()
    out["deepest_ep_sum_gain_by_side"] = gd.sum()
    # short gain grades
    S = B[B["side"]<0].dropna(subset=["next","ret30","ret90","off_low90"])
    def grade(df, col, q=5):
        g = df.groupby(pd.qcut(df[col], q, labels=False))
        r = g["gain"].agg(["mean","std","count"])
        r["t"] = r["mean"]/(r["std"]/np.sqrt(r["count"]))
        r["col_mean"] = g[col].mean()
        return r
    out["short_by_ret30"] = grade(S,"ret30")
    out["short_by_ret90"] = grade(S,"ret90")
    out["short_by_off_low90"] = grade(S,"off_low90")
    out["short_by_ret10"] = grade(S,"ret10")
    L = B[B["side"]>0].dropna(subset=["next","ret30","ret90"])
    out["long_by_ret90"] = grade(L,"ret90")
    # signal-level (non-overlapping 5-day grid) in falling regime: fwd5 by off_low90 quintile
    G = B[(B["i"]%5==0)&(B["regime"]=="mean_reversion")].dropna(subset=["fwd5","off_low90"])
    fv = B.groupby("coin")["fwd5"].mean()
    G = G[G["forecast"]<=-2].copy()
    G["unus"] = G["fwd5"] - G["coin"].map(fv)
    g = G.groupby(pd.qcut(G["off_low90"],4,labels=False))
    r = g["unus"].agg(["mean","std","count"]); r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"])); r["x"]=g["off_low90"].mean()
    out["short_signals_fwd5_by_off_low90"] = r
    G2 = B[(B["i"]%5==0)&(B["regime"]=="mean_reversion")&(B["forecast"]<=-2)].dropna(subset=["fwd5","ret30"]).copy()
    G2["unus"] = G2["fwd5"] - G2["coin"].map(fv)
    g = G2.groupby(pd.qcut(G2["ret30"],4,labels=False))
    r = g["unus"].agg(["mean","std","count"]); r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"])); r["x"]=g["ret30"].mean()
    out["short_signals_fwd5_by_ret30"] = r
    return out
