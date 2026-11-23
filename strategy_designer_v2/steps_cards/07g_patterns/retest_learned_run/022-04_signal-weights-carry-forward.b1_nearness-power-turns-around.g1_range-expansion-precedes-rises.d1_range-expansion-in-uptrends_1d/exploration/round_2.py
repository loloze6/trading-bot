def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c, h, l = b["close"], b["high"], b["low"]
            rr = (h - l) / (h - l).rolling(30, min_periods=20).mean()
            clpos = (c - l) / (h - l).replace(0, np.nan)
            r1 = c / c.shift(1) - 1
            f = pd.DataFrame({"coin": coin, "win": w, "rr": rr, "clpos": clpos, "r1": r1,
                              "ret20": c / c.shift(20) - 1, "fwd": c.shift(-H) / c - 1,
                              "fwd1": c.shift(-1) / c - 1,
                              "yr": pd.to_datetime(b["timestamp"]).dt.year})
            f["sig_cl"] = rr * (2 * clpos - 1)
            f["sig_r1"] = rr * np.sign(r1)
            f["pos"] = np.arange(len(f))
            rows.append(f)
    d = pd.concat(rows, ignore_index=True)
    out = {}
    for off in [0, 2]:
        g = d[((d["pos"] - off) % H == 0) & (d["pos"] >= off)].dropna(subset=["fwd"]).copy()
        drift = d[(d.pos % H == 0)].dropna(subset=["fwd"]).groupby("coin")["fwd"].mean()
        sd = d[(d.pos % H == 0)].dropna(subset=["fwd"]).groupby("coin")["fwd"].std()
        g["ex"] = g["fwd"] - g["coin"].map(drift)
        g["exz"] = g["ex"] / g["coin"].map(sd)
        res = []
        for x in ["sig_cl", "sig_r1", "rr", "clpos"]:
            for name, sub in [("all", g), ("up20", g[g.ret20 > 0]), ("dn20", g[g.ret20 <= 0])]:
                s = sub.dropna(subset=[x, "exz"])
                z = s.groupby("coin")[x].transform(lambda v: (v - v.mean()) / v.std())
                r = stats.linregress(z, s["exz"])
                res.append({"feat": x, "set": name, "slope": r.slope, "t": r.slope / r.stderr, "n": len(s)})
        out[f"slopes_grid_offset{off}"] = pd.DataFrame(res)
        if off == 0:
            s = g.dropna(subset=["sig_cl"]).copy()
            s["q"] = s.groupby("coin")["sig_cl"].transform(lambda v: pd.qcut(v.rank(method="first"), 5, labels=False))
            out["sig_cl_quintile_ex5_pct"] = s.groupby("q")["ex"].agg(lambda v: f"{v.mean()*100:.2f}% t={v.mean()/v.std()*np.sqrt(len(v)):.2f} n={len(v)}")
            pc = []
            for coin, sc in s.groupby("coin"):
                z = (sc.sig_cl - sc.sig_cl.mean()) / sc.sig_cl.std()
                r = stats.linregress(z, sc["exz"])
                pc.append({"coin": coin, "slope": r.slope, "t": r.slope / r.stderr, "n": len(sc)})
            out["sig_cl_by_coin"] = pd.DataFrame(pc)
            py = []
            for yr, sc in s.groupby("yr"):
                z = sc.groupby("coin")["sig_cl"].transform(lambda v: (v - v.mean()) / v.std())
                r = stats.linregress(z, sc["exz"])
                py.append({"yr": yr, "slope": r.slope, "t": r.slope / r.stderr, "n": len(sc)})
            out["sig_cl_by_year"] = pd.DataFrame(py)
            # total move of top quintile per case
            top = s[s.q == 4]
            out["top_quint_total_unusual_pct"] = pd.Series({"total": top.fwd.mean()*100, "unusual": top.ex.mean()*100,
                                                            "n": len(top)})
    # 1-day: close location next day
    e = d.dropna(subset=["fwd1", "sig_cl"])
    z = e.groupby("coin")["sig_cl"].transform(lambda v: (v - v.mean()) / v.std())
    r = stats.linregress(z, e["fwd1"])
    out["sig_cl_next1d_alldays"] = pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": len(e)})
    return out
