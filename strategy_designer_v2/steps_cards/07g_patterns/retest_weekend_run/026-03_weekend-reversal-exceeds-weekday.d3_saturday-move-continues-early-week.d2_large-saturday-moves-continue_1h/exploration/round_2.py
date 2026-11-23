def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    recs = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = pd.DataFrame({"ts": pd.to_datetime(df["timestamp"]), "c": df["close"].astype(float).values}).reset_index(drop=True)
            ct = d["ts"] + pd.Timedelta(hours=1)
            d["cwd"] = ct.dt.weekday; d["chr"] = ct.dt.hour
            c = d["c"]
            d["r1f"] = c.shift(-1)/c - 1
            d["r2f"] = c.shift(-2)/c - 1
            d["p24"] = c/c.shift(24) - 1
            d["f24"] = c.shift(-24)/c - 1
            d["s24"] = d["p24"].abs().rolling(720, min_periods=360).mean()
            d["p1"] = c/c.shift(1) - 1
            d["s1"] = d["p1"].abs().rolling(720, min_periods=360).mean()
            d["pos"] = np.arange(len(d)); d["coin"] = coin; d["win"] = w
            d["year"] = d["ts"].dt.year
            recs.append(d)
    A = pd.concat(recs, ignore_index=True)
    out = {}
    g24 = A[A["pos"] % 24 == 0]
    dr24 = g24.groupby("coin")["f24"].mean()
    A["x24"] = A["f24"] - A["coin"].map(dr24)
    G = g24.dropna(subset=["p24", "s24", "f24"]).copy()
    G["x24"] = G["f24"] - G["coin"].map(dr24)
    G["z"] = G["p24"]/G["s24"]
    G["vr"] = G["s24"]/G.groupby("coin")["s24"].transform("median")
    G["vh"] = G["vr"] > G["vr"].quantile(0.6)
    # reversal by year: graded slope and per-case directional excess for |z| top quartile
    rows = []
    for (yr), g in G.groupby("year"):
        sl = stats.linregress(g["z"], g["x24"]/g["s24"])
        big = g[g["z"].abs() > G["z"].abs().quantile(0.75)]
        rv = -np.sign(big["z"])*big["x24"]
        rows.append({"year": yr, "n": len(g), "slope": sl.slope, "t": sl.slope/sl.stderr,
                     "rev_big%": rv.mean()*100, "t_big": rv.mean()/rv.std()*np.sqrt(len(rv)), "n_big": len(rv)})
    out["rev24_by_year"] = pd.DataFrame(rows)
    rows = []
    for coin, g in G.groupby("coin"):
        sl = stats.linregress(g["z"], g["x24"]/g["s24"])
        rows.append({"coin": coin, "slope": sl.slope, "t": sl.slope/sl.stderr, "n": len(g)})
    out["rev24_by_coin"] = pd.DataFrame(rows)
    # high vol half: deciles of z, directional move
    H = G[G["vh"]].copy()
    H["zb"] = pd.qcut(H["z"], 5, labels=False)
    out["highvol_next24_by_z_quintile"] = H.groupby("zb").agg(z=("z", "mean"), ex_pct=("x24", lambda s: s.mean()*100),
        t=("x24", lambda s: s.mean()/s.std()*np.sqrt(len(s))), n=("x24", "size"))
    # down vs up asymmetry
    for nm, m in [("down", G["z"] < 0), ("up", G["z"] > 0)]:
        g = G[m]; sl = stats.linregress(g["z"], g["x24"]/g["s24"])
        out[f"slope_{nm}"] = f"slope {sl.slope:.4f} t {sl.slope/sl.stderr:.2f} n {len(g)}"
    # Saturday-anchor reversal vs other days difference
    E = A[A["chr"] == 0].dropna(subset=["p24", "s24", "x24"]).copy()
    E["z"] = E["p24"]/E["s24"]; E["rv"] = -np.sign(E["z"])*E["x24"]/E["s24"]*np.abs(E["z"])
    sat = E[E["cwd"] == 6]["rv"]; oth = E[E["cwd"] != 6]["rv"]
    tt = stats.ttest_ind(sat, oth, equal_var=False)
    out["sat_minus_other_graded_rev"] = f"diff {sat.mean()-oth.mean():.4f} t {tt.statistic:.2f} n {len(sat)}/{len(oth)}"
    # evening hours 21-22 close: 2h return by year and graded by past 24h z
    V = A[(A["chr"] == 21)].dropna(subset=["r2f", "p24", "s24"]).copy()
    V["z"] = V["p24"]/V["s24"]
    out["r2f_at_21close_by_year"] = V.groupby("year")["r2f"].agg(mean_bp=lambda s: s.mean()*1e4,
        t=lambda s: s.mean()/s.std()*np.sqrt(len(s)), n="size")
    V["zb"] = pd.qcut(V["z"], 5, labels=False)
    out["r2f_at_21close_by_z"] = V.groupby("zb")["r2f"].agg(mean_bp=lambda s: s.mean()*1e4,
        t=lambda s: s.mean()/s.std()*np.sqrt(len(s)), n="size")
    out["r2f_at_21close_by_weekday"] = V.groupby("cwd")["r2f"].agg(mean_bp=lambda s: s.mean()*1e4,
        t=lambda s: s.mean()/s.std()*np.sqrt(len(s)), n="size")
    # cumulative return from hour 20 close to hour 24 vs vol level
    V["vr"] = V["s1"]/V.groupby("coin")["s1"].transform("median")
    V["vb"] = pd.qcut(V["vr"], 3, labels=False)
    out["r2f_at_21close_by_vol_tercile"] = V.groupby("vb")["r2f"].agg(mean_bp=lambda s: s.mean()*1e4,
        t=lambda s: s.mean()/s.std()*np.sqrt(len(s)), n="size")
    return out
