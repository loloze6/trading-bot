def explore(data):
    import pandas as pd, numpy as np
    out = {}
    R = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            cl = b["close"]
            r1 = cl.pct_change()
            vol = r1.rolling(30).std()
            b["z"] = r1 / vol
            b["r30"] = cl / cl.shift(30) - 1
            b["volratio"] = r1.rolling(7).std() / vol
            b["nxt"] = cl.shift(-1) / cl - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["nxt"]
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["coin"] = c; b["wn"] = int(w[1:])
            R.append(b[["coin", "wn", "day", "z", "r30", "volratio", "nxt", "pos", "gain", "forecast"]])
    A = pd.concat(R).dropna(subset=["nxt", "r30", "volratio"])
    mu = A.groupby("coin")["nxt"].transform("mean")
    A["ex"] = A["nxt"] - mu
    act = A[A["forecast"] > 0].copy()
    act["vq"] = pd.qcut(act["volratio"], 3, labels=["vr_low", "vr_mid", "vr_high"])
    act["rq"] = pd.qcut(act["r30"], 3, labels=["r30_low", "r30_mid", "r30_high"])
    g = act.groupby(["vq", "rq"], observed=True).agg(n=("ex", "size"), ex=("ex", "mean"), sd=("nxt", "std"),
                                                    gain_sum=("gain", "sum"), gain_sd=("gain", "std"), pos=("pos", "mean"))
    g["t"] = g["ex"] / (g["sd"] / np.sqrt(g["n"]))
    out["vr_x_r30"] = g
    # book-level: daily gain per day (mean over coins) and drawdown, gain split by volratio tercile
    act["gain_scaled"] = act["gain"] / 6.0
    daily = act.groupby(["wn", "day", "vq"], observed=True)["gain_scaled"].sum().unstack("vq").fillna(0)
    allD = A.groupby(["wn", "day"]).size().index
    daily = daily.reindex(allD).fillna(0).sort_index()
    tot = daily.sum(axis=1)
    def stats_(s):
        eq = (1 + s).cumprod().values
        dd = eq / np.maximum.accumulate(eq) - 1
        yr = eq[-1] ** (365 / len(s)) - 1
        return pd.Series({"mean": s.mean(), "sharpe": s.mean() / s.std() * np.sqrt(365), "yearly": yr,
                          "deepest": dd.min(), "calmar": yr / -dd.min()})
    res = {"all": stats_(tot), "drop_vr_low": stats_(daily["vr_mid"] + daily["vr_high"]),
           "vr_high_only": stats_(daily["vr_high"])}
    out["approx_book_by_vr"] = pd.DataFrame(res)
    # during deepest-fall days of approx book: share of losses by tercile
    eq = (1 + tot).cumprod().values
    dd = eq / np.maximum.accumulate(eq) - 1
    k = int(np.argmin(dd)); s = k
    while s > 0 and dd[s - 1] < 0: s -= 1
    seg = daily.iloc[s:k + 1]
    out["deepest_fall_contrib_by_vr"] = seg.sum()
    out["deepest_fall_len"] = k - s + 1
    # losses by volratio on all drawdown days
    indd = dd < -0.10
    out["deep_dd_days_contrib_by_vr"] = daily[indd].sum()
    return out
