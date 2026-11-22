def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            r1 = c.pct_change()
            hh = hi.rolling(30).max(); ll = lo.rolling(30).min()
            er = (c - c.shift(30)) / (hh - ll)
            vol20 = r1.rolling(20).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(b)),
                               "fwd": c.shift(-H) / c - 1, "fwd10": c.shift(-10) / c - 1,
                               "er": er, "ret30": c / c.shift(30) - 1, "r1": r1, "next1": r1.shift(-1),
                               "vol_rel": vol20 / vol20.rolling(60, min_periods=20).mean(),
                               "wd": ts.dt.weekday, "yr": ts.dt.year})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    # weekday on daily, non-overlapping 1-day returns
    D = A.dropna(subset=["next1"]).copy()
    D["u1"] = D["next1"] - D["coin"].map(D.groupby("coin")["next1"].mean())
    D["wd_next"] = (D["wd"] + 1) % 7
    wd = D.groupby("wd_next").agg(n=("u1", "size"), u=("u1", "mean"), sd_=("u1", "std"))
    wd["t"] = wd["u"] / (wd["sd_"] / np.sqrt(wd["n"]))
    out["daily_unusual_by_weekday_of_return"] = wd.drop(columns="sd_").round(5)
    G = A[A["i"] % H == 0].dropna(subset=["fwd"]).copy()
    drift = G.groupby("coin")["fwd"].mean(); sd = G.groupby("coin")["fwd"].std()
    G["u"] = G["fwd"] - G["coin"].map(drift); G["s"] = G["u"] / G["coin"].map(sd)
    G["tot"] = G["fwd"]
    def tab(df, col, q):
        x = df.dropna(subset=[col]).copy()
        x["b"] = pd.qcut(x[col], q, labels=False, duplicates="drop")
        r = x.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), n=("u", "size"), u=("u", "mean"),
                               tot=("tot", "mean"), s=("s", "mean"), sd_=("u", "std"))
        r["t"] = r["u"] / (r["sd_"] / np.sqrt(r["n"]))
        return r.drop(columns="sd_").round(4)
    out["all_by_signed_er_dec"] = tab(G, "er", 10)
    x = G.dropna(subset=["er"])
    sl = stats.linregress(x["er"], x["s"]); out["slope_s_on_er"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(x)})
    up = x[x["er"] > 0]
    sl2 = stats.linregress(up["er"], up["s"]); out["slope_s_on_er_rising"] = pd.Series({"slope": sl2.slope, "t": sl2.slope / sl2.stderr, "n": len(up)})
    dn = x[x["er"] < 0]
    sl3 = stats.linregress(dn["er"], dn["s"]); out["slope_s_on_er_falling"] = pd.Series({"slope": sl3.slope, "t": sl3.slope / sl3.stderr, "n": len(dn)})
    hi_up = x[x["er"] > 0.4]
    yr = hi_up.groupby("yr").agg(n=("u", "size"), u=("u", "mean"), tot=("tot", "mean"), sd_=("u", "std"))
    yr["t"] = yr["u"] / (yr["sd_"] / np.sqrt(yr["n"])); out["clean_rise_by_year"] = yr.drop(columns="sd_").round(4)
    cn = hi_up.groupby("coin").agg(n=("u", "size"), u=("u", "mean")).round(4)
    out["clean_rise_coins_pos_share"] = pd.Series({"coins": len(cn), "share_u_pos": (cn["u"] > 0).mean(), "median_u": cn["u"].median()})
    # 10-day horizon on 10-grid
    G10 = A[A["i"] % 10 == 0].dropna(subset=["fwd10", "er"]).copy()
    G10["u"] = G10["fwd10"] - G10["coin"].map(G10.groupby("coin")["fwd10"].mean()); G10["tot"] = G10["fwd10"]
    G10["s"] = G10["u"] / G10["coin"].map(G10.groupby("coin")["fwd10"].std())
    out["10d_by_signed_er_q5"] = tab(G10, "er", 5)
    # vol_rel top by year
    v = G.dropna(subset=["vol_rel"]); vt = v[v["vol_rel"] > v["vol_rel"].quantile(0.8)]
    vy = vt.groupby("yr").agg(n=("u", "size"), u=("u", "mean"), sd_=("u", "std")); vy["t"] = vy["u"] / (vy["sd_"] / np.sqrt(vy["n"]))
    out["highvol_by_year"] = vy.drop(columns="sd_").round(4)
    # big down day by year
    bd = G[G["r1"] < G["r1"].quantile(0.2)]
    by = bd.groupby("yr").agg(n=("u", "size"), u=("u", "mean"), sd_=("u", "std")); by["t"] = by["u"] / (by["sd_"] / np.sqrt(by["n"]))
    out["bigdown_day_by_year"] = by.drop(columns="sd_").round(4)
    return out
