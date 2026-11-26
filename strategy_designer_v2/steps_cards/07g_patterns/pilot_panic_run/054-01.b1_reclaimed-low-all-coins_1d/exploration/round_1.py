def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 5
    rows = []
    coin_mean = {}
    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            for i in range(0, n - H, H):
                grid_rets.append(c[i + H] / c[i] - 1)
        coin_mean[coin] = np.mean(grid_rets) if grid_rets else np.nan
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            n = len(df)
            lo, hi, cl, op = df["low"], df["high"], df["close"], df["open"]
            plow = lo.shift(1).rolling(30).min()
            phigh = hi.shift(1).rolling(30).max()
            fwd = cl.shift(-H) / cl - 1
            fwd1 = cl.shift(-1) / cl - 1
            r1 = cl / cl.shift(1) - 1
            tr60 = cl / cl.shift(60) - 1
            vol30 = r1.rolling(30).std()
            rng = (hi - lo) / cl.shift(1)
            pos_in_rng = (cl - lo) / (hi - lo)
            d = pd.DataFrame({
                "coin": coin, "win": w, "i": np.arange(n), "cell": np.arange(n) // H,
                "day": df["timestamp"].astype(str).str[:10],
                "wd": pd.to_datetime(df["timestamp"]).dt.weekday,
                "fwd": fwd, "fwd1": fwd1, "r1": r1, "tr60": tr60, "vol30": vol30,
                "rng": rng, "pos": pos_in_rng,
                "plow": plow, "phigh": phigh, "lo": lo, "hi": hi, "cl": cl,
                "regime": df["regime"], "alloc": df["postRebalance_current_allocation"],
            })
            d["exc"] = d["fwd"] - coin_mean[coin]
            d["pierce_rec"] = (d.lo < d.plow) & (d.cl >= d.plow)
            d["pierce_fail"] = (d.lo < d.plow) & (d.cl < d.plow)
            d["hpierce_rej"] = (d.hi > d.phigh) & (d.cl <= d.phigh)
            d["hpierce_hold"] = (d.hi > d.phigh) & (d.cl > d.phigh)
            d["depth"] = (d.plow - d.lo) / d.plow
            d["hdepth"] = (d.hi - d.phigh) / d.phigh
            d["volz"] = d.vol30 / d.vol30.expanding(20).median()
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D = D[D.fwd.notna()]

    def summ(mask, col="exc"):
        s = D[mask].copy()
        s = s.sort_values("i").groupby(["coin", "win", "cell"]).head(1)
        s = s[s[col].notna()]
        if len(s) < 3:
            return pd.Series({"n": len(s)})
        g = (s.groupby("day")[col].sum())
        G = len(g)
        m = s[col].mean()
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(s) if G > 1 else np.nan
        return pd.Series({"n": len(s), "days": G, "mean": m, "t_dayclust": m / se if se else np.nan,
                          "hit": (s[col] > 0).mean()})

    out = {}
    base = pd.Series(True, index=D.index)
    tr = D.tr60
    groups = {
        "all bars": base,
        "low pierce reclaimed": D.pierce_rec,
        "low pierce reclaimed, tr60<-10%": D.pierce_rec & (tr < -0.10),
        "low pierce reclaimed, tr60 -10..10": D.pierce_rec & tr.between(-0.10, 0.10),
        "low pierce reclaimed, tr60>10%": D.pierce_rec & (tr > 0.10),
        "low pierce closed below": D.pierce_fail,
        "low pierce closed below, tr60<-10%": D.pierce_fail & (tr < -0.10),
        "high pierce rejected": D.hpierce_rej,
        "high pierce rejected, tr60>10%": D.hpierce_rej & (tr > 0.10),
        "high pierce held": D.hpierce_hold,
        "high pierce held, tr60>10%": D.hpierce_hold & (tr > 0.10),
        "high pierce held, tr60 -10..10": D.hpierce_hold & tr.between(-0.10, 0.10),
        "regime mean_reversion": D.regime == "mean_reversion",
        "day down >1 vol": D.r1 < -D.vol30,
        "day down >2 vol": D.r1 < -2 * D.vol30,
        "day up >2 vol": D.r1 > 2 * D.vol30,
        "low close wide day (pos<0.2, rng>2vol)": (D.pos < 0.2) & (D.rng > 2 * D.vol30),
        "high close wide day (pos>0.8, rng>2vol)": (D.pos > 0.8) & (D.rng > 2 * D.vol30),
        "vol high (volz>1.2)": D.volz > 1.2,
        "vol low (volz<0.8)": D.volz < 0.8,
    }
    out["groups 5d excess"] = pd.DataFrame({k: summ(v) for k, v in groups.items()}).T
    # depth terciles for reclaimed pierce, all trends
    pr = D[D.pierce_rec].copy()
    pr["dq"] = pd.qcut(pr.depth, 3, labels=["shallow", "mid", "deep"])
    out["reclaim by depth tercile"] = pd.DataFrame({q: summ(D.index.isin(pr[pr.dq == q].index)) for q in ["shallow", "mid", "deep"]}).T
    hp = D[D.hpierce_hold].copy()
    hp["dq"] = pd.qcut(hp.hdepth, 3, labels=["shallow", "mid", "deep"])
    out["high break held by depth tercile"] = pd.DataFrame({q: summ(D.index.isin(hp[hp.dq == q].index)) for q in ["shallow", "mid", "deep"]}).T
    out["weekday 1d next return (all bars)"] = D.groupby("wd")["fwd1"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    out["by year: reclaimed pierce"] = D[D.pierce_rec].assign(yr=D.day.str[:4]).groupby("yr")["exc"].agg(["count", "mean"])
    out["by window: reclaimed pierce"] = D[D.pierce_rec].groupby("win")["exc"].agg(["count", "mean"])
    return out
