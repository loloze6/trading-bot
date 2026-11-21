def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    daily = []
    pos = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(b)
            r1 = c.pct_change()
            f = pd.DataFrame({
                "coin": coin, "win": w,
                "ret28": c / c.shift(28) - 1,
                "ret1": r1,
                "ret1z": r1 / r1.rolling(30).std(),
                "ret5p": c / c.shift(5) - 1,
                "near60": c / c.rolling(60).max(),
                "vol30": r1.rolling(30).std(),
                "fc": b["forecast"].astype(float),
                "comb": b.get("debug_info.components.combined.post_pipeline_value"),
                "best": b.get("debug_info.components.best.post_pipeline_value"),
                "y": c.shift(-5) / c - 1,
                "y1": c.shift(-1) / c - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
            })
            g = f.iloc[::5]
            g = g[g["y"].notna()]
            rows.append(g)
            daily.append(pd.DataFrame({"coin": coin, "wd": f["wd"], "r": r1}))
            a = b["postRebalance_current_allocation"].astype(float)
            pos.append(pd.DataFrame({"coin": coin, "a": a, "nr": c.shift(-1) / c - 1}))
    G = pd.concat(rows, ignore_index=True)
    G["y"] = G["y"] - G.groupby("coin")["y"].transform("mean")
    out = {}
    sig = []
    for s in ["ret28", "ret1", "ret1z", "ret5p", "near60", "vol30", "fc", "comb", "best"]:
        d = G[[s, "y", "coin"]].dropna()
        d = d.assign(rk=d.groupby("coin")[s].rank(pct=True))
        r, p = stats.pearsonr(d[s], d["y"])
        rs, _ = stats.spearmanr(d[s], d["y"])
        top = d[d.rk > 0.8]["y"]; bot = d[d.rk <= 0.2]["y"]
        t = stats.ttest_ind(top, bot, equal_var=False).statistic
        sig.append([s, len(d), round(r, 4), round(rs, 4), round(top.mean()*100, 3), round(bot.mean()*100, 3), round(t, 2)])
    out["signal_vs_next5d (y demeaned, top-bottom quintile per coin)"] = pd.DataFrame(sig, columns=["sig", "n", "pearson", "spearman", "top%", "bot%", "t_top_bot"])
    # quintiles of combined and of ret1z
    for s in ["comb", "ret1z", "vol30", "ret28"]:
        d = G[[s, "y", "coin"]].dropna()
        d["q"] = d.groupby("coin")[s].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
        out["quintile_" + s] = d.groupby("q")["y"].agg(["count", "mean", "std"]).assign(t=lambda x: x["mean"] / (x["std"] / np.sqrt(x["count"])))
    # per coin correlation of comb and ret1z
    pc = []
    for coin, d in G.groupby("coin"):
        e = d[["comb", "ret1z", "ret28", "y"]].dropna()
        pc.append([coin, len(e), round(e["comb"].corr(e["y"]), 3), round(e["ret1z"].corr(e["y"]), 3), round(e["ret28"].corr(e["y"]), 3)])
    out["per_coin_corr"] = pd.DataFrame(pc, columns=["coin", "n", "comb", "ret1z", "ret28"])
    # absolute next move by vol quintile
    d = G[["vol30", "y", "coin"]].dropna()
    d["q"] = d.groupby("coin")["vol30"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["abs_next5d_by_vol_q"] = d.assign(ay=d.y.abs()).groupby("q")["ay"].mean()
    # weekday
    D = pd.concat(daily).dropna()
    D["r"] = D["r"] - D.groupby("coin")["r"].transform("mean")
    out["weekday_daily_ret"] = D.groupby("wd")["r"].agg(["count", "mean", "std"]).assign(t=lambda x: x["mean"] / (x["std"] / np.sqrt(x["count"])))
    # position decomposition
    P = pd.concat(pos).dropna()
    P["mu"] = P.groupby("coin")["nr"].transform("mean")
    P["gain"] = P.a * P.nr; P["drift"] = P.a * P.mu
    out["position_gain"] = P.groupby("coin")[["a", "gain", "drift"]].mean().assign(timing=lambda x: x.gain - x.drift, long_share=P.groupby("coin")["a"].apply(lambda s: (s > 0).mean()))
    return out
