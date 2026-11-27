def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    drift = {}
    for c in bars:
        drift[c] = pd.concat([b["close"].pct_change().dropna() for b in bars[c].values()]).mean()
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; rng = b["high"] - b["low"]
            lr = cl.pct_change()
            out = pd.DataFrame({
                "coin": c, "win": w, "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "ret1": lr, "ret5": cl.pct_change(5), "trend60": cl.pct_change(60),
                "wide": rng / rng.rolling(20).mean(),
                "loc": (cl - b["low"]) / rng.replace(0, np.nan),
                "nxt": cl.shift(-1) / cl - 1, "nxt2": cl.shift(-2) / cl - 1,
                "nxt3": cl.shift(-3) / cl - 1,
                "vol20": lr.rolling(20).std(),
                "alloc": b["postRebalance_current_allocation"],
            })
            out["dr"] = drift[c]
            rows.append(out)
    d = pd.concat(rows, ignore_index=True)
    for h, col in [(1, "nxt"), (2, "nxt2"), (3, "nxt3")]:
        d[f"s{h}"] = -(d[col] - h * d["dr"])
    def meas(mask, col="s1"):
        s = d.loc[mask & d[col].notna()]
        if len(s) < 3:
            return pd.Series({"n": len(s)})
        m = s[col].mean()
        g = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((g ** 2).sum()) / len(s)
        return pd.Series({"n": len(s), "days": s["day"].nunique(), "mean%": 100 * m,
                          "t": m / se, "hit": (s[col] > 0).mean()})
    fall = d["trend60"] < -0.10
    up = d["ret1"] > 0; dn = d["ret1"] <= 0; neg5 = d["ret5"] < 0
    broad = fall & up & neg5
    cond = {
        "fall_up_neg5": broad,
        "fall_down_neg5 (no up-day signal)": fall & dn & neg5,
        "fall_up_pos5": fall & up & ~neg5,
        "notfall_up_neg5": (~fall) & d["trend60"].notna() & up & neg5,
        "rise_up_neg5": (d["trend60"] > 0.10) & up & neg5,
    }
    t1 = pd.DataFrame({k: meas(m) for k, m in cond.items()}).T
    t2 = pd.DataFrame({k: meas(m, "s2") for k, m in cond.items()}).T
    # non-overlapping 2-day grid on broad set
    grid2 = broad & (d["pos"] % 2 == 0)
    t_grid2 = meas(grid2, "s2")
    # grading in broad set: depth of ret5 scaled by vol, and width
    s = d.loc[broad & d["s1"].notna()].copy()
    s["depthz"] = -s["ret5"] / (s["vol20"] * np.sqrt(5))
    s["q"] = pd.qcut(s["depthz"], 4, labels=["q1shallow", "q2", "q3", "q4deep"])
    gq = s.groupby("q").agg(n=("s1", "size"), m1=("s1", "mean"), m2=("s2", "mean"))
    s["qw"] = pd.qcut(s["wide"], 4, labels=["w1low", "w2", "w3", "w4wide"])
    gw = s.groupby("qw").agg(n=("s1", "size"), m1=("s1", "mean"), m2=("s2", "mean"))
    sp = stats.spearmanr(s["depthz"], s["s1"]).correlation
    sp2 = stats.spearmanr(s["depthz"], s["s2"].fillna(0)).correlation
    byw = s.groupby("win").agg(n=("s1", "size"), m1=("s1", "mean"), m2=("s2", "mean"))
    # rough book of broad version: short 1 day, size by depthz capped, vol-scaled
    d["sig"] = np.where(broad, np.clip(d["ret5"].abs() / (d["vol20"] * np.sqrt(5)), 0, 2), 0.0)
    d["w_"] = d["sig"] * (0.02 / d["vol20"]).clip(upper=2)
    d["pnl"] = -d["w_"] * d["nxt"] - d["w_"] * 0.0022 * (d["sig"] > 0)
    dd = d.dropna(subset=["nxt"]).groupby(["win", "day"])["pnl"].mean().sort_index()
    v = (1 + dd).cumprod(); mdd = (v / v.cummax() - 1).min()
    yrs = len(dd) / 365
    yr = v.iloc[-1] ** (1 / yrs) - 1
    rough = pd.Series({"trades/coinday": (d["sig"] > 0).mean(), "yearly%": 100 * yr,
                       "maxDD%": 100 * mdd, "calmar": yr / -mdd,
                       "sharpe": dd.mean() / dd.std() * np.sqrt(365)})
    # recorded book: trades per day share vs broad
    held = (d["alloc"].abs() > 1e-9).mean()
    return {"cond_s1": t1, "cond_s2": t2, "broad_grid2_s2": t_grid2, "grade_depth_vol": gq,
            "grade_width": gw, "spearman_depth_s1_s2": f"{sp:.3f} {sp2:.3f}",
            "broad_by_window": byw, "rough_broad_book": rough, "recorded_held_share": held}
