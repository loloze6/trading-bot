import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    PERIOD = 12
    RAW = "debug_info.components.nr_break_quiet.last_history_value"
    BAND = 2.0

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            high = pd.to_numeric(df["high"], errors="coerce").to_numpy(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(float)
            raw = (pd.to_numeric(df[RAW], errors="coerce").to_numpy(float)
                   if RAW in df.columns else np.full(len(df), np.nan))
            prior_high = (pd.Series(high).shift(1)
                          .rolling(PERIOD, min_periods=PERIOD).max().to_numpy(float))
            for i in range(len(df)):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                if np.isfinite(prior_high[i]) and np.isfinite(close[i]):
                    sit = close[i] > prior_high[i]
                else:
                    sit = np.isfinite(raw[i]) and raw[i] > 0
                if sit and f > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean 18-bar excess return of the bets over the coin's normal drift"
    main_thr = "t >= 2 over at least 100 cases confirms; t <= -2 over at least 100 cases rejects"
    sup_name = "Welch t of high-forecast half minus low-forecast half mean excess return"
    reading = ("A bet is a rise of the positive forecast of at least 2 points from its lowest level since the last bet "
               "(from 0 after a flat bar), the first bet in each 18-bar grid cell (positions 0,18,... of the window) is the case, "
               "the drift is the coin's mean non-overlapping 18-bar return over all windows, the high half is the cases with "
               "entry forecast strictly above the median, and fewer than 100 cases is reported as not observable; the situation "
               "is the close above the prior 12-bar high (from the component's raw value > 0 on a window's first 12 bars).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the close is above the "
                           "prior 12-bar high, as the plan's situation and side require."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    excess = []
    entry_fc = []
    for coin, wins in bars.items():
        # coin drift over all windows
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            for p in range(0, len(c) - H, H):
                r = c[p + H] / c[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(float)
            ref = 0.0
            taken = set()
            for i in range(len(df)):
                f = fc[i]
                if f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND:
                    ref = f
                    cell = i // H
                    if cell in taken:
                        continue
                    taken.add(cell)
                    if i + H < len(c) and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                        r = c[i + H] / c[i] - 1.0
                        excess.append(r - drift)
                        entry_fc.append(f)
                else:
                    ref = min(ref, f)

    excess = np.asarray(excess, float)
    entry_fc = np.asarray(entry_fc, float)
    n = int(len(excess))

    mean_ex = float(np.mean(excess)) if n > 0 else None
    t_main = None
    if n > 1:
        sd = float(np.std(excess, ddof=1))
        t_main = float(mean_ex / (sd / np.sqrt(n))) if sd > 0 else None

    welch = None
    n_hi = n_lo = 0
    if n > 1:
        med = float(np.median(entry_fc))
        hi = excess[entry_fc > med]
        lo = excess[entry_fc <= med]
        n_hi, n_lo = int(len(hi)), int(len(lo))
        if n_hi >= 2 and n_lo >= 2:
            tt = stats.ttest_ind(hi, lo, equal_var=False)
            if np.isfinite(tt.statistic):
                welch = float(tt.statistic)
    sup_pass = None if welch is None else bool(welch > 0)

    if n < 100:
        status = "not observable"
        decided = f"Only {n} cases, below the plan's minimum of 100 cases."
    elif t_main is not None and t_main >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean excess return has t >= 2 over at least 100 cases and the supporting Welch t is above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2 over at least 100 cases but the high-forecast half does not beat the low-forecast half."
    elif t_main is not None and t_main <= -2:
        status = "rejected"
        decided = "The mean excess return has t <= -2 over at least 100 cases."
    else:
        status = "inconclusive"
        decided = "The mean excess return's t is between -2 and 2 over at least 100 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_ex,
                         "statistic": ({"name": "ordinary t of the mean", "value": t_main}
                                       if t_main is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": welch, "passed": sup_pass},
        "counts": {"cases": n, "high-forecast half": n_hi, "low-forecast half": n_lo},
        "decided_by": decided,
        "reading": reading,
    }
