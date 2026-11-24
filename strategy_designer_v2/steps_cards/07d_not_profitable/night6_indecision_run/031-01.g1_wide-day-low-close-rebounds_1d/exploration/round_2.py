def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    wins = sorted({w for c in data["days"] for w in data["days"][c]}, key=lambda s: int(s[1:]))
    rows = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; h = b["high"]; l = b["low"]
            rng = h - l
            df = pd.DataFrame({
                "coin": c, "w": w, "wi": int(w[1:]), "pos": np.arange(len(b)),
                "fwd1": cl.shift(-1) / cl - 1,
                "fwd2": cl.shift(-2) / cl - 1,
                "ret1": cl / cl.shift(1) - 1,
                "rmult": rng / rng.rolling(20).mean(),
                "cloc": (cl - l) / rng.replace(0, np.nan),
                "vol20": cl.pct_change().rolling(20).std(),
                "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                "dret": (cl.pct_change() .abs()) / cl.pct_change().rolling(20).std().shift(1),
            })
            df["drop_z"] = -df["ret1"] / df["vol20"].shift(1)
            rows.append(df)
    a = pd.concat(rows, ignore_index=True)
    drift = a.groupby("coin")["fwd1"].mean()
    a["ex1"] = a["fwd1"] - a["coin"].map(drift)
    a["volq"] = a.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 4, labels=False, duplicates="drop"))
    sig = a[(a["fc"] > 0)].dropna(subset=["fwd1"]).copy()
    sig["pnl"] = sig["alloc"] * sig["fwd1"]
    sig["pnl_eq"] = sig["fwd1"]
    def summ(g, col="ex1"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": stats.ttest_1samp(x, 0).statistic if len(x) > 2 else np.nan,
                          "mean_alloc": g["alloc"].mean() if "alloc" in g else np.nan, "pnl_sum": g["pnl"].sum() if "pnl" in g else np.nan})
    # signal by coin-relative vol quartile vs non-signal
    out["sig_by_coin_volq"] = sig.groupby("volq").apply(summ)
    nons = a[(a["fc"] <= 0) | a["fc"].isna()].dropna(subset=["fwd1"])
    out["nonsig_by_coin_volq"] = nons.groupby("volq").apply(lambda g: pd.Series({"n": len(g), "mean": g["ex1"].mean(), "t": stats.ttest_1samp(g["ex1"], 0).statistic}))
    # drop strength
    sig["dzq"] = pd.qcut(sig["drop_z"], 4, labels=False, duplicates="drop")
    out["sig_by_drop_z"] = sig.groupby("dzq").apply(summ)
    out["sig_drop_z_edges"] = sig.groupby("dzq")["drop_z"].agg(["min", "max"])
    # non-signal big down days by drop_z (condition alone)
    nd = nons[nons["drop_z"] > 1.5]
    out["nonsig_dropz_gt1.5"] = pd.Series({"n": len(nd), "mean": nd["ex1"].mean(), "t": stats.ttest_1samp(nd["ex1"].dropna(), 0).statistic})
    # windows of falls: cases there
    for ws in [[20, 21, 22], [14], [1], [9]]:
        s = sig[sig["wi"].isin(ws)]
        out[f"cases_w{ws}"] = pd.Series({"n": len(s), "mean_fwd1": s["fwd1"].mean(), "pnl_sum": s["pnl"].sum(),
                                         "pnl_eq_sum": s["pnl_eq"].sum(), "mean_alloc": s["alloc"].mean(),
                                         "mean_volq": s["volq"].mean(), "mean_dropz": s["drop_z"].mean(),
                                         "worst_pnl": s["pnl"].min()})
    # worst 15 pnl cases features
    w15 = sig.nsmallest(15, "pnl")
    out["worst15_pnl_feat"] = pd.DataFrame({"worst15": w15[["fwd1", "alloc", "volq", "drop_z", "rmult", "cloc"]].mean(),
                                            "all": sig[["fwd1", "alloc", "volq", "drop_z", "rmult", "cloc"]].mean()})
    # alloc quartile
    sig["aq"] = pd.qcut(sig["alloc"], 4, labels=False, duplicates="drop")
    out["sig_by_alloc_q"] = sig.groupby("aq").apply(summ)
    # 2-day horizon
    s2 = sig.dropna(subset=["fwd2"])
    out["fwd2_mean"] = pd.Series({"mean_fwd2": s2["fwd2"].mean(), "mean_fwd1": s2["fwd1"].mean(),
                                  "day2_only": (s2["fwd2"] - s2["fwd1"]).mean(),
                                  "t_day2": stats.ttest_1samp(((1+s2["fwd2"])/(1+s2["fwd1"])-1), 0).statistic})
    # crude book proxy: pnl per day averaged over 6 coins, actual vs equal(alloc=1) vs inv-ok (alloc*vol20/median)
    def calmar(col):
        d = a[["coin", "w", "wi", "pos"]].copy()
        d["p"] = 0.0
        d.loc[sig.index, "p"] = sig[col] - 0.0019 * np.where(col == "pnl", sig["alloc"].abs(), 1.0)
        g = d.groupby(["wi", "pos"])["p"].sum() / 6
        v = (1 + g).cumprod()
        mdd = (v / v.cummax() - 1).min()
        yr = v.iloc[-1] ** (365 / len(v)) - 1
        return pd.Series({"yearly": yr, "maxdd": mdd, "calmar": yr / -mdd, "sharpe": g.mean() / g.std() * np.sqrt(365)})
    sig["pnl_hv"] = np.where(sig["volq"] >= 2, sig["fwd1"], 0.0)
    out["proxy_actual"] = calmar("pnl")
    out["proxy_equal"] = calmar("pnl_eq")
    out["proxy_highvol_only_equal"] = calmar("pnl_hv")
    return out
