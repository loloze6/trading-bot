import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    MIN_CASES = 100
    RAW = "debug_info.components.weekend_rise.last_history_value"

    def raw_component(df):
        # VolatilityScaledReturnComponent(period 1, vol_period 20), recomputed from prices
        c = df["close"].astype(float)
        r = c / c.shift(1) - 1.0
        sd = r.rolling(20, min_periods=20).std()
        return r / sd

    n_active = 0
    n_agree = 0
    case_rows = []  # (coin, |forecast|, shortfall)

    for coin, wins in bars.items():
        # coin's mean 3-day return over all its windows (non-overlapping grid 0, 3, 6, ... per window)
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).to_numpy()
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        coin_drift = float(np.mean(grid_rets)) if len(grid_rets) else np.nan

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            is_sunday = (ts.dt.dayofweek == 6).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
            recomputed = raw_component(df)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed).to_numpy()
            else:
                raw = recomputed.to_numpy()

            active = fc != 0
            agree = active & is_sunday & (np.nan_to_num(raw, nan=0.0) > 0) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

            c = df["close"].astype(float).to_numpy()
            for i in np.where(is_sunday & (fc < 0))[0]:
                if i + H >= len(c):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H])) or c[i] == 0:
                    continue
                if not np.isfinite(coin_drift):
                    continue
                r3 = c[i + H] / c[i] - 1.0
                shortfall = coin_drift - r3  # short's direction: drift minus 3-day return
                case_rows.append((coin, abs(fc[i]), shortfall))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    reading = ("A Sunday bar is a bar whose UTC start timestamp is a Sunday (its close is the Sunday close, the next bar "
               "Monday), the raw rise uses last_history_value (recomputed from prices where missing), cases are Sunday "
               "bars with forecast < 0 and 3 bars left in the window, the coin's drift is the mean of its non-overlapping "
               "3-bar returns pooled over all its windows, and the t of the |forecast|-weighted mean uses the weighted "
               "standard error sqrt(n/(n-1) * sum(w^2 (x-m)^2)) / sum(w).")

    main_name = "|forecast|-weighted mean 3-day shortfall vs coin drift (short direction), before costs"
    threshold = "confirm: mean > 0 with t >= 2 and correlation > 0; reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are Sunday-close bars after a weekend "
                           "rise with a short forecast, as the plan's situation requires."),
            "reading": reading,
        }

    n = len(case_rows)
    w = np.array([r[1] for r in case_rows], dtype=float)
    x = np.array([r[2] for r in case_rows], dtype=float)

    mean_w = None
    t_val = None
    corr = None
    if n >= 2 and w.sum() > 0:
        mean_w = float(np.sum(w * x) / np.sum(w))
        se = np.sqrt(n / (n - 1.0) * np.sum((w ** 2) * (x - mean_w) ** 2)) / np.sum(w)
        t_val = float(mean_w / se) if se > 0 else None
        if np.std(w) > 0 and np.std(x) > 0:
            corr = float(stats.pearsonr(w, x)[0])

    counts = {"cases (Sunday rises)": int(n)}
    supp_passed = None if corr is None else bool(corr > 0)
    supporting = {"name": "Pearson correlation of |forecast| with shortfall", "value": corr, "passed": supp_passed}
    statistic = {"name": "t of the weighted mean", "value": t_val} if t_val is not None else None

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases (Sunday rises), below the plan's minimum of {MIN_CASES}."
    elif mean_w is None or t_val is None:
        status = "inconclusive"
        decided = "The weighted mean or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_w > 0 and t_val >= 2 and corr is not None and corr > 0:
        status = "confirmed"
        decided = "The weighted mean shortfall is above 0 with t >= 2 and the correlation is above 0 (confirm rule)."
    elif mean_w < 0 and t_val <= -2:
        status = "rejected"
        decided = "The weighted mean shortfall is below 0 with t <= -2 (reject rule): weekend rises outrun their drift."
    else:
        status = "inconclusive"
        if t_val >= 2 and mean_w > 0:
            decided = "t >= 2 but the correlation is 0 or below (or undefined), so the plan's inconclusive rule applies."
        else:
            decided = "|t| < 2, so neither confirm nor reject holds (the plan's inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean_w, "statistic": statistic, "threshold": threshold},
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
