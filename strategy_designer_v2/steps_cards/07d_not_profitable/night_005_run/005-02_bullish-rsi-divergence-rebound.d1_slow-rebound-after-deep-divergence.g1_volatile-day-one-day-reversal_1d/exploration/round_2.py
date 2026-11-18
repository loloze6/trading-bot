def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        cr = pd.concat([data["days"][coin][w]["coin_return"] for w in wins], ignore_index=True)
        mu = cr.mean()
        for w, b in wins.items():
            b = b.copy()
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["ret1"]
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            b["net"] = b["gain"] - b["fee"]
            r = b["close"].pct_change()
            sd20 = r.rolling(20).std()
            b["z"] = r / sd20
            b["vr"] = sd20 / sd20.rolling(60).mean()
            b["r20"] = b["close"] / b["close"].shift(20) - 1
            b["coin"] = coin; b["w"] = w; b["mu"] = mu
            b["i"] = np.arange(len(b))
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    act = B[B["pos"].abs() > 1e-9].dropna(subset=["ret1", "z"]).copy()
    act["zb"] = pd.qcut(act["z"].abs(), 5, labels=False)
    g = act.groupby("zb")
    out["net_by_absz_q"] = pd.DataFrame({"n": g.size(), "gain": g["gain"].mean(), "fee": g["fee"].mean(),
        "net": g["net"].mean(), "abs_pos": g["pos"].apply(lambda s: s.abs().mean()),
        "t_gain": g["gain"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))})
    # reversal ret1*(-sign z) by |z| quintile on ALL bars with vr<1 vs vr>=1 (recomputed)
    A = B.dropna(subset=["ret1", "z", "vr"]).copy()
    A["rev"] = -np.sign(A["z"]) * (A["ret1"] - A["mu"])
    A["zb"] = pd.qcut(A["z"].abs(), 5, labels=False)
    A["hv"] = A["vr"] >= 1
    out["rev_by_absz_hv"] = A.groupby(["hv", "zb"]).agg(n=("rev", "size"), rev=("rev", "mean"),
        t=("rev", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))))
    # by sign of z and r20 sign, top two |z| quintiles in hv
    T = A[A["hv"] & (A["zb"] >= 3)].copy()
    T["dir"] = np.where(T["z"] > 0, "up_day", "down_day")
    T["trend"] = np.where(T["r20"] > 0, "r20_up", "r20_down")
    out["rev_bigmoves_by_dir_trend"] = T.groupby(["dir", "trend"]).agg(n=("rev", "size"), rev=("rev", "mean"),
        t=("rev", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))))
    # drawdown: deepest fall of each coin's chained book; bars inside it
    dd_info = []
    for coin in B["coin"].unique():
        x = B[B["coin"] == coin].copy()
        x["net"] = x["net"].fillna(0)
        eq = (1 + x["net"]).cumprod().values
        peak = np.maximum.accumulate(eq)
        ddv = eq / peak - 1
        trough = ddv.argmin()
        pk = np.where(eq[:trough + 1] == peak[trough])[0][-1]
        seg = x.iloc[pk:trough + 1]
        s = seg[seg["pos"].abs() > 1e-9]
        dd_info.append(pd.Series({"dd": ddv.min(), "bars": len(seg), "active": len(s),
            "share_long": (s["pos"] > 0).mean(), "gain_sum": seg["gain"].sum(), "fee_sum": seg["fee"].sum(),
            "mean_absz": s["z"].abs().mean(), "mean_vr": s["vr"].mean(), "coin_ret": seg["close"].iloc[-1] / seg["close"].iloc[0] - 1 if seg["w"].nunique() == 1 else np.nan,
            "n_windows": seg["w"].nunique(), "share_short_in_r20_up": ((s["pos"] < 0) & (s["r20"] > 0)).mean()},
            name=coin))
    out["deepest_fall"] = pd.DataFrame(dd_info)
    return out
