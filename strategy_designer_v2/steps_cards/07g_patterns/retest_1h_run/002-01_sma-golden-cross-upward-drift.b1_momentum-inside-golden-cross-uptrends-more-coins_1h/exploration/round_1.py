def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    # 1) 240-bar grid: forward 240 ret vs 480 past return, by regime
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            cl = df["close"].values
            n = len(cl)
            ts = pd.to_datetime(df["timestamp"])
            reg = df["regime"].values
            for i in range(0, n - 240, 240):
                if i < 480: past = np.nan
                else: past = cl[i] / cl[i-480] - 1
                p5 = cl[i]/cl[i-120]-1 if i >= 120 else np.nan
                rows.append((c, w, reg[i], past, p5, cl[i+240]/cl[i]-1))
    g = pd.DataFrame(rows, columns=["coin","w","reg","past20","past5","fwd"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g2 = g.dropna(subset=["past20"]).copy()
    g2["q"] = g2.groupby("reg")["past20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["fwd10d_by_regime_past20q"] = g2.groupby(["reg","q"])["ex"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))]).round(4)
    nt = g2[g2.reg != "trending"]
    if len(nt) > 10:
        r = stats.linregress(nt["past20"], nt["ex"])
        out["nontrend_slope_ex_on_past20"] = f"slope {r.slope:.4f} t {r.slope/r.stderr:.2f} n {len(nt)}"
    g3 = g.dropna(subset=["past5"])
    for reg in g3.reg.unique():
        s = g3[g3.reg == reg]
        r = stats.linregress(s["past5"], s["ex"])
        out[f"slope_ex_on_past5d_{reg}"] = f"slope {r.slope:.4f} t {r.slope/r.stderr:.2f} n {len(s)}"
    # 2) 24-bar grid: next-day return after past-day return, by vol tercile
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            cl = df["close"].values; n = len(cl)
            lr = np.diff(np.log(cl))
            for i in range(168, n - 24, 24):
                vol = lr[i-168:i].std()
                rows.append((c, cl[i]/cl[i-24]-1, vol, cl[i+24]/cl[i]-1))
    d = pd.DataFrame(rows, columns=["coin","p1","vol","f1"])
    d["z"] = d["p1"] / (d["vol"]*np.sqrt(24))
    d["zq"] = pd.qcut(d["z"], 5, labels=False)
    d["vq"] = d.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False))
    d["fz"] = d["f1"]/(d["vol"]*np.sqrt(24))
    out["next1d_z_by_past1d_zq"] = d.groupby("zq")["fz"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))]).round(4)
    out["next1d_ret_by_volq"] = d.groupby("vq")["f1"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))]).round(5)
    # 3) hour and weekday of 1h returns
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            ts = pd.to_datetime(df["timestamp"])
            r = df["close"].pct_change()
            # normalized per coin-window
            rows.append(pd.DataFrame({"h": ts.dt.hour, "wd": ts.dt.weekday, "r": r/r.std()}))
    h = pd.concat(rows).dropna()
    ht = h.groupby("h")["r"].agg(["mean","count"])
    ht["t"] = ht["mean"]*np.sqrt(ht["count"])
    out["hour_norm_ret_t"] = ht["t"].round(2)
    # 4) book daily by weekday and book share
    rows = []
    for c, ws in days.items():
        for w, df in ws.items():
            dd = df.copy(); dd["coin"] = c
            dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
            rows.append(dd)
    D = pd.concat(rows).dropna(subset=["book_return","coin_return"])
    wd = D.groupby("wd")[["book_return","coin_return"]].mean()
    wd["book_t"] = D.groupby("wd")["book_return"].apply(lambda s: s.mean()/s.std()*np.sqrt(len(s)))
    out["book_by_weekday"] = wd.round(5)
    return out
