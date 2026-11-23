def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    recs = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = pd.DataFrame({"ts": pd.to_datetime(df["timestamp"]), "c": df["close"].astype(float).values})
            d = d.reset_index(drop=True)
            ct = d["ts"] + pd.Timedelta(hours=1)
            d["cwd"] = ct.dt.weekday; d["chr"] = ct.dt.hour
            c = d["c"]
            d["r1f"] = c.shift(-1)/c - 1
            for k in (24, 48):
                d[f"p{k}"] = c/c.shift(k) - 1
                d[f"f{k}"] = c.shift(-k)/c - 1
                d[f"s{k}"] = d[f"p{k}"].abs().rolling(720, min_periods=360).mean()
            d["pos"] = np.arange(len(d)); d["coin"] = coin; d["win"] = w
            d["year"] = d["ts"].dt.year
            recs.append(d)
    A = pd.concat(recs, ignore_index=True)
    out = {}
    # drift per coin for 48h and 24h on grid
    dr = {}
    for k in (24, 48):
        g = A[A["pos"] % k == 0]
        dr[k] = g.groupby("coin")[f"f{k}"].mean()
    for k in (24, 48):
        A[f"x{k}"] = A[f"f{k}"] - A["coin"].map(dr[k])
    # anchor-day analysis: past 48h scaled vs next 48h, anchor at close hour 0 of each weekday
    rows = []
    E = A[(A["chr"] == 0)].dropna(subset=["p48", "s48", "x48"])
    for wd, g in E.groupby("cwd"):
        z = g["p48"]/g["s48"]; y = g["x48"]/g["s48"]
        rev = -np.sign(z)*g["x48"]
        sl = stats.linregress(z, y)
        big = z.abs() > z.abs().quantile(0.75)
        rows.append({"close_wd": wd, "n": len(g), "slope": sl.slope, "t_slope": sl.slope/sl.stderr,
                     "rev_mean%": rev.mean()*100, "rev_t": rev.mean()/rev.std()*np.sqrt(len(rev)),
                     "rev_top25%": rev[big].mean()*100, "t_top25": rev[big].mean()/rev[big].std()*np.sqrt(big.sum())})
    out["past48_vs_next48_by_anchor_weekday(0=Mon close)"] = pd.DataFrame(rows)
    # 24h past vs next 24h by anchor weekday
    rows = []
    E = A[(A["chr"] == 0)].dropna(subset=["p24", "s24", "x24"])
    for wd, g in E.groupby("cwd"):
        z = g["p24"]/g["s24"]; y = g["x24"]/g["s24"]
        sl = stats.linregress(z, y)
        rows.append({"close_wd": wd, "n": len(g), "slope": sl.slope, "t_slope": sl.slope/sl.stderr,
                     "mean_next24%": g["f24"].mean()*100, "t_mean": g["x24"].mean()/g["x24"].std()*np.sqrt(len(g))})
    out["past24_vs_next24_by_anchor_weekday"] = pd.DataFrame(rows)
    # hour of day 1h returns
    h = A.dropna(subset=["r1f"]).groupby("chr")["r1f"].agg(["mean", "std", "count"])
    h["t"] = h["mean"]/h["std"]*np.sqrt(h["count"]); h["mean_bp"] = h["mean"]*1e4
    out["next1h_by_close_hour"] = h[["mean_bp", "t", "count"]]
    # large 24h move buckets, 24h grid, all hours
    G = A[A["pos"] % 24 == 0].dropna(subset=["p24", "s24", "x24"]).copy()
    G["z"] = G["p24"]/G["s24"]
    G["zb"] = pd.qcut(G["z"], 10, labels=False)
    b = G.groupby("zb").agg(z=("z", "mean"), next24_ex_pct=("x24", lambda s: s.mean()*100),
                            t=("x24", lambda s: s.mean()/s.std()*np.sqrt(len(s))), n=("x24", "size"))
    out["next24_by_past24_decile"] = b
    # vol level: s24 relative to coin's pooled median
    G["vr"] = G["s24"]/G.groupby("coin")["s24"].transform("median")
    G["vb"] = pd.qcut(G["vr"], 5, labels=False)
    rows = []
    for vb, g in G.groupby("vb"):
        sl = stats.linregress(g["z"], g["x24"]/g["s24"])
        rows.append({"volq": vb, "n": len(g), "mean_ex%": g["x24"].mean()*100,
                     "t_mean": g["x24"].mean()/g["x24"].std()*np.sqrt(len(g)), "slope": sl.slope, "t_slope": sl.slope/sl.stderr})
    out["by_vol_quintile_24h"] = pd.DataFrame(rows)
    # book daily by weekday
    bd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df.copy(); x["wd"] = pd.to_datetime(x["day"]).dt.weekday; bd.append(x)
    B = pd.concat(bd).dropna(subset=["book_return"])
    bw = B.groupby("wd").agg(book_bp=("book_return", lambda s: s.mean()*1e4), coin_bp=("coin_return", lambda s: s.mean()*1e4), n=("book_return", "size"))
    out["book_and_coin_daily_by_weekday"] = bw
    return out
