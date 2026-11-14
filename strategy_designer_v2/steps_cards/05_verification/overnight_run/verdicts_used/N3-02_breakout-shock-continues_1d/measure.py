import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    LOOKBACK = 20
    STD_WIN = 60
    STD_MINP = 20
    FC_COL = "forecast"
    RAW_COL = "debug_info.components.shock.last_history_value"

    def fwd_ret(close, h):
        return close.shift(-h) / close - 1.0

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df[FC_COL], errors="coerce")
            prior_max = close.shift(1).rolling(LOOKBACK, min_periods=LOOKBACK).max()
            new_high_px = close >= prior_max * (1 - 1e-12)
            computable = prior_max.notna() & close.notna()
            regime_trend = df["regime"].astype(str).str.lower() == "trending" if "regime" in df else pd.Series(False, index=df.index)
            new_high = pd.Series(np.where(computable, new_high_px, regime_trend), index=df.index).astype(bool)
            r1 = close / close.shift(1) - 1.0
            if RAW_COL in df.columns:
                raw = pd.to_numeric(df[RAW_COL], errors="coerce")
                r1 = r1.where(r1.notna(), raw)
            up = r1 > 0
            situation = new_high & up
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean excess 5-bar forward return after shock-up new highs",
                             "value": None, "statistic": None,
                             "threshold": "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"non-overlapping cases pooled across coins": 0},
            "decided_by": "No bar has a non-zero forecast, so no case could be observed.",
            "reading": "none",
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean excess 5-bar forward return after shock-up new highs",
                             "value": None, "statistic": None,
                             "threshold": "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {},
            "decided_by": ("Fewer than 90% of non-zero-forecast bars are long bars on an up day closing at the "
                           "highest close of the current and prior 20 bars, as the Fidelity situation requires."),
            "reading": "Situation recomputed from closes where 20 prior bars exist in the window, else from the regime label.",
        }

    # ---------- 2. criterion ----------
    case_excess = []
    inside_excess = []
    for coin, wins in bars.items():
        # coin mean 5-bar return over all windows pooled (every bar with a forward return)
        all_f = []
        prepared = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            f5 = fwd_ret(close, H)
            all_f.append(f5.dropna().values)
            prepared.append((df, close, f5))
        allv = np.concatenate(all_f) if all_f else np.array([])
        if len(allv) == 0:
            continue
        coin_mean = float(np.mean(allv))

        for df, close, f5 in prepared:
            fc = pd.to_numeric(df[FC_COL], errors="coerce")
            # main cases: forecast >= 10, merged if within 5 bars of an earlier kept case
            sig_idx = np.where((fc >= 10).values)[0]
            last = None
            for i in sig_idx:
                if last is not None and i - last <= H:
                    continue
                last = i
                v = f5.iloc[i]
                if pd.notna(v):
                    case_excess.append(float(v) - coin_mean)
            # inside-range shock-up days: standardised 1-day return >= 10 while forecast == 0
            r1 = close / close.shift(1) - 1.0
            meanabs = r1.abs().rolling(STD_WIN, min_periods=STD_MINP).mean()
            z = 10.0 * r1 / meanabs.replace(0, np.nan)
            mask = (z >= 10) & (fc == 0) & f5.notna()
            inside_excess.extend((f5[mask] - coin_mean).astype(float).tolist())

    n_cases = len(case_excess)
    n_inside = len(inside_excess)
    counts = {"non-overlapping cases pooled across coins": n_cases,
              "inside-range shock-up days": n_inside}

    mean_c = float(np.mean(case_excess)) if n_cases > 0 else None
    t_c = None
    if n_cases >= 2:
        sd = float(np.std(case_excess, ddof=1))
        t_c = float(mean_c / (sd / np.sqrt(n_cases))) if sd > 0 else None

    diff = None
    if n_cases > 0 and n_inside > 0:
        diff = float(mean_c - np.mean(inside_excess))
    sup_passed = None if diff is None else bool(diff > 0)

    reading = ("Coin mean is the mean of all overlapping 5-bar forward returns of the coin pooled over its windows; "
               "a signal at most 5 bars after the last kept case is merged into it; the standardised return is "
               "10 x r / mean |r| of the last 60 one-day returns (min 20, current bar included, recomputed within "
               "each window); inside-range days are not merged; t is the ordinary t of the mean.")

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping cases pooled across coins, fewer than the 30 the plan requires."
    elif t_c is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (zero dispersion), so neither rule is met."
    elif mean_c > 0 and t_c >= 2 and sup_passed is True:
        status = "confirmed"
        decided = "Mean excess 5-bar return is positive with t >= 2 and exceeds that after inside-range shock-up days."
    elif mean_c < 0 and t_c <= -2:
        status = "rejected"
        decided = "Mean excess 5-bar return is negative with t <= -2: prices reverse after shock-up new highs."
    else:
        status = "inconclusive"
        if t_c >= 2 and mean_c > 0:
            decided = "t >= 2 but the supporting difference is not positive (or not computable), so the confirm rule is not met."
        else:
            decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": "mean excess 5-bar forward return after shock-up new highs (forecast >= 10)",
                         "value": mean_c,
                         "statistic": None if t_c is None else {"name": "t of the mean", "value": t_c},
                         "threshold": "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject"},
        "supporting_check": {"name": "mean excess after new-high cases minus after inside-range shock-up days",
                             "value": diff, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
