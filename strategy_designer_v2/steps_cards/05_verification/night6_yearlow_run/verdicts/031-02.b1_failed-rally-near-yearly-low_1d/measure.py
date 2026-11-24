import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    RET_LB = 60
    COL_RAW_DIST = "debug_info.components.dist_low.last_history_value"
    COL_POST_DIST = "debug_info.components.dist_low.post_pipeline_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)

            # 60-bar return from the window's own closes where available;
            # otherwise the detector's recorded decision (its component is not recorded).
            ret60 = np.full(n, np.nan)
            if n > RET_LB:
                ret60[RET_LB:] = close[RET_LB:] / close[:-RET_LB] - 1.0
            regime = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * n)
            in_regime = np.where(np.isnan(ret60), regime == "trending", ret60 > 0)

            if COL_POST_DIST in df.columns:
                post = pd.to_numeric(df[COL_POST_DIST], errors="coerce").to_numpy(dtype=float)
            else:
                post = np.full(n, np.nan)
            if COL_RAW_DIST in df.columns:
                raw = pd.to_numeric(df[COL_RAW_DIST], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(n, np.nan)

            # Expected side: short when the distance above the yearly low is smaller than
            # its usual size (standardised value below 10), long when larger.
            exp_side = np.sign(post - 10.0)
            raw_ok = raw >= 0  # a distance above the low is never negative

            active = np.isfinite(fc) & (fc != 0)
            agree = (active & in_regime & np.isfinite(post) & raw_ok
                     & (np.sign(fc) == exp_side))
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "Pearson correlation of forecast with 20-bar forward excess return (non-overlapping grid, nonzero forecast)"
    threshold = "confirm: t >= 2 with supporting check passing; reject: t <= -2"
    sup_name = "mean 20-bar excess return on grid bars with forecast <= -2 is below 0"
    reading = ("Cases are pooled over all coins and windows on the 0,20,40,... grid of each window; the coin's mean "
               "20-bar return is the mean over that grid on all its bars in all windows; correlation t is "
               "r*sqrt((n-2)/(1-r^2)); the 60-day return for the situation check is recomputed from closes where the "
               "window has 60 prior bars, else read from the recorded regime; the expected side is the sign of the "
               "dist_low standardised value minus 10; the plan's minimum counts, when unmet, give 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of nonzero-forecast bars are bars with a positive 60-day return whose "
                           "forecast is short when the close is nearer its 365-day low than usual and long when farther."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for i in range(0, n, H):
                if i + H < n:
                    fwd = close[i + H] / close[i] - 1.0
                else:
                    fwd = np.nan
                coin_rows.append((coin, fc[i], fwd))
        if not coin_rows:
            continue
        cdf = pd.DataFrame(coin_rows, columns=["coin", "forecast", "fwd"])
        coin_mean = cdf["fwd"].dropna().mean()
        cdf["excess"] = cdf["fwd"] - coin_mean
        rows.append(cdf)

    if rows:
        g = pd.concat(rows, ignore_index=True)
    else:
        g = pd.DataFrame(columns=["coin", "forecast", "fwd", "excess"])
    g = g.dropna(subset=["forecast", "excess"])
    s = g[g["forecast"] != 0]
    neg = s[s["forecast"] <= -2]
    n_cases = int(len(s))
    n_neg = int(len(neg))

    r = None
    t = None
    if n_cases >= 3:
        x = s["forecast"].to_numpy(dtype=float)
        y = s["excess"].to_numpy(dtype=float)
        if np.std(x) > 0 and np.std(y) > 0:
            r = float(np.corrcoef(x, y)[0, 1])
            if abs(r) < 1:
                t = float(r * np.sqrt((n_cases - 2) / (1 - r * r)))
            else:
                t = float(np.sign(r) * np.inf)

    sup_val = float(neg["excess"].mean()) if n_neg > 0 else None
    sup_pass = (sup_val < 0) if sup_val is not None else None

    counts = {"grid cases with a nonzero forecast": n_cases,
              "grid cases with forecast at or below -2": n_neg}

    if n_cases < 50 or n_neg < 20:
        status = "not observable"
        missing = []
        if n_cases < 50:
            missing.append(f"{n_cases} grid cases with a nonzero forecast (minimum 50)")
        if n_neg < 20:
            missing.append(f"{n_neg} grid cases at or below -2 (minimum 20)")
        decided = "Minimum count not reached: " + " and ".join(missing) + "."
    elif t is None:
        status = "inconclusive"
        decided = "The correlation could not be computed (no variation), so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The correlation's t is 2 or more and the supporting check passes (confirm rule)."
    elif t <= -2:
        status = "rejected"
        decided = "The correlation's t is -2 or less (reject rule)."
    elif t >= 2:
        status = "inconclusive"
        decided = "The correlation's t is 2 or more but the supporting check fails (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The correlation's t is between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": r,
                         "statistic": ({"name": "correlation t (n=%d)" % n_cases, "value": t}
                                       if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": sup_val,
                             "passed": (bool(sup_pass) if sup_pass is not None else None)},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
