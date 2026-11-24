def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    wins = sorted(bars[coins[0]].keys(), key=lambda w: int(w[1:]))
    rows = []
    for c in coins:
        for w in wins:
            b = bars[c].get(w)
            if b is None: continue
            b = b.reset_index(drop=True)
            cl = b.close; r = cl.pct_change()
            vol20 = r.rolling(20).std()
            ret5 = cl/cl.shift(5)-1
            ret20 = cl/cl.shift(20)-1
            ret3 = cl/cl.shift(3)-1
            dd20 = cl/cl.rolling(20).max()-1
            df = pd.DataFrame({"c": c, "w": w, "pos": range(len(b)), "f": b.forecast,
                "alloc": b.postRebalance_current_allocation, "vol20": vol20,
                "ret5": ret5, "ret3": ret3, "ret20": ret20, "dd20": dd20,
                "r5s": ret5/(vol20*np.sqrt(5)),
                "fwd10": cl.shift(-10)/cl-1, "fwd1": cl.shift(-1)/cl-1})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.pos % 10 == 0].groupby("c").fwd10.mean()
    A["ab10"] = A.fwd10 - A.c.map(drift)
    A["gain"] = A.alloc*A.fwd1
    out = {}
    G = A[A.pos % 10 == 0].dropna(subset=["fwd10","ret5","vol20"]).copy()
    G["on"] = G.f > 0
    def summ(x):
        return pd.Series({"n": len(x), "fwd10": x.fwd10.mean(), "ab10": x.ab10.mean(),
            "t": x.ab10.mean()/(x.ab10.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    G["r5q"] = G.groupby("c").ret5.transform(lambda x: pd.qcut(x,3,labels=False))
    out["r5_on"] = G[G.on].groupby("r5q").apply(summ)
    out["r5_off"] = G[~G.on].groupby("r5q").apply(summ)
    G["dq"] = G.groupby("c").dd20.transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=False))
    out["dd20_on"] = G[G.on].groupby("dq").apply(summ)
    out["dd20_off"] = G[~G.on].groupby("dq").apply(summ)
    # sign of 5-day return while on
    out["on_ret5pos"] = G[G.on].groupby(G[G.on].ret5 > 0).apply(summ)
    out["off_ret5pos"] = G[~G.on].groupby(G[~G.on].ret5 > 0).apply(summ)
    # daily: book gain by ret5 sign while held
    H = A[(A.alloc > 0)].dropna(subset=["gain","ret5"])
    out["held_daily_by_r5sign"] = H.groupby(H.ret5 > 0).agg(n=("gain","size"), gain=("gain","mean"), sd=("gain","std"), fwd1=("fwd1","mean"))
    # simulated books: daily gain per coin, mean over coins, chained
    def book(mask):
        A["g2"] = np.where(mask, A.gain, 0.0)
        res = []
        for w in wins:
            s = A[A.w == w].groupby("pos").g2.mean().dropna()
            res.append(s.values)
        r = np.concatenate(res); r = r[~np.isnan(r)]
        v = np.cumprod(1+r); mdd = (v/np.maximum.accumulate(v)-1).min()
        yr = v[-1]**(365/len(r))-1
        return pd.Series({"yr": yr, "mdd": mdd, "calmar": yr/abs(mdd), "sharpe": r.mean()/r.std()*np.sqrt(365)})
    out["sim_base"] = book(np.ones(len(A), bool))
    out["sim_r5pos"] = book((A.ret5 > 0).values)
    out["sim_r3pos"] = book((A.ret3 > 0).values)
    out["sim_dd20_gt-10"] = book((A.dd20 > -0.10).values)
    out["sim_dd20_gt-05"] = book((A.dd20 > -0.05).values)
    return out
