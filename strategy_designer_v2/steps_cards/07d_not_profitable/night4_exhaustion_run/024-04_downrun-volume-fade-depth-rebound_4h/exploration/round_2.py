def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["bars"].keys())
    rows = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            r1 = b["close"].shift(-1) / b["close"] - 1
            a = b["postRebalance_current_allocation"]
            fwd18 = b["close"].shift(-18) / b["close"] - 1
            ret30 = b["close"] / b["close"].shift(180) - 1
            ret90 = b["close"] / b["close"].shift(540) - 1
            lr = np.log(b["close"]).diff()
            vr = lr.rolling(42).std() / lr.rolling(180).std()
            rows.append(pd.DataFrame({"coin": c, "w": w, "a": a, "g": a * r1, "r1": r1,
                "f": b["forecast"], "fwd18": fwd18, "ret30": ret30, "ret90": ret90, "vr": vr,
                "sl": b["debug_info.components.streak_loss.last_history_value"],
                "vf": b["debug_info.components.volume_fade.last_history_value"],
                "pos": np.arange(len(b)), "wn": int(w[1:])}))
    B = pd.concat(rows, ignore_index=True)
    out["share_forecast_pos"] = float((B["f"] > 0).mean())
    out["share_forecast_zero"] = float((B["f"] == 0).mean())
    B["fstate"] = np.where(B["f"] > 0, "f>0", np.where(B["f"] == 0, "f=0", "f<0"))
    out["by_forecast_state"] = B.dropna(subset=["g"]).groupby("fstate").agg(
        n=("g", "size"), mean_alloc=("a", "mean"), mean_gain=("g", "mean"), sum_gain=("g", "sum"))
    out["forecast_pos_quantiles"] = B.loc[B["f"] > 0, "f"].describe()
    # deepest fall windows w12-w16 vs others
    B["period"] = np.where(B["wn"].between(12, 16), "w12-w16", "other")
    out["fall_vs_other"] = B.dropna(subset=["g"]).groupby("period").agg(
        mean_alloc=("a", "mean"), mean_gain=("g", "mean"), mean_r1=("r1", "mean"), share_ret30_neg=("ret30", lambda x: (x < 0).mean()))
    drift = B[B["pos"] % 18 == 0]["fwd18"].mean()
    def tt(x): return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
    # gain on long bars by ret90 sign and vr
    L = B[B["a"] > 0].dropna(subset=["g", "ret90"])
    out["gain_by_ret90_quintile"] = L.groupby(pd.qcut(L["ret90"], 5)).agg(
        n=("g", "size"), mean_gain=("g", "mean"), sum_gain=("g", "sum"), sd_gain=("g", "std"))
    # grid cases inside streaks: fwd18 excess by streak loss quintile, split by ret30 sign
    S = B[(B["pos"] % 18 == 0) & (B["f"] > 0)].dropna(subset=["fwd18", "sl", "ret30"]).copy()
    S["ex"] = S["fwd18"] - drift
    S["up30"] = np.where(S["ret30"] > 0, "ret30>0", "ret30<=0")
    S["slq"] = pd.qcut(S["sl"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["case_ex_by_sl_and_trend"] = S.groupby(["up30", "slq"]).agg(n=("ex", "size"), mean_ex=("ex", "mean"), t=("ex", tt))
    S["vrq"] = pd.qcut(S["vr"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["case_ex_by_vr"] = S.groupby("vrq").agg(n=("ex", "size"), mean_ex=("ex", "mean"), t=("ex", tt), mean_vr=("vr", "mean"))
    out["sl_describe"] = S["sl"].describe()
    # daily book dd by window chain: worst 5 window book sums and holding sums already seen; compute corr of book with coin daily
    dr = []
    for c in coins:
        for w, d in data["days"][c].items():
            dr.append(d[["book_return", "coin_return"]].dropna())
    D = pd.concat(dr)
    out["corr_book_coin_daily"] = float(D["book_return"].corr(D["coin_return"]))
    out["beta_book_coin"] = float(np.polyfit(D["coin_return"], D["book_return"], 1)[0])
    return out
