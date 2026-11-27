def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    drift = {}
    for c in bars:
        allr = []
        for w, b in bars[c].items():
            r = b["close"].pct_change().dropna()
            allr.append(r)
        drift[c] = pd.concat(allr).mean() if allr else 0.0
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"]
            rng = (b["high"] - b["low"])
            out = pd.DataFrame({
                "coin": c, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "ret1": cl.pct_change(),
                "ret5": cl.pct_change(5),
                "trend60": cl.pct_change(60),
                "wide": rng / rng.rolling(20).mean(),
                "loc": (cl - b["low"]) / rng.replace(0, np.nan),
                "nxt": cl.shift(-1) / cl - 1,
                "nxt2": cl.shift(-2) / cl - 1,
                "regime": b["regime"],
                "alloc": b["postRebalance_current_allocation"],
            })
            out["dr"] = drift[c]
            rows.append(out)
    d = pd.concat(rows, ignore_index=True)
    d["short1"] = -(d["nxt"] - d["dr"])
    d["short2"] = -(d["nxt2"] - 2 * d["dr"])

    def meas(mask, col="short1"):
        s = d.loc[mask & d[col].notna()]
        if len(s) < 3:
            return pd.Series({"n": len(s)})
        g = s.groupby("day")[col].sum()
        nd = len(g)
        m = s[col].mean()
        se = np.sqrt((g - g.mean() * 0 - m * s.groupby("day").size()).pow(2).sum()) / len(s)
        return pd.Series({"n": len(s), "days": nd, "mean%": 100 * m, "t": m / se if se > 0 else np.nan,
                          "hit": (s[col] > 0).mean()})

    up = d["ret1"] > 0
    fall = d["trend60"] < -0.10
    rise = d["trend60"] > 0.10
    chop = (~fall) & (~rise) & d["trend60"].notna()
    neg5 = d["ret5"] < 0
    variants = {
        "recorded_regime": d["regime"] == "mean_reversion",
        "base_recomp": fall & up & neg5 & (d["wide"] >= 1.5) & (d["loc"] >= 0.75),
        "wide1.2": fall & up & neg5 & (d["wide"] >= 1.2) & (d["loc"] >= 0.75),
        "wide1.0": fall & up & neg5 & (d["wide"] >= 1.0) & (d["loc"] >= 0.75),
        "loc0.5": fall & up & neg5 & (d["wide"] >= 1.5) & (d["loc"] >= 0.5),
        "nolocc": fall & up & neg5 & (d["wide"] >= 1.5),
        "no5": fall & up & (d["wide"] >= 1.5) & (d["loc"] >= 0.75),
        "w1.2_loc0.5": fall & up & neg5 & (d["wide"] >= 1.2) & (d["loc"] >= 0.5),
        "w1.2_nolocc": fall & up & neg5 & (d["wide"] >= 1.2),
        "fall_up_neg5_any": fall & up & neg5,
        "fall_up_any": fall & up,
        "fall_all": fall,
        "rise_up_neg5_w1.5_loc": rise & up & neg5 & (d["wide"] >= 1.5) & (d["loc"] >= 0.75),
        "chop_up_neg5_w1.5_loc": chop & up & neg5 & (d["wide"] >= 1.5) & (d["loc"] >= 0.75),
        "fall_up_neg5_w<1.2": fall & up & neg5 & (d["wide"] < 1.2),
    }
    v1 = pd.DataFrame({k: meas(m) for k, m in variants.items()}).T
    v2 = pd.DataFrame({k: meas(m, "short2") for k, m in variants.items()}).T
    # grading inside broad set by ret5 depth and width
    bm = variants["w1.2_nolocc"] & d["short1"].notna()
    s = d.loc[bm].copy()
    s["q5"] = pd.qcut(s["ret5"], 3, labels=["deep", "mid", "shallow"])
    s["qw"] = pd.qcut(s["wide"], 3, labels=["lowW", "midW", "highW"])
    g5 = s.groupby("q5")["short1"].agg(["count", "mean"])
    gw = s.groupby("qw")["short1"].agg(["count", "mean"])
    sp5 = stats.spearmanr(-s["ret5"], s["short1"])
    spw = stats.spearmanr(s["wide"], s["short1"])
    # per window for broad set
    pw = d.loc[bm].groupby("win")["short1"].agg(["count", "mean"])
    # book drawdown
    bk = []
    for c in days:
        for w, t in days[c].items():
            bk.append(t.assign(coin=c, win=w))
    bk = pd.concat(bk)
    bd = bk.groupby(["win", "day"])["book_return"].mean().dropna()
    bd = bd.sort_index(level=[0, 1])
    v = (1 + bd).cumprod()
    dd = v / v.cummax() - 1
    worst = bd.nsmallest(8)
    book = pd.Series({"days": len(bd), "maxDD%": 100 * dd.min(), "total%": 100 * (v.iloc[-1] - 1),
                      "worst8_sum%": 100 * worst.sum(), "posdays": (bd != 0).sum()})
    return {"next1_short": v1, "next2_short": v2, "grade_ret5_broad": g5, "grade_wide_broad": gw,
            "spearman_depth_broad": f"{sp5.correlation:.3f} p{sp5.pvalue:.3f}",
            "spearman_wide_broad": f"{spw.correlation:.3f} p{spw.pvalue:.3f}",
            "broad_by_window": pw, "book": book,
            "worst_book_days%": (100 * worst).reset_index(drop=True)}
