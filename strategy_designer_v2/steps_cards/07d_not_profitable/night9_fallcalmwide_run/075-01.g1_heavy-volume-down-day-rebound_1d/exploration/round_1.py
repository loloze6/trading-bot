def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # book daily returns: mean over coins per day, window order
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"]).agg(br=("book_return","mean"), cr=("coin_return","mean")).dropna().reset_index().sort_values(["wn","day"])
    val = (1+B["br"]).cumprod(); peak = val.cummax(); ddn = val/peak-1
    B["dd"] = ddn.values
    out["book by window"] = B.groupby("wn").agg(mean_br=("br","mean"), sum_br=("br","sum"), sum_cr=("cr","sum"), min_dd=("dd","min"), n=("br","size"))
    # deepest fall location
    i_min = ddn.values.argmin(); i_peak = np.argmax(val.values[:i_min+1])
    seg = B.iloc[i_peak:i_min+1]
    out["deepest fall"] = pd.Series({"depth": ddn.values[i_min], "days": i_min-i_peak, "from_w": B["wn"].iloc[i_peak], "to_w": B["wn"].iloc[i_min], "book_sum": seg["br"].sum(), "coins_sum": seg["cr"].sum()})
    # per coin features, joined by timestamp for features only
    recs = []
    for c in bars:
        ws = sorted(bars[c].keys(), key=lambda x:int(x[1:]))
        full = pd.concat([bars[c][w].assign(w=w) for w in ws]).sort_values("timestamp").reset_index(drop=True)
        full["timestamp"] = pd.to_datetime(full["timestamp"])
        cl = full["close"]
        full["r1"] = cl.pct_change()
        full["tr60"] = cl/cl.shift(60)-1
        sd30 = full["r1"].rolling(30).std()
        full["agit"] = sd30 > sd30.rolling(365, min_periods=200).median()
        full["agit"] = full["agit"].where(sd30.rolling(365, min_periods=200).median().notna())
        full["r5"] = cl/cl.shift(5)-1
        vr = full["volume"]/full["volume"].shift(1).rolling(20).mean()
        full["vr"] = vr
        # next-day return inside window
        full["nx"] = full.groupby("w")["close"].shift(-1)/cl-1
        full["same_prev_w"] = full["w"].eq(full["w"].shift(1))
        full["down"] = (full["r1"]<0) & full["same_prev_w"]
        full["alloc"] = full["postRebalance_current_allocation"]
        full["pg"] = full["alloc"]*full["nx"]
        full["coin"] = c
        recs.append(full)
    F = pd.concat(recs)
    F["drift"] = F.groupby("coin")["nx"].transform("mean")
    F["ex"] = F["nx"]-F["drift"]
    F["trend"] = np.where(F["tr60"]>0.1,"rising",np.where(F["tr60"]<-0.1,"falling",np.where(F["tr60"].notna(),"choppy",None)))
    F["prof"] = F["trend"].astype(str)+"_"+F["agit"].map({True:"agit",False:"calm"}).astype(str)
    g = F[F["nx"].notna()]
    def summ(x):
        return pd.Series({"n":len(x),"mean_nx":x["nx"].mean(),"mean_ex":x["ex"].mean(),"t_ex":x["ex"].mean()/(x["ex"].std()/np.sqrt(len(x))) if len(x)>2 else np.nan,"mean_pg":x["pg"].mean(),"mean_alloc":x["alloc"].abs().mean()})
    out["all days by trend"] = g.groupby("trend").apply(summ)
    out["down days by trend"] = g[g["down"]].groupby("trend").apply(summ)
    out["down days by profile"] = g[g["down"]].groupby("prof").apply(summ)
    out["all days by profile"] = g.groupby("prof").apply(summ)
    dn = g[g["down"]].copy()
    dn["vq"] = pd.qcut(dn["vr"], 3, labels=["lo","mid","hi"])
    out["down by trend x vol tercile"] = dn.groupby(["trend","vq"]).apply(summ)
    dn["fallq"] = pd.qcut(dn["r1"], 3, labels=["big","mid","small"])
    out["down by fall size x vol"] = dn.groupby(["fallq","vq"]).apply(summ)
    dn["r5q"] = pd.qcut(dn["r5"], 3, labels=["r5low","r5mid","r5high"])
    out["down by prior 5d x vol"] = dn.groupby(["r5q","vq"]).apply(summ)
    # position gain during deepest fall by trend
    out["book pg by trend all bars"] = g.groupby("trend")["pg"].agg(["sum","mean","count"])
    return out
