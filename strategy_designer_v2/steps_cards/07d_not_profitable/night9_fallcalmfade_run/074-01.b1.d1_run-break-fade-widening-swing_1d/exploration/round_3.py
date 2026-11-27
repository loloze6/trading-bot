def explore(data):
    import numpy as np, pandas as pd
    out = {}
    wn = lambda s: int(s[1:])
    cs = []
    ncoins = len(data["bars"])
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r = cl.pct_change()
            df = pd.DataFrame({"coin": c, "w": wn(w), "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                               "n1": cl.shift(-1) / cl - 1, "ret5": cl / cl.shift(5) - 1,
                               "sd30": r.rolling(30).std(),
                               "vr": r.rolling(10).std() / r.rolling(60).std(),
                               "ret60": cl / cl.shift(60) - 1, "up": r})
            df["r5z"] = df.ret5 / (df.sd30 * np.sqrt(5))
            cs.append(df)
    C = pd.concat(cs).reset_index(drop=True)
    C["un1"] = -(C.n1 - C.coin.map(C.groupby("coin")["n1"].mean()))
    K = C[(C.fc < 0) & C.n1.notna()].copy()
    K["pnl"] = K.alloc * K.n1 - K.alloc.abs() * 0.0019
    alldays = C[["w", "day"]].drop_duplicates().sort_values(["w", "day"])
    def proxy(mask, name):
        S = K[mask]
        d = S.groupby(["w", "day"]).pnl.sum() / ncoins
        s = alldays.set_index(["w", "day"]).join(d.rename("p")).fillna(0).p
        v = (1 + s).cumprod().values
        dd = (v / np.maximum.accumulate(v) - 1).min()
        yrs = len(s) / 365
        yr = v[-1] ** (1 / yrs) - 1
        return pd.Series({"cases": len(S), "yearly": yr, "maxdd": dd, "calmar": yr / -dd,
                          "sharpe": s.mean() / s.std() * np.sqrt(365)})
    res = {"all": proxy(K.n1.notna(), "all"),
           "ret5<0": proxy(K.ret5 < 0, ""),
           "ret5<-0.076": proxy(K.ret5 < -0.076, ""),
           "r5z<0": proxy(K.r5z < 0, ""),
           "r5z<-1": proxy(K.r5z < -1, ""),
           "vr>1": proxy(K.vr > 1, ""),
           "ret5<0&vr>0.9": proxy((K.ret5 < 0) & (K.vr > 0.9), "")}
    out["proxy_books"] = pd.DataFrame(res).T
    # graded inside: r5z quintiles
    K["_q"] = pd.qcut(K.r5z, 5)
    out["by_r5z"] = K.groupby("_q").agg(n=("un1", "size"), un=("un1", "mean"),
                                        t=("un1", lambda x: x.mean() / x.std() * np.sqrt(len(x))), pnl=("pnl", "mean"))
    # condition alone check on r5z
    F = C[(C.ret60 < -0.10) & C.n1.notna()].copy()
    F["sig"] = F.index.isin(K.index)
    F["r5lo"] = F.r5z < -1
    out["r5z_alone_vs_both"] = F.groupby(["r5lo", "sig"]).agg(n=("un1", "size"), un1=("un1", "mean"),
                                                             t=("un1", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    # per window of ret5<0 subset
    S = K[K.ret5 < 0]
    out["ret5neg_by_window"] = S.groupby("w").agg(n=("un1", "size"), un=("un1", "mean"), pnl=("pnl", "sum"))
    out["ret5pos_by_window"] = K[K.ret5 >= 0].groupby("w").agg(n=("un1", "size"), un=("un1", "mean"), pnl=("pnl", "sum"))
    return out
