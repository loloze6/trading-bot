def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["days"].keys())
    # book daily returns: mean across coins per day within window
    rows = []
    for c in coins:
        for w, d in data["days"][c].items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"] = c; dd["window"] = w
            rows.append(dd)
    D = pd.concat(rows)
    wn = {w:int(w[1:]) for w in D["window"].unique()}
    D["wn"] = D["window"].map(wn)
    B = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().reset_index().sort_values(["wn","day"])
    B = B.dropna()
    v = (1+B["book_return"]).cumprod()
    dd = v/v.cummax()-1
    B["dd"] = dd.values
    B["year"] = pd.to_datetime(B["day"]).dt.year
    # deepest fall: trough and peak
    ti = dd.values.argmin()
    pi = v.values[:ti+1].argmax()
    seg = B.iloc[pi:ti+1]
    out["deepest_fall"] = pd.Series({"depth": dd.values[ti], "days": ti-pi,
        "book_sum": seg["book_return"].sum(), "coin_sum": seg["coin_return"].sum(),
        "start_window": seg["wn"].iloc[0], "end_window": seg["wn"].iloc[-1], "year_start": seg["year"].iloc[0], "year_end": seg["year"].iloc[-1]})
    out["by_window"] = B.groupby("wn").agg(book=("book_return","sum"), coin=("coin_return","sum"), mindd=("dd","min"), n=("book_return","size"))
    # per-bar case analysis
    recs = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float)
            r = cl.pct_change()
            vol = r.rolling(60).std()
            z = r/vol
            nxt = cl.shift(-1)/cl-1
            f = pd.DataFrame({"coin":c,"wn":wn[w],"r":r,"z":z,"nxt":nxt,"fc":b["forecast"],
                "alloc":b["postRebalance_current_allocation"],
                "ret20":cl/cl.shift(20)-1, "ret60":cl/cl.shift(60)-1,
                "vol20":r.rolling(20).std(),"vol60":vol,
                "below_ma50": cl < cl.rolling(50).mean()})
            f["volratio"] = f["vol20"]/f["vol60"]
            f["pos"] = np.arange(len(f))
            recs.append(f)
    F = pd.concat(recs).dropna(subset=["nxt","z"])
    drift = F.groupby("coin")["nxt"].mean()
    F["ex"] = F["nxt"] - F["coin"].map(drift)
    F["sig"] = F["fc"]>0
    F["gain"] = F["alloc"]*F["nxt"]
    def tt(x):
        x = x.dropna(); return pd.Series({"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,"n":len(x)})
    # condition splits: signal vs not
    for name, cond in [("ret20<0", F["ret20"]<0), ("ret60<0", F["ret60"]<0), ("below_ma50", F["below_ma50"]), ("volratio>1.2", F["volratio"]>1.2)]:
        g = []
        for s in [True, False]:
            for cv in [True, False]:
                m = (F["sig"]==s)&(cond==cv)
                x = tt(F.loc[m,"ex"]); x["sig"]=s; x["cond"]=cv; x["gain_mean"]=F.loc[m,"gain"].mean()
                g.append(x)
        out["split_"+name] = pd.DataFrame(g)
    # signal strength terciles within signal
    S = F[F["sig"]].copy()
    S["fq"] = pd.qcut(S["fc"].rank(method="first"),4,labels=False)
    out["by_fc_quart"] = S.groupby("fq").apply(lambda g: tt(g["ex"]))
    S["r60q"] = pd.qcut(S["ret60"],4,labels=False)
    out["sig_by_ret60_quart"] = S.groupby("r60q").apply(lambda g: pd.concat([tt(g["ex"]), pd.Series({"gain":g["gain"].mean(),"alloc":g["alloc"].mean()})]))
    S["vrq"] = pd.qcut(S["volratio"],4,labels=False)
    out["sig_by_volratio_quart"] = S.groupby("vrq").apply(lambda g: pd.concat([tt(g["ex"]), pd.Series({"gain":g["gain"].mean()})]))
    # holding gain in non-signal bars (position still held?)
    out["alloc_when_nosig"] = pd.Series({"share_held_nosig": (F.loc[~F["sig"],"alloc"].abs()>1e-6).mean(),
        "gain_nosig": F.loc[~F["sig"],"gain"].mean(), "gain_sig": F.loc[F["sig"],"gain"].mean(),
        "mean_alloc_sig": F.loc[F["sig"],"alloc"].mean()})
    return out
