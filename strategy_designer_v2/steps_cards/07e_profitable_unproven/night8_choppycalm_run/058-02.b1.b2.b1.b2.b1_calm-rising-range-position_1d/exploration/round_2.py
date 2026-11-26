def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    cm = {}
    for c in days:
        r = pd.concat([d["coin_return"] for d in days[c].values()]).dropna()
        cm[c] = r.mean()
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            a = b["postRebalance_current_allocation"].fillna(0)
            nr = b["close"].shift(-1) / b["close"] - 1
            hi = b["high"].rolling(20).max(); lo = b["low"].rolling(20).min()
            pos = 2 * (b["close"] - lo) / (hi - lo) - 1
            r60 = b["close"] / b["close"].shift(60) - 1
            vol = b["close"].pct_change().rolling(30).std()
            vr = vol / vol.rolling(180, min_periods=60).median()
            rows.append(pd.DataFrame({"coin": c, "w": w, "a": a, "g": a * nr, "mkt": a * cm[c], "pos": pos,
                                      "fc": b["forecast"], "r60": r60, "vr": vr, "inp": b["regime"] == "unknown",
                                      "year": pd.to_datetime(b["timestamp"]).dt.year}))
    R = pd.concat(rows).dropna(subset=["g"])
    I = R[R.a != 0].copy()
    I["side"] = np.where(I.a > 0, "long", "short")
    I["pq"] = pd.cut(I["pos"], [-1.01, -0.5, 0, 0.5, 0.9, 1.01], labels=["<-.5", "-.5-0", "0-.5", ".5-.9", ">.9"])
    out["gain_by_side_rawpos"] = I.groupby(["side", "pq"]).agg(n=("g", "size"), sum_g=("g", "sum"), mean_g=("g", "mean"), sum_mkt=("mkt", "sum")).dropna()
    I["tq"] = pd.qcut(I["r60"], 4, labels=["t1low", "t2", "t3", "t4high"])
    out["gain_long_by_r60_quart"] = I[I.side == "long"].groupby("tq").agg(n=("g", "size"), r60_med=("r60", "median"), mean_g=("g", "mean"), sum_g=("g", "sum"), t=("g", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    out["gain_long_by_year_excl"] = I[I.side == "long"].groupby("year").agg(n=("g", "size"), mean_g=("g", "mean"), t=("g", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    # book daily excluding 2020
    bd = []
    for c in days:
        for w, d in days[c].items():
            bd.append(pd.DataFrame({"day": d["day"], "w": w, "br": d["book_return"], "cr": d["coin_return"]}))
    Bd = pd.concat(bd).dropna().groupby(["w", "day"])[["br", "cr"]].mean().reset_index()
    Bd["year"] = pd.to_datetime(Bd["day"]).dt.year
    out["book_by_year"] = Bd.groupby("year").agg(n=("br", "size"), mean=("br", "mean"), sharpe=("br", lambda x: x.mean() / x.std() * np.sqrt(365)), hold_mean=("cr", "mean"))
    s = Bd["br"].sort_values(ascending=False)
    out["book_without_top10_days"] = pd.Series({"mean_all": s.mean(), "mean_wo_top10": s.iloc[10:].mean(), "sharpe_wo_top10": s.iloc[10:].mean() / s.iloc[10:].std() * np.sqrt(365)})
    # non-overlapping 10d test: raw pos (unstandardised) and r60 strength, in profile, long-only excess
    res = []
    for c in bars:
        fr_all = []
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            fr_all.append((b["close"].shift(-10) / b["close"] - 1).iloc[::10])
        fa = pd.concat(fr_all).dropna(); m10, s10 = fa.mean(), fa.std()
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            hi = b["high"].rolling(20).max(); lo = b["low"].rolling(20).min()
            pos = 2 * (b["close"] - lo) / (hi - lo) - 1
            r60 = b["close"] / b["close"].shift(60) - 1
            hi60 = b["high"].rolling(60, min_periods=40).max()
            dist60 = b["close"] / hi60 - 1
            fr = b["close"].shift(-10) / b["close"] - 1
            idx = np.arange(0, len(b), 10)
            d = pd.DataFrame({"pos": pos.iloc[idx], "r60": r60.iloc[idx], "d60": dist60.iloc[idx], "fr": fr.iloc[idx],
                              "inp": (b["regime"] == "unknown").iloc[idx], "fc": b["forecast"].iloc[idx]})
            d["ex"] = (d.fr - m10) / s10; d["coin"] = c
            res.append(d)
    D = pd.concat(res).dropna(subset=["fr", "pos"])
    P = D[D.inp]
    def cr(g, x):
        g = g.dropna(subset=[x]); r = stats.spearmanr(g[x], g["ex"]); return pd.Series({"rho": r[0], "p": r[1], "n": len(g)})
    out["inprof_corr_10d"] = pd.DataFrame({x: cr(P, x) for x in ["pos", "fc", "r60", "d60"]}).T
    out["outprof_corr_10d"] = pd.DataFrame({x: cr(D[~D.inp], x) for x in ["pos", "fc", "r60", "d60"]}).T
    P = P.copy(); P["fsign"] = np.sign(P.fc)
    P["pq"] = pd.cut(P["pos"], [-1.01, 0, 0.5, 0.9, 1.01])
    out["inprof_fc_sign_vs_pos"] = P.groupby(["fsign", "pq"])["ex"].agg(["size", "mean"])
    P["dq"] = pd.qcut(P["d60"], 4)
    out["inprof_ex_by_dist60high"] = P.groupby("dq")["ex"].agg(["size", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    return out
