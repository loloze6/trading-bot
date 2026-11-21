def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # book daily returns: per window/day mean over coins
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["window"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["window"].str[1:].astype(int)
    B = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"), n=("coin", "count")).reset_index().sort_values(["wn", "day"])
    B = B.dropna(subset=["br"])
    B["eq"] = (1 + B["br"]).cumprod()
    B["peak"] = B["eq"].cummax()
    B["dd"] = B["eq"] / B["peak"] - 1
    B["i"] = np.arange(len(B))
    # identify drawdown episodes
    ep = []
    in_dd = False
    for _, r in B.iterrows():
        if r["dd"] < 0 and not in_dd:
            in_dd = True; start = r["i"]
        if r["dd"] == 0 and in_dd:
            in_dd = False; ep.append((start, r["i"]))
    if in_dd: ep.append((start, B["i"].iloc[-1]))
    E = []
    for s, e in ep:
        seg = B.iloc[int(s):int(e) + 1]
        trough = seg["dd"].idxmin()
        E.append({"start_i": s, "len_days": e - s, "depth": seg["dd"].min(),
                  "windows": ",".join(sorted(set("w%d" % x for x in seg["wn"]))),
                  "coin_mean_ret_sum": seg["cr"].sum(), "book_ret_sum": seg["br"].sum()})
    E = pd.DataFrame(E).sort_values("depth").head(8).drop(columns="start_i")
    out["deepest_falls"] = E
    out["book_by_window"] = B.groupby("wn").agg(days=("br", "size"), mean=("br", "mean"), sum=("br", "sum"), mindd=("dd", "min"), coinsum=("cr", "sum")).reset_index()
    yrs = len(B) / 365
    tot = B["eq"].iloc[-1]
    out["calmar_parts"] = pd.Series({"yearly": tot ** (1 / yrs) - 1, "maxdd": B["dd"].min(), "days": len(B)})
    # trade-level: entry features
    T = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r60 = cl / cl.shift(60) - 1
            r10 = cl / cl.shift(10) - 1
            r1 = cl.pct_change()
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60).std()
            ma20 = cl / cl.rolling(20).mean() - 1
            alloc = b["postRebalance_current_allocation"].fillna(0)
            prev = alloc.shift(1).fillna(0)
            ent = b.index[(alloc > 0) & (prev <= 0)]
            for i in ent:
                # hold until alloc goes to 0
                j = i
                while j + 1 < len(b) and alloc.iloc[j + 1] > 0: j += 1
                ret = cl.iloc[min(j + 1, len(b) - 1)] / cl.iloc[i] - 1
                r5 = cl.iloc[i + 5] / cl.iloc[i] - 1 if i + 5 < len(b) else np.nan
                T.append({"coin": c, "w": w, "r60": r60.iloc[i], "r10": r10.iloc[i], "r1": r1.iloc[i], "volr": vol20.iloc[i] / vol60.iloc[i] if vol60.iloc[i] else np.nan,
                          "vol20": vol20.iloc[i], "ma20": ma20.iloc[i], "alloc": alloc.iloc[i], "hold": j - i + 1, "ret": ret, "r5": r5,
                          "brk": b.get("debug_info.components.break.last_history_value", pd.Series(np.nan, index=b.index)).iloc[i]})
    T = pd.DataFrame(T)
    T["wret"] = T["ret"] * T["alloc"]
    out["trades_n"] = pd.Series({"n": len(T), "mean_ret": T["ret"].mean(), "mean_wret": T["wret"].mean(), "hold_med": T["hold"].median(), "share_neg": (T["ret"] < 0).mean(), "p5": T["ret"].quantile(0.05)})
    for f in ["r60", "r10", "r1", "volr", "vol20", "ma20", "brk"]:
        x = T.dropna(subset=[f, "ret"])
        x["q"] = pd.qcut(x[f].rank(method="first"), 5, labels=False)
        g = x.groupby("q").agg(n=("ret", "size"), fmean=(f, "mean"), ret=("ret", "mean"), r5=("r5", "mean"), wret=("wret", "mean"), p10=("ret", lambda s: s.quantile(0.1)))
        out["by_" + f] = g
    return out
