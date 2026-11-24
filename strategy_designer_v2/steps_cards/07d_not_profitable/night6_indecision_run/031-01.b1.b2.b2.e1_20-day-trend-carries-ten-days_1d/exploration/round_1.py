def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    days = data["days"]; bars = data["bars"]
    coins = list(bars.keys())
    wins = sorted(bars[coins[0]].keys(), key=lambda w: int(w[1:]))
    out = {}
    # book daily
    chain = []
    for w in wins:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w].set_index("day")["book_return"]
                frames.append(d.rename(c))
        df = pd.concat(frames, axis=1)
        s = df.mean(axis=1).dropna()
        chain.append(pd.DataFrame({"w": w, "r": s.values, "i": range(len(s))}))
    ch = pd.concat(chain, ignore_index=True)
    v = (1 + ch.r).cumprod()
    peak = v.cummax(); dd = v / peak - 1
    ch["dd"] = dd.values
    # window-level stats
    g = ch.groupby("w", sort=False).agg(ret=("r", lambda x: (1+x).prod()-1), mindd=("dd", "min"), n=("r","size"))
    g["winfall"] = ch.groupby("w", sort=False)["r"].apply(lambda x: ((1+x).cumprod()/(1+x).cumprod().cummax()-1).min())
    out["windows"] = g
    out["maxdd"] = float(dd.min())
    # features per coin bar
    rows = []
    for c in coins:
        for w in wins:
            b = bars[c].get(w)
            if b is None: continue
            b = b.reset_index(drop=True)
            cl = b.close; r = cl.pct_change()
            vol20 = r.rolling(20).std()
            rng = (b.high - b.low) / cl.shift(1)
            body = (b.close - b.open).abs() / (b.high - b.low).replace(0, np.nan)
            wide = rng / rng.rolling(20).mean()
            # wide flat day: range ratio * (1-body)
            wf = (wide * (1 - body))
            wfmax5 = wf.rolling(5).max()
            ret20 = cl / cl.shift(20) - 1
            ret5 = cl / cl.shift(5) - 1
            fwd10 = cl.shift(-10) / cl - 1
            fwd1 = cl.shift(-1)/cl - 1
            alloc = b.postRebalance_current_allocation
            df = pd.DataFrame({"c": c, "w": w, "pos": range(len(b)), "f": b.forecast, "alloc": alloc,
                               "vol20": vol20, "ret20": ret20, "ret5": ret5, "wf": wf, "wfmax5": wfmax5,
                               "wide": wide, "fwd10": fwd10, "fwd1": fwd1, "gain": alloc * fwd1})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.pos % 10 == 0].groupby("c").fwd10.mean()
    A["ab10"] = A.fwd10 - A.c.map(drift)
    G = A[(A.pos % 10 == 0)].dropna(subset=["fwd10", "ret20", "vol20", "wfmax5"])
    G = G.copy()
    G["on"] = G.f > 0
    def summ(x):
        return pd.Series({"n": len(x), "fwd10": x.fwd10.mean(), "ab10": x.ab10.mean(),
                          "t": x.ab10.mean() / (x.ab10.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    # forecast bins
    G["fbin"] = pd.cut(G.f, [-0.1, 0, 5, 10, 15, 20.1])
    out["by_forecast"] = G.groupby("fbin", observed=True).apply(summ)
    # vol tercile
    G["volq"] = G.groupby("c").vol20.transform(lambda x: pd.qcut(x, 3, labels=False))
    out["by_vol_on"] = G[G.on].groupby("volq").apply(summ)
    out["by_vol_off"] = G[~G.on].groupby("volq").apply(summ)
    # wide flat day in last 5
    G["wfq"] = G.groupby("c").wfmax5.transform(lambda x: pd.qcut(x, 3, labels=False))
    out["by_wf_on"] = G[G.on].groupby("wfq").apply(summ)
    out["by_wf_off"] = G[~G.on].groupby("wfq").apply(summ)
    # ret5 tercile while on (recent spike)
    G["r5q"] = G.groupby("c").ret5.transform(lambda x: pd.qcut(x, 3, labels=False))
    out["by_r5_on"] = G[G.on].groupby("r5q").apply(summ)
    # gain on days by book drawdown state: worst 20 days
    A2 = A.dropna(subset=["gain"])
    out["gain_by_volq_alloc"] = A2.assign(vq=A2.groupby("c").vol20.transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))).groupby("vq").agg(gain=("gain", "mean"), sd=("gain", "std"), alloc=("alloc", "mean"))
    # deepest falls: windows with deepest internal falls -> what held
    worst = g.sort_values("winfall").head(5).index.tolist()
    W = A[A.w.isin(worst)].groupby("w").agg(alloc=("alloc", "mean"), f=("f", "mean"), ret20=("ret20", "mean"), vol20=("vol20", "mean"), fwd1=("fwd1","mean"))
    out["worst_windows_state"] = W
    out["all_state"] = A.agg({"alloc": "mean", "f": "mean", "ret20": "mean", "vol20": "mean", "fwd1": "mean"})
    return out
