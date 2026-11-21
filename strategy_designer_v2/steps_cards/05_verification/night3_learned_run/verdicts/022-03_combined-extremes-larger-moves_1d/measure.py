import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    P = "debug_info.components."
    comb_raw = P + "combined.last_history_value"
    comb_post = P + "combined.post_pipeline_value"
    singles = ["s_momentum", "s_reversal", "s_high", "s_volatility"]

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[comb_raw], errors="coerce") if comb_raw in df.columns else pd.Series(np.nan, index=df.index)
            post = pd.to_numeric(df[comb_post], errors="coerce") if comb_post in df.columns else pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            # situation: the combined score is out (graded, non-zero after its transforms),
            # side: the score's own direction (sign of the raw combined value)
            situ = raw.notna() & (raw != 0) & post.notna() & (post != 0)
            agree = active & situ & (np.sign(f) == np.sign(raw))
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean signed unusual 5-bar move, combined top-10% minus best single top-10%"
    thr = "Welch t >= 2 (with combined beating every single and slope t >= 2) confirms; Welch t <= -2 or slope t <= -2 rejects"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars where the combined score is out "
                           "and the forecast takes the score's sign (agreement %.3f)." % agreement),
            "reading": "Situation taken as a non-zero combined post_pipeline_value, side as the sign of the combined last_history_value.",
        }

    # ---------- 2. grid cells ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            n = len(d)
            cols = {}
            for name in ["combined"] + singles:
                c = P + name + ".last_history_value"
                cols[name] = pd.to_numeric(d[c], errors="coerce").to_numpy(dtype=float) if c in d.columns else np.full(n, np.nan)
            cpost = pd.to_numeric(d[comb_post], errors="coerce").to_numpy(dtype=float) if comb_post in d.columns else np.full(n, np.nan)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = {"coin": coin, "window": w, "ret": c1 / c0 - 1.0, "combined_post": cpost[t]}
                for name in cols:
                    r[name] = cols[name][t]
                rows.append(r)
    g = pd.DataFrame(rows)
    if g.empty:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": passed},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"combined top-10% cells": 0},
            "decided_by": "No 5-bar grid cell could be measured, so no top-10% group reaches 30 cases.",
            "reading": "none",
        }
    g["drift"] = g.groupby("coin")["ret"].transform("mean")
    g["unusual"] = g["ret"] - g["drift"]

    groups = {}
    counts = {}
    for name in ["combined"] + singles:
        sub = g[g[name].notna() & np.isfinite(g[name])]
        if len(sub) == 0:
            groups[name] = np.array([])
            counts[name + " top-10% cells"] = 0
            continue
        a = sub[name].abs()
        q = a.quantile(0.9)
        top = sub[a >= q]
        top = top[top[name] != 0]
        vals = (top["unusual"] * np.sign(top[name])).to_numpy(dtype=float)
        groups[name] = vals
        counts[name + " top-10% cells"] = int(len(vals))

    # supporting check data
    cc = g[g["combined"].notna() & g["combined_post"].notna() & (g["combined"] != 0)]
    y = (cc["unusual"] * np.sign(cc["combined"])).to_numpy(dtype=float)
    x = cc["combined_post"].abs().to_numpy(dtype=float)
    counts["combined cells in regression"] = int(len(y))

    means = {k: (float(np.mean(v)) if len(v) else None) for k, v in groups.items()}
    reading = ("Cells are rows 0,5,10,... of each window with a 5-bar return inside it; each group's top 10% is abs(last_history_value) "
               "at or above its pooled 90th percentile over measured cells, signed by that same component's raw value; the best single "
               "is the one with the highest mean signed unusual move; and since the minimum-count rule is stated, a group under 30 "
               "cases gives 'not observable'.")

    short = [k for k in groups if len(groups[k]) < 30]
    if short:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": passed},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "Top-10% group(s) %s have fewer than 30 non-overlapping cases." % ", ".join(short),
            "reading": reading,
        }

    best = max(singles, key=lambda k: means[k])
    diff = means["combined"] - means[best]
    t_w = float(stats.ttest_ind(groups["combined"], groups[best], equal_var=False).statistic)
    beats_all = all(means["combined"] > means[k] for k in singles)

    slope_t = None
    slope = None
    if len(y) >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        slope_t = float(lr.slope / lr.stderr) if lr.stderr > 0 else None
    check_pass = bool(slope_t is not None and slope_t >= 2)

    if (np.isfinite(t_w) and t_w <= -2) or (slope_t is not None and slope_t <= -2):
        status = "rejected"
        decided = ("Reject rule: Welch t of combined minus best single (%s) is %.2f and slope t is %s; one is <= -2."
                   % (best, t_w, "nan" if slope_t is None else "%.2f" % slope_t))
    elif np.isfinite(t_w) and t_w >= 2 and beats_all and check_pass:
        status = "confirmed"
        decided = ("Confirm rule: combined minus best single (%s) Welch t %.2f >= 2, combined beats every single, slope t %.2f >= 2."
                   % (best, t_w, slope_t))
    else:
        status = "inconclusive"
        decided = ("Neither rule met: Welch t %.2f vs best single %s, combined beats all singles: %s, slope t %s."
                   % (t_w, best, beats_all, "nan" if slope_t is None else "%.2f" % slope_t))

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {"name": main_name, "value": float(diff),
                         "statistic": {"name": "Welch t", "value": float(t_w)},
                         "threshold": thr,
                         "group_means": {k: float(v) for k, v in means.items()},
                         "best_single": best},
        "supporting_check": {"name": "slope t of signed unusual move on abs(combined post_pipeline_value)",
                             "value": slope_t, "passed": check_pass if slope_t is not None else None},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
