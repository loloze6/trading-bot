def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; H = 20
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            lr = np.log(cl[1:] / cl[:-1])
            for i in range(0, len(b) - H, H):
                r = cl[i + H] / cl[i] - 1
                r20 = cl[i] / cl[i - 20] - 1 if i >= 20 else np.nan
                r5 = cl[i] / cl[i - 5] - 1 if i >= 5 else np.nan
                vol = lr[max(0, i - 20):i].std() if i >= 10 else np.nan
                rows.append((c, w, int(w[1:]), b["forecast"].iloc[i], r, r20, r5, vol,
                             b["postRebalance_current_allocation"].iloc[i]))
    G = pd.DataFrame(rows, columns=["coin", "win", "wnum", "fc", "r", "r20", "r5", "vol", "pos"])
    G["drift"] = G.groupby("coin")["r"].transform("mean")
    G["u"] = G["r"] - G["drift"]
    G["dir_u"] = np.sign(G["fc"]) * G["u"]
    G["dir_r"] = np.sign(G["fc"]) * G["r"]
    def agg(x):
        return pd.Series({"n": len(x), "raw_r": x["r"].mean(), "unusual": x["u"].mean(),
                          "dir_unusual": x["dir_u"].mean(), "dir_total": x["dir_r"].mean(),
                          "t_dir_u": stats.ttest_1samp(x["dir_u"], 0).statistic if len(x) > 2 else np.nan})
    G["fq"] = pd.qcut(G["fc"], 6, labels=False, duplicates="drop")
    out["by_forecast_sextile"] = G.groupby("fq").apply(agg).join(G.groupby("fq")["fc"].mean().rename("fc"))
    G["side"] = np.where(G["fc"] > 0, "long", np.where(G["fc"] < 0, "short", "flat"))
    G["align20"] = np.sign(G["r20"]) == np.sign(G["fc"])
    out["by_side_align20"] = G.dropna(subset=["r20"]).groupby(["side", "align20"]).apply(agg)
    G["vq"] = G.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["by_side_vol"] = G.groupby(["side", "vq"]).apply(agg)
    G["era"] = np.where(G["wnum"].between(15, 21), "w15-21", "other")
    out["by_side_era"] = G.groupby(["side", "era"]).apply(agg)
    # graded within longs/shorts: corr of |fc| with dir_u
    for s in ["long", "short"]:
        x = G[G.side == s]
        rho, p = stats.spearmanr(x["fc"].abs(), x["dir_u"])
        out[f"spearman_absfc_dirU_{s}"] = pd.Series({"n": len(x), "rho": rho, "p": p})
    # within longs: graded on r20 size
    x = G[(G.side == "long")].dropna(subset=["r20"]).copy()
    x["r20q"] = pd.qcut(x["r20"], 4, labels=False)
    out["long_by_r20_quart"] = x.groupby("r20q").apply(agg).join(x.groupby("r20q")["r20"].mean().rename("r20m"))
    x = G[(G.side == "short")].dropna(subset=["r20"]).copy()
    x["r20q"] = pd.qcut(x["r20"], 4, labels=False)
    out["short_by_r20_quart"] = x.groupby("r20q").apply(agg).join(x.groupby("r20q")["r20"].mean().rename("r20m"))
    return out
