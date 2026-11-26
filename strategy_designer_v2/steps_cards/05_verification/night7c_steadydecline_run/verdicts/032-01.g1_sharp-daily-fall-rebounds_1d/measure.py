import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    BAND = 2.0
    THR = -2.0
    VOL_N = 20
    COL_RAW = "debug_info.components.fall.last_history_value"

    def ser(df, col):
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").reset_index(drop=True)
        return pd.Series(np.nan, index=range(len(df)))

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = ser(df, "close")
            fc = ser(df, "forecast").fillna(0.0)
            ret = close / close.shift(1) - 1.0
            vol = ret.rolling(VOL_N, min_periods=VOL_N).std(ddof=1)
            vsr_re = ret / vol.replace(0, np.nan)
            raw = ser(df, COL_RAW)
            vsr = raw.where(raw.notna(), vsr_re)
            active = fc != 0
            situ = (vsr <= THR) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean excess 2-bar return of the cases over the coin's mean 2-bar return, before costs"
    main_thr = "confirm: mean > 0 with t >= 2 (and slope > 0 with t >= 2); reject: mean < 0 with t <= -2 or slope < 0 with t <= -2"
    sup_name = "OLS slope of the case's excess 2-bar return on its forecast"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in the situation, long": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars where the 1-day return is "
                           "-2 or less in 20-day standard deviations with a long (positive) forecast, "
                           "as the plan's Fidelity requires."),
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    cases = []  # (day, excess_signed, forecast)
    for coin, wins in bars.items():
        # coin's normal drift: mean of non-overlapping 2-bar returns over all windows
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = ser(df, "close").values.astype(float)
            fc = ser(df, "forecast").fillna(0.0).values.astype(float)
            ts = pd.to_datetime(df["timestamp"].reset_index(drop=True), utc=True)
            n = len(close)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            prepared.append((close, fc, ts, n))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for close, fc, ts, n in prepared:
            # bets: rise of forecast on its side by >= band from its lowest level on that side since last bet
            side_prev = 0
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            bet_side = np.zeros(n, dtype=int)
            for i in range(n):
                f = fc[i]
                s = 1 if f > 0 else (-1 if f < 0 else 0)
                if s == 0:
                    side_prev = 0
                    ref = 0.0
                    continue
                if s != side_prev:
                    ref = 0.0
                    side_prev = s
                mag = abs(f)
                if mag - ref >= BAND:
                    bet[i] = True
                    bet_side[i] = s
                    ref = mag
                else:
                    ref = min(ref, mag)
            # once per 2-bar grid cell: first bet bar of each cell
            seen = set()
            for i in range(n):
                if not bet[i]:
                    continue
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                ex = bet_side[i] * (r - drift)
                cases.append((ts.iloc[i].floor("D"), float(ex), float(fc[i])))

    n_cases = len(cases)
    days = sorted(set(c[0] for c in cases))
    n_days = len(days)
    counts = {"cases": int(n_cases), "case-days": int(n_days)}
    reading = ("Bets are read as in the holding-period rule (forecast rise >= 2 from its lowest level on its side since "
               "the last bet), one per 2-bar grid cell from each window's first row taking the cell's first bet bar and "
               "its return from that bar's close over 2 bars inside the window; the drift is the coin's mean of grid "
               "2-bar returns over all its windows; the mean's t sums deviations per day (cluster SE with D/(D-1)); "
               "the slope is ordinary OLS on the case's forecast; the 30 minimum counts case-days.")

    mean_ex = float(np.mean([c[1] for c in cases])) if n_cases else None

    if n_days < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": mean_ex, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": "Fewer than 30 cases (case-days) in total, the plan's minimum count.",
            "reading": reading,
        }

    ex = np.array([c[1] for c in cases])
    fx = np.array([c[2] for c in cases])
    dser = pd.Series(ex - ex.mean(), index=[c[0] for c in cases])
    day_sums = dser.groupby(level=0).sum().values
    D = len(day_sums)
    var_mean = (D / (D - 1.0)) * np.sum(day_sums ** 2) / (n_cases ** 2) if D > 1 else np.nan
    t_mean = float(ex.mean() / np.sqrt(var_mean)) if (np.isfinite(var_mean) and var_mean > 0) else 0.0

    slope = None
    t_slope = 0.0
    if n_cases >= 3 and np.std(fx) > 0:
        lr = stats.linregress(fx, ex)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else 0.0
    sup_pass = bool(slope is not None and slope > 0 and t_slope >= 2)

    if (mean_ex < 0 and t_mean <= -2) or (slope is not None and slope < 0 and t_slope <= -2):
        status = "rejected"
        decided = ("Reject rule met: the mean excess return is negative with t <= -2, or the slope is negative with t <= -2 "
                   f"(t mean {t_mean:.2f}, t slope {t_slope:.2f}).")
    elif mean_ex > 0 and t_mean >= 2 and sup_pass:
        status = "confirmed"
        decided = ("Confirm rule met: the mean excess return is positive with t >= 2 and the slope on the forecast is "
                   f"positive with t >= 2 (t mean {t_mean:.2f}, t slope {t_slope:.2f}).")
    else:
        status = "inconclusive"
        decided = ("Inconclusive rule: neither the confirm nor the reject rule is met, a t lies between -2 and 2 on a measure "
                   f"(t mean {t_mean:.2f}, t slope {t_slope:.2f}).")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_ex,
                         "statistic": {"name": "t of the mean, cases of one day taken together", "value": t_mean},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": slope, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
