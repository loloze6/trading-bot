def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    comps = ["mom28","rev1","high90","vol30"]
    def grid(h, phase=0):
        rows = []
        for coin, ws in bars.items():
            for w, df in ws.items():
                df = df.reset_index(drop=True)
                c = df["close"].values
                n = len(df)
                idx = np.arange(phase, n - h, h)
                if len(idx) == 0: continue
                r = c[idx + h] / c[idx] - 1
                d = pd.DataFrame({"coin": coin, "win": w, "r": r,
                                  "f": df["forecast"].values[idx]})
                for k in comps:
                    d[k] = df[f"debug_info.components.{k}.post_pipeline_value"].values[idx]
                d["rawvol"] = df["debug_info.components.vol30.last_history_value"].values[idx]
                rows.append(d)
        g = pd.concat(rows, ignore_index=True)
        g["ex"] = g["r"] - g.groupby("coin")["r"].transform("mean")
        g["p"] = g["f"] * g["ex"]
        return g
    def t(x):
        x = pd.Series(x).dropna()
        return x.mean() / (x.std() / np.sqrt(len(x)))
    # 5d grid phase sensitivity
    ph = {}
    for p in range(5):
        g = grid(5, p)
        ph[p] = {"n": len(g), "t_forecast": t(g["p"]), **{f"t_{k}": t(g[k] * g["ex"]) for k in comps}}
    out["5d_by_phase"] = pd.DataFrame(ph).T
    # components by horizon
    hz = {}
    for h in [1, 2, 3, 5, 10, 20]:
        g = grid(h)
        no_rev = (g["mom28"] + g["high90"] + g["vol30"] + 2 * 10) / 5  # approx centring
        hz[h] = {"n": len(g), "t_forecast": t(g["p"]), **{f"t_{k}": t(g[k] * g["ex"]) for k in comps},
                 "t_mom_plus_high": t((g["mom28"] + g["high90"] + 10) * g["ex"]),
                 "corr_f_ex": g["f"].corr(g["ex"])}
    out["components_by_horizon"] = pd.DataFrame(hz).T
    # 10d: by year-ish halves via window, and by coin
    g = grid(10)
    out["10d_by_coin"] = g.groupby("coin")["p"].apply(t)
    g["half"] = np.where(g["win"].str[1:].astype(int) <= 12, "w1-w12", "w13-w24")
    out["10d_by_half"] = g.groupby("half")["p"].apply(t)
    g["side"] = np.where(g["f"] > 0, "long", "short")
    out["10d_side_mean_ex"] = g.groupby("side")["ex"].agg(["mean", "size"])
    g["volq"] = g.groupby("coin")["rawvol"].transform(lambda s: pd.qcut(s.rank(method="first"), 2, labels=["low", "high"]))
    out["10d_by_vol"] = g.groupby("volq")["p"].apply(t)
    out["10d_size"] = pd.Series({"mean_abs_f": g["f"].abs().mean(),
                                 "unusual_move_in_dir": (np.sign(g["f"]) * g["ex"]).mean(),
                                 "usual_move_sd": g["r"].std()})
    return out
