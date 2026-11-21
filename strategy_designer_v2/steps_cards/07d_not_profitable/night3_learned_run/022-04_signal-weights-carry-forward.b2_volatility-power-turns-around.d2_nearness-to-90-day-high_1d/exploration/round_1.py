def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    # per-bar gain decomposition
    rows = []
    grid = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            pos = b["postRebalance_current_allocation"].astype(float)
            r1 = b["close"].shift(-1) / b["close"] - 1
            g = pos * r1
            fc = b["forecast"].astype(float)
            ret30 = b["close"] / b["close"].shift(30) - 1
            vol = b["close"].pct_change().rolling(30).std()
            rows.append(pd.DataFrame({"coin": c, "w": w, "pos": pos, "r1": r1, "g": g, "fc": fc}))
            idx = np.arange(0, len(b) - 5, 5)
            f5 = (b["close"].shift(-5) / b["close"] - 1).iloc[idx]
            grid.append(pd.DataFrame({"coin": c, "w": w, "fc": fc.iloc[idx].values, "f5": f5.values,
                                      "pos": pos.iloc[idx].values, "ret30": ret30.iloc[idx].values,
                                      "vol": vol.iloc[idx].values}))
    R = pd.concat(rows).dropna(subset=["r1"])
    G = pd.concat(grid).dropna(subset=["f5"])
    drift = G.groupby("coin")["f5"].transform("mean")
    G["ex5"] = G["f5"] - drift
    md = R.groupby("coin")["r1"].transform("mean")
    R["mkt"] = R["pos"] * md
    R["side"] = np.where(R["pos"] > 0.01, "long", np.where(R["pos"] < -0.01, "short", "flat"))
    out["by_side"] = R.groupby("side").agg(share=("g", "size"), mean_pos=("pos", "mean"),
                                          gain=("g", "mean"), mkt=("mkt", "mean"), coin_r=("r1", "mean"))
    out["by_side"]["share"] = out["by_side"]["share"] / len(R)
    out["gain_sum_by_side_per_bar"] = (R.groupby("side")["g"].sum() / len(R)).to_frame("contrib")
    out["by_coin"] = R.groupby("coin").agg(gain=("g", "mean"), mkt=("mkt", "mean"), pos=("pos", "mean"),
                                          coin_r=("r1", "mean"))
    G["fq"] = pd.qcut(G["fc"], 5, labels=False, duplicates="drop")
    out["fwd5_by_forecast_q"] = G.groupby("fq").agg(n=("f5", "size"), fc=("fc", "mean"), pos=("pos", "mean"),
                                                   f5=("f5", "mean"), ex5=("ex5", "mean"),
                                                   ex5_sd=("ex5", "std"))
    # in trend regimes
    G["trend"] = np.where(G["ret30"] > 0, "up30", "down30")
    G["vq"] = G.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    def slope(df):
        df = df.dropna(subset=["fc", "ex5"])
        if len(df) < 30: return pd.Series({"n": len(df)})
        s = stats.linregress(df["fc"], df["ex5"])
        return pd.Series({"n": len(df), "slope": s.slope, "t": s.slope / s.stderr, "ex5": df["ex5"].mean()})
    out["slope_by_trend"] = G.groupby("trend").apply(slope)
    out["slope_by_volq"] = G.groupby("vq").apply(slope)
    out["slope_by_coin"] = G.groupby("coin").apply(slope)
    # book daily, per window
    win_order = sorted(days[coins[0]].keys(), key=lambda x: int(x[1:]))
    chain = []
    for w in win_order:
        br = pd.concat([days[c][w].set_index("day")["book_return"] for c in coins if w in days[c]], axis=1).mean(axis=1)
        cr = pd.concat([days[c][w].set_index("day")["coin_return"] for c in coins if w in days[c]], axis=1).mean(axis=1)
        pp = pd.concat([bars[c][w].assign(day=pd.to_datetime(bars[c][w]["timestamp"]).dt.floor("D")).groupby("day")["postRebalance_current_allocation"].last() for c in coins if w in bars[c]], axis=1).mean(axis=1)
        d = pd.DataFrame({"br": br, "cr": cr}).dropna()
        d["pos"] = pp.reindex(d.index).values
        d["w"] = w
        chain.append(d.reset_index(drop=True))
    D = pd.concat(chain, ignore_index=True)
    eq = (1 + D["br"]).cumprod(); dd = eq / eq.cummax() - 1
    ceq = (1 + D["cr"]).cumprod(); cdd = ceq / ceq.cummax() - 1
    out["book_vs_hold"] = pd.DataFrame({"book": [D["br"].mean(), D["br"].std(), dd.min()],
                                        "hold": [D["cr"].mean(), D["cr"].std(), cdd.min()]},
                                       index=["mean", "sd", "maxdd"])
    tr = dd.idxmin(); pk = eq.iloc[:tr + 1].idxmax()
    seg = D.iloc[pk:tr + 1]
    out["deepest_fall"] = pd.DataFrame({"days": [tr - pk], "book_fall": [dd.min()],
                                        "coin_chain": [(1 + seg["cr"]).prod() - 1],
                                        "mean_pos": [seg["pos"].mean()],
                                        "windows": [seg["w"].nunique()]})
    out["fall_windows"] = seg.groupby("w").agg(n=("br", "size"), br=("br", lambda s: (1 + s).prod() - 1),
                                              cr=("cr", lambda s: (1 + s).prod() - 1), pos=("pos", "mean"))
    out["by_window"] = D.groupby("w").agg(br=("br", "mean"), cr=("cr", "mean"), pos=("pos", "mean")).reindex(win_order)
    # daily gain by position sign while coin up/down
    D["pside"] = np.where(D["pos"] > 0.05, "net_long", np.where(D["pos"] < -0.05, "net_short", "near_flat"))
    out["daily_by_pside"] = D.groupby("pside").agg(n=("br", "size"), br=("br", "mean"), cr=("cr", "mean"), sd=("br", "std"))
    return out
