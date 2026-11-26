def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    days = data["days"]; bars = data["bars"]
    # book daily returns: per window, per day, mean over coins
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["alloc"] = b["postRebalance_current_allocation"]
            b["ret1"] = b["close"].pct_change()
            b["r20"] = b["close"]/b["close"].shift(20)-1
            b["r5"] = b["close"]/b["close"].shift(5)-1
            b["vol20"] = b["ret1"].rolling(20).std()
            b["fc"] = b["forecast"]
            dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd = dd.merge(b[["day","alloc","fc","r20","r5","vol20"]], on="day", how="left")
            dd["alloc_prev"] = dd["alloc"].shift(1)
            rows.append(dd)
    D = pd.concat(rows)
    book = D.groupby(["w","day"])["book_return"].mean().dropna().reset_index()
    hold = D.groupby(["w","day"])["coin_return"].mean().dropna().reset_index()
    out = {}
    # drawdowns on chained book
    book = book.sort_values(["w","day"]).reset_index(drop=True)
    v = (1+book["book_return"]).cumprod()
    peak = v.cummax(); dd = v/peak-1
    book["dd"] = dd
    # identify episodes
    ep = []
    in_dd = False
    for i in range(len(book)):
        if dd[i] < 0 and not in_dd:
            start = i; in_dd = True
        if in_dd and (dd[i] == 0 or i == len(book)-1):
            seg = book.iloc[start:i+1]
            ep.append((seg["dd"].min(), start, int(seg["dd"].idxmin()), i, seg["w"].iloc[0], seg["w"].iloc[-1]))
            in_dd = False
    ep = sorted(ep)[:6]
    out["worst_falls"] = pd.DataFrame([{"depth":e[0],"days_to_trough":e[2]-e[1]+1,"days_total":e[3]-e[1]+1,
                                        "w_start":e[4],"w_trough":book.loc[e[2],"w"]} for e in ep])
    # coin state on fall days vs others
    fallmask = np.zeros(len(book), bool)
    for e in ep[:4]:
        fallmask[e[1]:e[2]+1] = True
    book["fall"] = fallmask
    DD = D.merge(book[["w","day","fall"]], on=["w","day"], how="inner")
    DD["inpos"] = DD["alloc_prev"].abs() > 0.01
    g = DD[DD["inpos"]].groupby("fall").agg(n=("book_return","size"), book_ret=("book_return","mean"),
        coin_ret=("coin_return","mean"), alloc=("alloc_prev","mean"), r20=("r20","mean"), r5=("r5","mean"),
        vol20=("vol20","mean"))
    out["inpos_fall_vs_not"] = g
    out["by_window_book"] = book.groupby("w")["book_return"].agg(["mean","std","count"]).assign(
        hold=hold.groupby("w")["coin_return"].mean())
    # grid analysis: 3-day forward returns per coin in-position, by r20 bucket and fc bucket
    G = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            f3 = cl.shift(-3)/cl-1
            r20 = cl/cl.shift(20)-1
            r60 = cl/cl.shift(60)-1
            r1 = cl.pct_change()
            vol = r1.rolling(20).std()
            idx = np.arange(0, len(b), 3)
            g2 = pd.DataFrame({"f3":f3.iloc[idx].values, "fc":b["forecast"].iloc[idx].values,
                               "r20":r20.iloc[idx].values, "r60":r60.iloc[idx].values,
                               "r1":r1.iloc[idx].values, "vol":vol.iloc[idx].values,"coin":c,"w":w})
            G.append(g2)
    G = pd.concat(G).dropna(subset=["f3"])
    drift = G.groupby("coin")["f3"].mean()
    G["ex"] = G["f3"] - G["coin"].map(drift)
    G["inp"] = G["fc"] > 0
    G["fcq"] = pd.qcut(G["fc"].where(G["inp"]), 3, labels=["lo","mid","hi"])
    G["r20b"] = pd.cut(G["r20"], [-9,-0.10,0.10,9], labels=["fall","chop","rise"])
    G["r60b"] = pd.cut(G["r60"], [-9,-0.10,0.10,9], labels=["fall","chop","rise"])
    def agg(x):
        return pd.Series({"n":len(x),"f3":x["f3"].mean(),"ex":x["ex"].mean(),
                          "t":x["f3"].mean()/(x["f3"].std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out["grid_inp_by_r20"] = G[G["inp"]].groupby("r20b").apply(agg)
    out["grid_outp_by_r20"] = G[~G["inp"]].groupby("r20b").apply(agg)
    out["grid_inp_by_r60"] = G[G["inp"]].groupby("r60b").apply(agg)
    out["grid_inp_by_fcq_r20"] = G[G["inp"]].groupby(["fcq","r20b"]).apply(agg)
    G["volq"] = pd.qcut(G["vol"], 3, labels=["lo","mid","hi"])
    out["grid_inp_by_fcq_vol"] = G[G["inp"]].groupby(["fcq","volq"]).apply(agg)
    out["grid_outp_by_vol"] = G[~G["inp"]].groupby("volq").apply(agg)
    return out
