def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # book daily returns, mean over coins per day within window
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d.copy(); dd["coin"] = c; dd["win"] = w
            rows.append(dd[["day","win","coin","book_return","coin_return"]])
    D = pd.concat(rows)
    D["wn"] = D["win"].str[1:].astype(int)
    B = D.groupby(["wn","day"]).agg(book=("book_return","mean"), hold=("coin_return","mean")).dropna().reset_index().sort_values(["wn","day"])
    v = (1+B["book"]).cumprod(); dd_ = v/v.cummax()-1
    B["dd"] = dd_.values
    out["by_window"] = B.groupby("wn").agg(n=("book","size"), book_mean=("book","mean"), book_sum=("book","sum"), hold_mean=("hold","mean"), min_dd=("dd","min"))
    out["max_dd"] = float(dd_.min())
    # worst days
    out["worst_days_by_window"] = B.nsmallest(15,"book")[["wn","book","hold"]].reset_index(drop=True)
    # cases: build per coin bar-level features
    cs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"]; r = cl.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            f = pd.DataFrame({"r":r, "z":r/sd30, "fc":b["forecast"], "alloc":b["postRebalance_current_allocation"], "reg":b["regime"]})
            f["depth"] = 1 - cl/cl.rolling(20, min_periods=10).max()
            f["r3"] = cl/cl.shift(3)-1
            f["r5z"] = (cl/cl.shift(5)-1)/(sd30*np.sqrt(5))
            f["r60"] = cl/cl.shift(60)-1
            f["n1"] = cl.shift(-1)/cl-1
            f["n2"] = cl.shift(-2)/cl-1
            f["n3"] = cl.shift(-3)/cl-1
            f["n5"] = cl.shift(-5)/cl-1
            f["coin"]=c; f["wn"]=int(w[1:])
            f["pnl"] = f["alloc"]*f["n1"]
            cs.append(f)
    F = pd.concat(cs, ignore_index=True)
    mu = F.groupby("coin")["n1"].mean()
    F["u1"] = -(F["n1"] - F["coin"].map(mu))
    inp = F["reg"]=="unknown"
    sig = inp & (F["r"]>0)
    S = F[sig].dropna(subset=["n1","z"])
    def summ(g):
        x = g["u1"]
        return pd.Series({"n":len(x), "u1":x.mean(), "t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,
                          "fall2":(-g["n2"]).mean(), "fall3":(-g["n3"]).mean(), "fall5":(-g["n5"]).mean(), "pnl_mean":g["pnl"].mean()})
    out["sig_by_z"] = S.groupby(pd.qcut(S["z"],5)).apply(summ)
    out["sig_by_depth"] = S.groupby(pd.qcut(S["depth"],5)).apply(summ)
    out["sig_by_r60"] = S.groupby(pd.qcut(S["r60"],4)).apply(summ)
    out["sig_by_r5z"] = S.groupby(pd.qcut(S["r5z"],5)).apply(summ)
    out["sig_by_window"] = S.groupby("wn").apply(summ)
    # in-profile non-signal (down days) for comparison
    N = F[inp & (F["r"]<=0)].dropna(subset=["n1"])
    out["inprofile_downdays"] = summ(N)
    out["all_sig"] = summ(S)
    # position pnl by holding: are positions held beyond signal day?
    pos = F[F["alloc"].abs()>1e-6]
    out["pos_on_updays_share"] = float((pos["r"]>0).mean())
    out["pos_pnl_by_dayret_sign"] = pos.groupby(pos["r"]>0)["pnl"].agg(["size","mean","sum"])
    out["pos_pnl_by_window"] = pos.groupby("wn")["pnl"].agg(["size","mean","sum"])
    return out
