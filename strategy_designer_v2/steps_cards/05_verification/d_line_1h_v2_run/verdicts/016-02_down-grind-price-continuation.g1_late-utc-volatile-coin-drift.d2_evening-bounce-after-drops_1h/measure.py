import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    MIN_CASES = 300
    RAW = "debug_info.components.fall.last_history_value"

    def _ts(s):
        if np.issubdtype(s.dtype, np.number):
            unit = "ms" if s.dropna().abs().median() > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    n_active = 0
    n_agree = 0
    cases = []  # (coin, forecast, fwd2)

    for coin in sorted(bars.keys()):
        grid_rets = []
        coin_cases = []
        for win in sorted(bars[coin].keys(), key=lambda w: (len(str(w)), str(w))):
            df = bars[coin][win]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            ts = _ts(df["timestamp"])
            coming_hour = (ts + pd.Timedelta(hours=1)).dt.hour.to_numpy()

            # raw value of the 'fall' component; recompute its sign from prices where not recorded
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(n, np.nan)
            ret24 = np.full(n, np.nan)
            if n > 24:
                ret24[24:] = close[24:] / close[:-24] - 1.0
            sign_src = np.where(np.isnan(raw), ret24, raw)

            situation = (coming_hour == 21) & (sign_src < 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

            # forward 2-bar return inside the window
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:-H] = close[H:] / close[:-H] - 1.0

            # coin's mean 2-bar return: non-overlapping grid 0, 2, 4, ... of each window
            g = fwd[0::H]
            grid_rets.append(g[np.isfinite(g)])

            for i in np.where(fc > 0)[0]:
                if np.isfinite(fwd[i]):
                    coin_cases.append((fc[i], fwd[i]))

        allg = np.concatenate(grid_rets) if grid_rets else np.array([])
        coin_mean = float(np.mean(allg)) if len(allg) else np.nan
        for f, r in coin_cases:
            if np.isfinite(coin_mean):
                cases.append((coin, f, r - coin_mean))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    main_name = "forecast-weighted mean excess 2-bar return at forecast > 0 bars"
    thr = "confirm: weighted mean > 0 with t >= 2 and upper-minus-lower half difference > 0; reject: weighted mean < 0 with t <= -2; min 300 cases"
    reading = ("Situation bars are those whose timestamp + 1h has hour 21 with a negative raw 'fall' value (24-bar return from prices where unrecorded); "
               "the t of the weighted mean is the ordinary t of the mean of forecast/mean(forecast) x excess return; "
               "the halves split the pooled cases sorted by forecast into the bottom floor(n/2) and top floor(n/2), the middle case dropped when n is odd; "
               "cases are forecast > 0 bars with a 2-bar return inside the window.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases with forecast > 0": int(len(cases))},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars closing at 21:00 UTC after a negative 24-bar return"
                           if n_active > 0 else "The forecast is never non-zero, so the plan's situation is never traded."),
            "reading": reading,
        }

    n_cases = len(cases)
    w = np.array([c[1] for c in cases], dtype=float)
    x = np.array([c[2] for c in cases], dtype=float)

    wmean = None
    tval = None
    if n_cases >= 2 and w.sum() > 0:
        wmean = float(np.sum(w * x) / np.sum(w))
        y = w / w.mean() * x
        sd = np.std(y, ddof=1)
        tval = float(np.mean(y) / (sd / np.sqrt(n_cases))) if sd > 0 else None

    diff = None
    welch = None
    sup_passed = None
    n_up = n_lo = 0
    if n_cases >= 4:
        order = np.argsort(w, kind="mergesort")
        half = n_cases // 2
        lo = x[order[:half]]
        up = x[order[n_cases - half:]]
        n_up, n_lo = len(up), len(lo)
        diff = float(np.mean(up) - np.mean(lo))
        res = stats.ttest_ind(up, lo, equal_var=False)
        welch = float(res.statistic) if np.isfinite(res.statistic) else None
        sup_passed = bool(diff > 0 and welch is not None and welch > 0)

    counts = {"cases with forecast > 0": int(n_cases),
              "upper half cases": int(n_up), "lower half cases": int(n_lo)}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases with forecast > 0 across all coins and windows, below the plan's minimum of 300."
    elif wmean is None or tval is None:
        status = "inconclusive"
        decided = "The weighted mean's t could not be computed, so neither the confirm nor the reject rule is met."
    elif wmean > 0 and tval >= 2 and sup_passed:
        status = "confirmed"
        decided = "The weighted mean excess return is positive with t >= 2 and the upper-minus-lower half difference is positive."
    elif wmean < 0 and tval <= -2:
        status = "rejected"
        decided = "The weighted mean excess return is negative with t <= -2."
    elif tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the upper-minus-lower half difference is not positive."
    else:
        status = "inconclusive"
        decided = "The weighted mean's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name,
                         "value": wmean,
                         "statistic": None if tval is None else {"name": "t of the weighted mean", "value": tval},
                         "threshold": thr},
        "supporting_check": {"name": "upper-half minus lower-half mean excess return (Welch t > 0)",
                             "value": diff, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
