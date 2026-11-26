def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]; days = data["days"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            cl = b["close"].astype(float)
            r = cl.pct_change()
            fwd = cl.shift(-1)/cl - 1
            fwd2 = cl.shift(-2)/cl - 1
            pos = b["postRebalance_current_allocation"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": c, "w": w, "pos": pos, "fwd": fwd, "fwd2": fwd2, "r": r,
                               "fc": b["forecast"].astype(float), "agit": (b["regime"] == "unknown").values,
                               "t60": cl/cl.shift(60)-1, "day": ts.dt.floor("D"), "i": np.arange(len(b))})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["ex"] = A["fwd"] - A["coin"].map(A.groupby("coin")["fwd"].mean())
    A["ex2"] = A["fwd2"] - A["coin"].map(A.groupby("coin")["fwd2"].mean())
    A["gain"] = A["pos"]*A["fwd"]
    A["tr"] = pd.cut(A["t60"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    out = {}
    def summ(g, col="ex"):
        n = g[col].notna().sum()
        return pd.Series({"n": n, "mean": g[col].mean(),
                          "t": g[col].mean()/(g[col].std()/np.sqrt(n)) if n > 2 else np.nan,
                          "mean_gain": g["gain"].mean(), "sum_gain": g["gain"].sum()})
    Ag = A[A["agit"]].dropna(subset=["fwd"]).copy()
    Ag["sig"] = Ag["fc"] > 0
    out["agit_trend60_sig_vs_nosig"] = Ag.groupby(["tr", "sig"]).apply(summ)
    # condition alone also on calm bars
    Cm = A[~A["agit"]].dropna(subset=["fwd"]).copy()
    Cm["down"] = Cm["r"] < 0
    out["calm_trend60_down_vs_up"] = Cm.groupby(["tr", "down"]).apply(summ)
    S = Ag[Ag["sig"]].copy()
    S["fcq"] = pd.qcut(S["fc"], 3, labels=False, duplicates="drop")
    out["trend60_x_fcq"] = S.groupby(["tr", "fcq"]).apply(summ)
    # slope of ex on fc within each trend
    sl = {}
    for k, g in S.groupby("tr"):
        g = g.dropna(subset=["ex", "fc"])
        if len(g) > 10:
            x = g["fc"]-g["fc"].mean(); b1 = (x*g["ex"]).sum()/(x**2).sum()
            res = g["ex"]-g["ex"].mean()-b1*x
            se = np.sqrt((res**2).sum()/(len(g)-2)/(x**2).sum())
            sl[k] = pd.Series({"n": len(g), "slope": b1, "t": b1/se})
    out["slope_by_trend60"] = pd.DataFrame(sl).T
    # 2-day horizon, non-overlapping-ish (even i) for signal bars
    S2 = S[S["i"] % 2 == 0]
    out["trend60_2d_ex"] = S2.groupby("tr").apply(lambda g: summ(g, "ex2"))
    # book gain on held bars by trend60 (all held bars, including holding overflow)
    H = A[A["pos"].abs() > 1e-9].dropna(subset=["fwd"])
    out["held_gain_by_trend60"] = H.groupby("tr").apply(summ)
    # deepest fall in w16: profile of held bars
    D = []
    for c in days:
        for w, d in days[c].items():
            d = d[["day", "book_return"]].copy(); d["w"] = w; d["coin"] = c; D.append(d)
    D = pd.concat(D)
    bd = D.groupby(["w", "day"])["book_return"].mean().reset_index()
    bd["wn"] = bd["w"].str[1:].astype(int); bd = bd.sort_values(["wn", "day"]).dropna().reset_index(drop=True)
    v = (1+bd["book_return"]).cumprod().values; dd = v/np.maximum.accumulate(v)-1
    i = int(np.argmin(dd)); pk = int(np.argmax(v[:i+1]))
    seg = bd.iloc[pk:i+1]
    key = set(zip(seg["w"], pd.to_datetime(seg["day"]).dt.floor("D")))
    Hd = H[[ (a, b) in key for a, b in zip(H["w"], H["day"]) ]]
    out["dd_held_by_trend60"] = Hd.groupby("tr").apply(summ)
    # simulated drawdown/calmar proxy of filtered books: gain only in fall trend vs all
    for name, mask in {"all": A["pos"].abs() > -1, "fall_only": A["tr"] == "fall", "nonrise": A["tr"] != "rise"}.items():
        g = A[mask].copy()
        dg = A.assign(g2=np.where(mask, A["gain"], 0.0)).groupby(["w", "day"])["g2"].mean().reset_index()
        dg["wn"] = dg["w"].str[1:].astype(int); dg = dg.sort_values(["wn", "day"])
        vv = (1+dg["g2"].fillna(0)).cumprod().values
        ddd = (vv/np.maximum.accumulate(vv)-1).min()
        yrs = len(dg)/365
        yr = vv[-1]**(1/yrs)-1
        out["calmar_proxy_"+name] = pd.Series({"yearly": yr, "maxdd": ddd, "calmar": yr/abs(ddd),
                                               "sharpe": dg["g2"].mean()/dg["g2"].std()*np.sqrt(365)})
    return out
