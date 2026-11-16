import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    COMP = "range_pos"
    FLAT_COL = "debug_info.components." + COMP + ".last_history_value"

    def _raw_range_pos(df):
        # 1) flattened column
        if FLAT_COL in df.columns:
            return pd.to_numeric(df[FLAT_COL], errors="coerce").reset_index(drop=True)
        # 2) nested dict column
        if "debug_info.components" in df.columns:
            vals = []
            for v in df["debug_info.components"].tolist():
                x = np.nan
                if isinstance(v, dict):
                    c = v.get(COMP)
                    if isinstance(c, dict):
                        try:
                            x = float(c.get("last_history_value"))
                        except (TypeError, ValueError):
                            x = np.nan
                vals.append(x)
            s = pd.Series(vals, dtype=float)
            if s.notna().any():
                return s
        # 3) recompute from closes (position in the 20-bar closing range, -1 low .. +1 high)
        c = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
        lo = c.rolling(20, min_periods=20).min()
        hi = c.rolling(20, min_periods=20).max()
        rng = (hi - lo).replace(0, np.nan)
        return 2.0 * (c - lo) / rng - 1.0

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            f = pd.to_numeric(d["forecast"], errors="coerce")
            reg = d["regime"].astype(str)
            rp = _raw_range_pos(d)
            active = f.notna() & (f != 0)
            situ = (reg == "trending") & rp.notna() & (rp <= 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (f < 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed_sit = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean of (forecast/10) x excess 5-bar return on trending grid bars"
    main_thr = "t >= 2 confirms (with check < 0); t <= -2 rejects; otherwise inconclusive; needs >= 100 active grid cases and >= 30 with forecast < 0"
    check_name = "mean excess 5-bar return, forecast < -10 minus forecast == 0 (active grid bars)"

    if not passed_sit and n_active > 0:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active forecast bars": int(n_active)},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are short bars with the close above its 200-bar SMA (trending) and in the lower half of its 20-bar closing range.",
            "reading": "Situation taken as regime == trending (the recorded 200-SMA decision) and the recorded range_pos raw value <= 0 (lower half of the 20-bar range), expected side short.",
        }

    # ---------- criterion ----------
    prods, excess_all, fc_all = [], [], []
    for coin, wins in bars.items():
        # coin mean 5-bar return over all windows (non-overlapping grid, all bars)
        rets_all = []
        per_win = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce").values
            f = pd.to_numeric(d["forecast"], errors="coerce").values
            reg = d["regime"].astype(str).values
            n = len(d)
            for t in range(0, n - H, H):
                r = c[t + H] / c[t] - 1.0
                if np.isfinite(r):
                    rets_all.append(r)
                    per_win.append((r, f[t], reg[t]))
        if len(rets_all) == 0:
            continue
        mu = float(np.mean(rets_all))
        for r, fv, rg in per_win:
            if rg != "trending" or not np.isfinite(fv):
                continue
            ex = r - mu
            prods.append((fv / 10.0) * ex)
            excess_all.append(ex)
            fc_all.append(fv)

    prods = np.array(prods, dtype=float)
    excess_all = np.array(excess_all, dtype=float)
    fc_all = np.array(fc_all, dtype=float)
    n_cases = int(len(prods))
    n_neg = int((fc_all < 0).sum()) if n_cases else 0

    mean_val, t_val = None, None
    if n_cases >= 2:
        sd = float(np.std(prods, ddof=1))
        mean_val = float(np.mean(prods))
        t_val = float(mean_val / (sd / np.sqrt(n_cases))) if sd > 0 else None
    elif n_cases == 1:
        mean_val = float(prods[0])

    low = excess_all[fc_all < -10] if n_cases else np.array([])
    zero = excess_all[fc_all == 0] if n_cases else np.array([])
    diff = float(low.mean() - zero.mean()) if (len(low) > 0 and len(zero) > 0) else None
    check_pass = (diff < 0) if diff is not None else None

    counts = {
        "active grid cases": n_cases,
        "active grid cases with forecast below 0": n_neg,
        "grid cases with forecast below -10": int(len(low)),
        "grid cases with forecast 0": int(len(zero)),
    }

    if n_cases < 100 or n_neg < 30:
        status = "not observable"
        decided = ("Minimum not reached: %d active grid cases (need 100) and %d with forecast below 0 (need 30)."
                   % (n_cases, n_neg))
    elif t_val is None:
        status = "inconclusive"
        decided = "The main-measure t could not be computed (zero dispersion), so neither confirm nor reject is met."
    elif t_val >= 2 and check_pass is True:
        status = "confirmed"
        decided = "Main-measure t is 2 or more and the supporting check's difference is below 0."
    elif t_val <= -2:
        status = "rejected"
        decided = "Main-measure t is -2 or less: near the range low in an up-trend, the coin rises more than usual."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "Main-measure t is 2 or more but the supporting check fails (difference not below 0 or not computable)."
    else:
        status = "inconclusive"
        decided = "Main-measure t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None),
                            "passed": passed_sit},
        "main_measure": {"name": main_name,
                         "value": mean_val,
                         "statistic": ({"name": "ordinary t of the mean", "value": t_val} if t_val is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": check_name, "value": diff, "passed": check_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Active grid cases are taken as grid bars with regime == trending (the forecast is active only in that regime, "
                    "so forecast-0 trending bars are the check's comparison group), the coin's mean 5-bar return is the mean of its "
                    "non-overlapping grid returns over all windows and regimes, the situation is the range_pos raw value <= 0 in the "
                    "trending regime on the short side, and a minimum-count shortfall is reported as not observable."),
    }
