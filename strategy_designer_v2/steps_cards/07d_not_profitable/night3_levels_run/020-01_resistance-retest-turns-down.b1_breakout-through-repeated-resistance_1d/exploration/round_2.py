def explore(data):
    import pandas as pd, numpy as np
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    P = []; C = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.copy().reset_index(drop=True)
            lr = np.log(b.close).diff()
            b["r20"] = b.close/b.close.shift(20)-1
            b["r5"] = b.close/b.close.shift(5)-1
            b["vol20"] = lr.rolling(20).std()
            b["vol60"] = lr.rolling(60).std()
            b["vr"] = b.vol20/b.vol60
            b["hi60"] = b.close/b.close.rolling(60).max()-1
            b["nxt"] = b.close.shift(-1)/b.close-1
            b["gain"] = b.postRebalance_current_allocation*b.nxt
            b["fwd10"] = b.close.shift(-10)/b.close-1
            b["coin"]=c; b["w"]=w
            P.append(b[["coin","w","r20","r5","vol20","vr","hi60","gain","postRebalance_current_allocation","nxt"]])
            f = b.forecast.fillna(0)
            ent = (f>0)&(f.shift(1).fillna(0)<=0)
            e = b[ent].copy(); e["fc"]=f[ent]
            C.append(e[["coin","w","r20","r5","vol20","vr","hi60","fwd10","fc"]])
    P = pd.concat(P); C = pd.concat(C).dropna(subset=["fwd10"])
    # normal drift per coin over 10 bars, approx from all bars' mean daily return *10
    drift = P.groupby("coin").nxt.mean()*10
    C["ex"] = C.fwd10 - C.coin.map(drift)
    held = P[P.postRebalance_current_allocation.abs()>0].dropna(subset=["gain"])
    out["held_share"] = pd.Series({"share_bars_held": len(held)/len(P.dropna(subset=['gain'])), "mean_alloc_held": held.postRebalance_current_allocation.mean()})
    for f in ["r20","r5","vr","hi60","vol20"]:
        h = held.dropna(subset=[f])
        q = pd.qcut(h[f],5,duplicates="drop")
        g = h.groupby(q,observed=True).agg(gain_mean=("gain","mean"),gain_sum=("gain","sum"),n=("gain","size"),coin_next=("nxt","mean"),share_loss_lt5=("gain",lambda s:(s<-0.05).mean()))
        g.index=[f"{f}_q{i+1}" for i in range(len(g))]
        out["held_gain_by_"+f]=g
        e = C.dropna(subset=[f]); q2 = pd.qcut(e[f],5,duplicates="drop")
        g2 = e.groupby(q2,observed=True).ex.agg(["mean","count","std","min"]); g2["t"]=g2["mean"]/(g2["std"]/np.sqrt(g2["count"]))
        g2.index=[f"{f}_q{i+1}" for i in range(len(g2))]
        out["entry_ex10_by_"+f]=g2
    # worst 2% held days: state
    thr = held.gain.quantile(0.02)
    worst = held[held.gain<=thr]
    out["worst_days_state_vs_all"] = pd.DataFrame({"worst":worst[["r20","r5","vr","hi60","vol20","postRebalance_current_allocation"]].median(),
                                                   "all_held":held[["r20","r5","vr","hi60","vol20","postRebalance_current_allocation"]].median()})
    out["worst_days_share_of_loss"] = pd.Series({"n":len(worst),"sum_worst":worst.gain.sum(),"sum_all":held.gain.sum()})
    return out
