def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["days"].keys())
    wins = [f"w{i}" for i in range(1, 25)]
    # book daily returns: per window, mean over coins per day
    perwin = []
    for w in wins:
        frames = []
        for c in coins:
            d = data["days"][c].get(w)
            if d is None: continue
            frames.append(d.set_index("day")[["book_return", "coin_return"]].add_suffix("_" + c))
        if not frames: continue
        df = pd.concat(frames, axis=1)
        br = df[[k for k in df.columns if k.startswith("book_return")]].mean(axis=1)
        cr = df[[k for k in df.columns if k.startswith("coin_return")]].mean(axis=1)
        perwin.append(pd.DataFrame({"w": w, "b": br.values, "c": cr.values}))
    allb = pd.concat(perwin, ignore_index=True).dropna()
    eq = (1 + allb["b"]).cumprod()
    dd = eq / eq.cummax() - 1
    allb["dd"] = dd.values
    # per window summary
    g = allb.groupby("w", sort=False)
    ws = pd.DataFrame({"book_sum": g["b"].sum(), "coin_sum": g["c"].sum(),
                       "min_dd_in_chain": g["dd"].min(),
                       "book_sd": g["b"].std()})
    out["per_window"] = ws
    out["max_dd"] = float(dd.min())
    # trough location
    ti = int(dd.values.argmin())
    pk = int(eq.values[:ti + 1].argmax())
    out["dd_peak_trough_windows"] = f"{allb['w'].iloc[pk]} -> {allb['w'].iloc[ti]}, days {ti - pk}"
    # bar-level: gain = alloc * next return, grouped by state known at close
    rows = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            r1 = b["close"].shift(-1) / b["close"] - 1
            a = b["postRebalance_current_allocation"]
            ret30 = b["close"] / b["close"].shift(180) - 1
            ret7 = b["close"] / b["close"].shift(42) - 1
            lr = np.log(b["close"]).diff()
            vol30 = lr.rolling(180).std()
            vol7 = lr.rolling(42).std()
            fwd18 = b["close"].shift(-18) / b["close"] - 1
            sl = b["debug_info.components.streak_loss.last_history_value"]
            rows.append(pd.DataFrame({"coin": c, "w": w, "a": a, "g": a * r1, "r1": r1,
                                      "ret30": ret30, "ret7": ret7, "vr": vol7 / vol30,
                                      "fwd18": fwd18, "f": b["forecast"], "sl": sl,
                                      "pos": np.arange(len(b))}))
    B = pd.concat(rows, ignore_index=True)
    L = B[B["a"] > 0].dropna(subset=["g", "ret30"])
    out["share_bars_long"] = float((B["a"] > 0).mean())
    out["gain_by_ret30_quintile"] = L.groupby(pd.qcut(L["ret30"], 5)).agg(
        n=("g", "size"), mean_gain=("g", "mean"), sum_gain=("g", "sum"), mean_alloc=("a", "mean"), mean_r1=("r1", "mean"))
    L2 = L.dropna(subset=["ret7"])
    out["gain_by_ret7_quintile"] = L2.groupby(pd.qcut(L2["ret7"], 5)).agg(
        n=("g", "size"), mean_gain=("g", "mean"), sum_gain=("g", "sum"), mean_r1=("r1", "mean"))
    L3 = L.dropna(subset=["vr"])
    out["gain_by_volratio_quintile"] = L3.groupby(pd.qcut(L3["vr"], 5)).agg(
        n=("g", "size"), mean_gain=("g", "mean"), sum_gain=("g", "sum"), sd_gain=("g", "std"))
    # signal-bar grid cases: forecast>0 on grid positions, fwd18 by ret30 quintile
    S = B[(B["pos"] % 18 == 0) & (B["f"] > 0)].dropna(subset=["fwd18", "ret30"])
    drift = B[B["pos"] % 18 == 0]["fwd18"].mean()
    S = S.assign(ex=S["fwd18"] - drift)
    def tt(x): return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
    out["grid_long_fwd18_by_ret30"] = S.groupby(pd.qcut(S["ret30"], 5)).agg(
        n=("ex", "size"), mean_ex=("ex", "mean"), t=("ex", tt), sd=("fwd18", "std"))
    out["drift18"] = float(drift)
    return out
