import numpy as np
import pandas as pd


def measure(bars):
    def col(df, name):
        return df[name] if name in df.columns else pd.Series(np.nan, index=df.index)

    def weighted_stats(r, w):
        r = np.asarray(r, dtype=float)
        w = np.asarray(w, dtype=float)
        sw = w.sum()
        if len(r) == 0 or sw <= 0:
            return np.nan, np.nan, 0.0
        m = float(np.sum(w * r) / sw)
        var = float(np.sum(w * (r - m) ** 2) / sw)
        n_eff = float(sw ** 2 / np.sum(w ** 2))
        if n_eff > 1:
            var = var * n_eff / (n_eff - 1.0)  # unbiased-like correction
        else:
            var = np.nan
        return m, var, n_eff

    act_total = 0
    act_ok = 0
    heavy_r, heavy_w, thin_r, thin_w = [], [], [], []
    all_r = []

    for coin in bars:
        for win in bars[coin]:
            df = bars[coin][win].reset_index(drop=True)
            close = df["close"].astype(float)
            vol = df["volume"].astype(float)
            fc = df["forecast"].astype(float)

            move = col(df, "debug_info.components.heavy_up.last_history_value").astype(float)
            alt = col(df, "debug_info.components.thin_up.last_history_value").astype(float)
            move = move.where(move.notna(), alt)
            move = move.where(move.notna(), close.pct_change())

            vmean = vol.rolling(20, min_periods=20).mean()
            heavy_vol = vol >= vmean
            vol_known = vmean.notna() & vol.notna()

            # --- situation check ---
            for i in range(len(df)):
                f = fc.iloc[i]
                if pd.isna(f) or f == 0:
                    continue
                act_total += 1
                m = move.iloc[i]
                if pd.isna(m) or m <= 0:
                    continue
                if not vol_known.iloc[i]:
                    act_ok += 1  # up bar, volume class not computable inside the window
                    continue
                expected = 1.0 if heavy_vol.iloc[i] else -1.0
                if np.sign(f) == expected:
                    act_ok += 1

            # --- returns ---
            nxt = close.shift(-1) / close - 1.0
            for i in range(len(df) - 1):
                r = nxt.iloc[i]
                if pd.isna(r):
                    continue
                all_r.append(float(r))
                f = fc.iloc[i]
                m = move.iloc[i]
                if pd.isna(f) or f == 0 or pd.isna(m) or m <= 0:
                    continue
                if f > 0:
                    heavy_r.append(float(r)); heavy_w.append(abs(float(f)))
                else:
                    thin_r.append(float(r)); thin_w.append(abs(float(f)))

    reading = ("Up bar = one-bar move (heavy_up/thin_up last_history_value) > 0; heavy/thin groups are the "
               "forecast-bearing up bars with positive/negative forecast; the Welch t uses |forecast|-weighted "
               "means and variances with Kish effective sample sizes; the unconditional mean is the plain mean "
               "of all next-bar returns in all windows; the plan's 30-bar minimum per group is applied as "
               "'not observable'; in the situation check, active up bars in the first 19 rows of a window "
               "(20-bar volume mean not computable) count as on-side.")

    agreement = act_ok / act_total if act_total > 0 else 0.0
    passed = act_total > 0 and agreement >= 0.9
    counts = {"heavy forecast-bearing up bars": len(heavy_r),
              "thin forecast-bearing up bars": len(thin_r)}
    mm_name = "|forecast|-weighted mean next-bar return, heavy up bars minus thin up bars"
    thr = "confirm if difference > 0 and t >= 2; reject if difference < 0 and t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": ("Fewer than 90% of active bars are up bars with a long forecast on volume at/above "
                           "its 20-bar mean or a short forecast on volume below it (or there are no active bars)."),
            "reading": reading,
        }

    mh, vh, nh = weighted_stats(heavy_r, heavy_w)
    mt, vt, nt = weighted_stats(thin_r, thin_w)
    diff = mh - mt if not (np.isnan(mh) or np.isnan(mt)) else np.nan
    t = np.nan
    if not np.isnan(diff) and nh > 1 and nt > 1:
        se = np.sqrt(vh / nh + vt / nt)
        if se > 0:
            t = diff / se
    uncond = float(np.mean(all_r)) if all_r else np.nan
    sup_val = mt - uncond if not (np.isnan(mt) or np.isnan(uncond)) else np.nan
    sup_pass = None if np.isnan(sup_val) else bool(sup_val < 0)

    def clean(x):
        return None if x is None or (isinstance(x, float) and np.isnan(x)) else float(x)

    if len(heavy_r) < 30 or len(thin_r) < 30:
        status = "not observable"
        decided = "Fewer than 30 forecast-bearing up bars in at least one group (heavy or thin) across all windows."
    elif np.isnan(t):
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so neither confirm nor reject is met."
    elif diff > 0 and t >= 2:
        status = "confirmed"
        decided = "The heavy-minus-thin difference is positive with t >= 2."
    elif diff < 0 and t <= -2:
        status = "rejected"
        decided = "The heavy-minus-thin difference is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": mm_name, "value": clean(diff),
                         "statistic": None if np.isnan(t) else {"name": "Welch t (weighted)", "value": float(t)},
                         "threshold": thr},
        "supporting_check": {"name": "thin-up weighted mean next-bar return minus unconditional mean daily return (< 0)",
                             "value": clean(sup_val), "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
