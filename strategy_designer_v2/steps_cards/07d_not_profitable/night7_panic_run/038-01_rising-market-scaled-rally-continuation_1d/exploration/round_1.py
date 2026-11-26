import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars, days = data["bars"], data["days"]
    coins = list(bars.keys())
    wins = sorted({w for c in coins for w in bars[c]}, key=lambda s: int(s[1:]))
    # book daily
    rows = []
    for w in wins:
        dfs = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day","book_return","coin_return"]].copy(); d["coin"] = c; dfs.append(d)
        dd = pd.concat(dfs)
        g = dd.groupby("day")[["book_return","coin_return"]].mean().reset_index(); g["win"] = w
        rows.append(g)
    B = pd.concat(rows).dropna(subset=["book_return"]).reset_index(drop=True)
    v = (1 + B["book_return"]).cumprod(); peak = v.cummax(); dd_ = v/peak - 1
    B["dd"] = dd_
    out["calmar_parts"] = pd.Series({"yearly": v.iloc[-1]**(365/len(v))-1, "maxdd": dd_.min(), "days": len(v)})
    # drawdown episodes
    eps = []; inep = False
    for i in range(len(B)):
        if dd_[i] < 0 and not inep: inep = True; st = i - 1 if i > 0 else 0
        if inep and dd_[i] == 0:
            seg = B.iloc[st:i]; trough = seg["dd"].idxmin()
            eps.append((seg["win"].iloc[0], seg["win"].iloc[-1], st, trough, i, seg["dd"].min())); inep = False
    if inep:
        seg = B.iloc[st:]; eps.append((seg["win"].iloc[0], seg["win"].iloc[-1], st, seg["dd"].idxmin(), len(B), seg["dd"].min()))
    E = pd.DataFrame(eps, columns=["w_start","w_end","i0","itrough","iend","depth"]).sort_values("depth").head(6)
    E["days_to_trough"] = E["itrough"] - E["i0"]
    E["coin_ret_mean_to_trough"] = [B["coin_return"].iloc[a+1:b+1].sum() for a,b in zip(E.i0,E.itrough)]
    E["book_ret_sum_to_trough"] = [B["book_return"].iloc[a+1:b+1].sum() for a,b in zip(E.i0,E.itrough)]
    out["deepest_falls"] = E[["w_start","w_end","days_to_trough","depth","coin_ret_mean_to_trough","book_ret_sum_to_trough"]]
    out["by_window_book"] = B.groupby("win").agg(book_mean=("book_return","mean"), book_sum=("book_return","sum"),
                                                coin_sum=("coin_return","sum"), mindd=("dd","min"), n=("dd","size"))
    # case-level features
    cases = []
    allg = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r1 = cl.pct_change()
            f = pd.DataFrame({"coin": c, "win": w, "fc": b["forecast"].fillna(0), "rising": b["regime"] != "chop",
                              "alloc": b["postRebalance_current_allocation"]})
            f["fwd3"] = cl.shift(-3)/cl - 1
            f["r3"] = cl/cl.shift(3) - 1
            f["r1"] = r1
            vol30 = r1.rolling(30, min_periods=20).std()
            f["volratio"] = vol30 / r1.rolling(90, min_periods=60).std()
            f["r20"] = cl/cl.shift(20) - 1
            f["r60"] = cl/cl.shift(60) - 1
            f["fromhigh20"] = cl/cl.rolling(20).max() - 1
            f["z3"] = f["r3"]/(vol30*np.sqrt(3))
            f["range_pos"] = (cl - b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            g = f.iloc[::3].copy()
            allg.append(g)
    G = pd.concat(allg).dropna(subset=["fwd3"])
    drift = G.groupby("coin")["fwd3"].mean()
    G["ex"] = G["fwd3"] - G["coin"].map(drift)
    R = G[G.rising]
    R["sig"] = R.fc > 0
    def summ(x):
        return pd.Series({"n": len(x), "mean_fwd3": x.fwd3.mean(), "mean_ex": x.ex.mean(),
                          "t": x.ex.mean()/(x.ex.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,
                          "share_neg5": (x.fwd3 < -0.05).mean()})
    out["rising_sig_vs_not"] = R.groupby("sig").apply(summ)
    S = R[R.sig].copy()
    out["by_fc_bucket"] = S.groupby(pd.cut(S.fc,[0,5,10,15,20.01])).apply(summ)
    for col, q in [("volratio",4),("r20",4),("r60",4),("fromhigh20",3),("r1",4),("z3",4)]:
        x = R.dropna(subset=[col]).copy()
        x["bin"] = pd.qcut(x[col], q, duplicates="drop")
        out[f"{col}_sig"] = x[x.sig].groupby("bin").apply(summ)
        out[f"{col}_nosig"] = x[~x.sig].groupby("bin").apply(summ)
    out["by_window_sig"] = S.groupby("win").apply(summ)
    out["by_coin_sig"] = S.groupby("coin").apply(summ)
    return out
