import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    RISE_COL = "debug_info.components.rise.last_history_value"

    def _rise_from_prices(close):
        r = close.pct_change()
        sd = r.rolling(20, min_periods=20).std(ddof=1).shift(1)
        return r / sd

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            if RISE_COL in df.columns:
                rise = pd.to_numeric(df[RISE_COL], errors="coerce")
            else:
                rise = pd.Series(np.nan, index=df.index)
            rise = rise.where(rise.notna(), _rise_from_prices(close))
            # falling: 60-bar price evolution (percent) below -10, where computable in the window
            evo = (close / close.shift(60) - 1.0) * 100.0
            falling = (evo < -10).where(evo.notna(), True)
            # calm part of the profile (365-bar vol percentile) is not recomputable from the record: the detector's regime stands for it
            in_profile = df["regime"].astype(str) == "mean_reversion"
            situation = (rise >= 2.0) & falling.astype(bool) & in_profile
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    main_name = "mean short-direction 3-bar excess return on case bars"
    thr = "mean > 0 with t >= 2 on at least 30 cases (confirm); mean < 0 with t <= -2 on at least 30 cases (reject)"
    reading = ("Situation = rise in swings >= 2 (recorded raw value, else from prices) and 60-bar price change below -10 % "
               "where the window holds 60 bars, with the detector's regime mean_reversion standing for the calm profile "
               "(365-bar vol percentile not recomputable); a case is the first bar of each 3-bar grid cell (positions 0,3,6,... "
               "per window) with regime mean_reversion and forecast < 0 whose close[t+3] lies in the same window; the normal "
               "drift is the mean of the coin's non-overlapping 3-bar grid returns over all its windows; the day-pooled t "
               "sums the cases' deviations per UTC day (standard error sqrt(sum of squared day sums)/n).")
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": ("Fewer than 90 % of the active bars are short bars of the plan's situation (a large scaled rise "
                           "in a falling calm market): the forecast is active elsewhere or on the long side."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    vals, absf, days = [], [], []
    for coin, wins in bars.items():
        # normal drift over all windows of the coin
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).to_numpy()
            for i in range(0, len(c) - H, H):
                grid_rets.append(c[i + H] / c[i] - 1.0)
        grid_rets = [g for g in grid_rets if np.isfinite(g)]
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            reg = df["regime"].astype(str).to_numpy()
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for start in range(0, n, H):
                for t in range(start, min(start + H, n)):
                    if reg[t] == "mean_reversion" and np.isfinite(fc[t]) and fc[t] < 0:
                        if t + H < n and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0:
                            r = c[t + H] / c[t] - 1.0
                            vals.append(-(r - drift))
                            absf.append(abs(float(fc[t])))
                            days.append(ts.iloc[t].strftime("%Y-%m-%d"))
                        break

    vals = np.array(vals, dtype=float)
    absf = np.array(absf, dtype=float)
    n_cases = int(len(vals))
    n_days = int(len(set(days)))

    mean = float(np.mean(vals)) if n_cases > 0 else None
    t_stat = None
    if n_cases >= 2:
        dev = pd.Series(vals - mean).groupby(pd.Series(days)).sum()
        se = float(np.sqrt(np.sum(dev.to_numpy() ** 2)) / n_cases)
        if se > 0:
            t_stat = float(mean / se)
    corr = None
    if n_cases >= 3 and np.std(absf) > 0 and np.std(vals) > 0:
        corr = float(stats.pearsonr(absf, vals)[0])
    corr_pass = None if corr is None else bool(corr > 0)

    counts = {"cases": n_cases, "days": n_days}
    main = {"name": main_name, "value": mean,
            "statistic": None if t_stat is None else {"name": "t of the mean, cases of one day pooled", "value": t_stat},
            "threshold": thr}
    supp = {"name": "Pearson correlation of abs(forecast) with short-direction excess return",
            "value": corr, "passed": corr_pass}

    if n_cases < 30 or t_stat is None:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif mean > 0 and t_stat >= 2:
        if corr_pass:
            status = "confirmed"
            decided = "Mean short-direction excess return above 0 with t >= 2 on at least 30 cases, and correlation above 0."
        else:
            status = "inconclusive"
            decided = "A confirming t with a correlation at or below 0 is inconclusive."
    elif mean < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean short-direction excess return below 0 with t <= -2 on at least 30 cases: the price rises after large scaled up days."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
