def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # ---- book daily returns, chained in window order
    days = data["days"]
    coins = list(days.keys())
    wins = list(days[coins[0]].keys())
    def wkey(w): return int(w[1:])
    wins = sorted(wins, key=wkey)
    rows = []
    for w in wins:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day","book_return","coin_return"]].copy()
                d["coin"] = c
                frames.append(d)
        f = pd.concat(frames)
        g = f.groupby("day").agg(book=("book_return","mean"), hold=("coin_return","mean")).reset_index()
        g["w"] = w
        g = g.sort_values("day")
        rows.append(g)
    B = pd.concat(rows, ignore_index=True).dropna(subset=["book"])
    B["year"] = pd.to_datetime(B["day"]).dt.year
    v = (1+B["book"]).cumprod()
    dd = v/v.cummax()-1
    B["dd"] = dd.values
    # drawdown episodes
    trough = int(np.argmin(dd.values))
    peak = int(np.argmax(v.values[:trough+1]))
    out["deepest fall"] = pd.Series({"depth": dd.min(), "days peak->trough": trough-peak,
                                     "window at peak": B["w"].iloc[peak], "window at trough": B["w"].iloc[trough],
                                     "year trough": B["year"].iloc[trough],
                                     "hold return over fall": (1+B["hold"].iloc[peak+1:trough+1]).prod()-1,
                                     "book return over fall": (1+B["book"].iloc[peak+1:trough+1]).prod()-1})
    # per window book vs hold
    out["by window"] = B.groupby("w").agg(book=("book", lambda x:(1+x).prod()-1), hold=("hold", lambda x:(1+x).prod()-1), mindd=("dd","min")).reindex(wins)
    # ---- bar-level features
    recs = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.sort_values("timestamp")
            cl = b["close"].astype(float)
            r = cl.pct_change()
            df = pd.DataFrame({
                "fc": b["forecast"].values,
                "alloc": b["postRebalance_current_allocation"].values,
                "r1": r.values,
                "fwd": (cl.shift(-1)/cl-1).values,
                "ret20": (cl/cl.shift(20)-1).values,
                "vol30": r.rolling(30).std().values,
                "vol7": r.rolling(7).std().values,
                "r5": (cl/cl.shift(5)-1).values,
            })
            df["coin"] = c; df["w"] = w
            df["ts"] = b["timestamp"].values
            recs.append(df)
    D = pd.concat(recs, ignore_index=True)
    D["gain"] = D["alloc"]*D["fwd"]
    cm = D.groupby("coin")["fwd"].mean()
    D["ex"] = D["fwd"] - D["coin"].map(cm)
    D["sig"] = D["fc"] > 0
    out["position stats"] = pd.Series({"share alloc>0": (D["alloc"]>0).mean(), "share sig": D["sig"].mean(),
        "share alloc>0 & not sig": ((D["alloc"]>0)&(~D["sig"])).mean(),
        "mean alloc when sig": D.loc[D.sig,"alloc"].mean(), "mean alloc not sig": D.loc[~D.sig,"alloc"].mean(),
        "gain/bar sig": D.loc[D.sig,"gain"].mean(), "gain/bar not sig (held)": D.loc[(~D.sig)&(D.alloc>0),"gain"].mean()})
    # forecast bins
    D["fcbin"] = pd.cut(D["fc"], [-0.01,0,4,8,12,16,20.01])
    out["by forecast bin"] = D.dropna(subset=["fwd"]).groupby("fcbin", observed=True).agg(n=("ex","size"), ex=("ex","mean"), fwd=("fwd","mean"), gain=("gain","mean"), alloc=("alloc","mean"))
    # trend condition
    E = D.dropna(subset=["fwd","ret20"]).copy()
    E["trend_q"] = pd.qcut(E["ret20"], 5, labels=["q1 down","q2","q3","q4","q5 up"])
    out["by 20d trend x sig"] = E.groupby(["trend_q","sig"], observed=True).agg(n=("ex","size"), ex=("ex","mean"), fwd=("fwd","mean"), gain=("gain","mean"), gainstd=("gain","std")).unstack()
    E2 = D.dropna(subset=["fwd","vol30","vol7"]).copy()
    E2["volratio_q"] = pd.qcut(E2["vol7"]/E2["vol30"], 4, labels=["calm","2","3","hot"])
    out["by vol7/vol30 x sig"] = E2.groupby(["volratio_q","sig"], observed=True).agg(n=("ex","size"), ex=("ex","mean"), gain=("gain","mean"), gainstd=("gain","std")).unstack()
    # worst book days: what was held
    D["year"] = pd.to_datetime(D["ts"]).dt.year
    out["by year sig"] = D[D.sig].dropna(subset=["fwd"]).groupby("year").agg(n=("ex","size"), ex=("ex","mean"), gain=("gain","mean"))
    return out
