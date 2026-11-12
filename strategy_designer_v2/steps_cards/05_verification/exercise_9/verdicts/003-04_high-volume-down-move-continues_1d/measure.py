import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LH = "debug_info.components.drop.last_history_value"
    agree_hits = 0
    agree_total = 0
    gains = []
    fcs = []

    for coin, windows in bars.items():
        for w, df in windows.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")

            # raw 1-day change: component value, falling back to the close-to-close change
            if LH in df.columns:
                chg = pd.to_numeric(df[LH], errors="coerce")
            else:
                chg = pd.Series(np.nan, index=df.index)
            chg = chg.where(chg.notna(), close.pct_change())

            vmean = vol.rolling(20, min_periods=20).mean()

            # situation check on active bars where the 20-bar volume mean is available
            active = fc.notna() & (fc != 0)
            checkable = active & vmean.notna() & chg.notna()
            situ = (chg < 0) & (vol >= vmean * (1 - 1e-12))
            ok = checkable & situ & (fc < 0)
            agree_total += int(checkable.sum())
            agree_hits += int(ok.sum())

            # main measure
            ret_next = close.shift(-1) / close - 1
            win_mean = (close / close.shift(1) - 1).mean()
            g = (fc / 10.0) * (ret_next - win_mean)
            m = active & ret_next.notna() & np.isfinite(g)
            gains.extend(g[m].tolist())
            fcs.extend(fc[m].tolist())

    agreement = agree_hits / agree_total if agree_total > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("The situation is a negative 1-day change on a bar whose volume is at or above the "
               "rolling 20-bar mean including that bar, checked only on active bars where 20 bars of "
               "volume exist in the window; the window's mean daily return is the mean of its close-to-close "
               "returns; position is forecast/10 as the plan says; the forecast split puts the n//2 most "
               "negative forecasts in the larger-short half and the n//2 least negative in the smaller-short "
               "half (middle bar dropped if n is odd); the 40-bar minimum counts active bars with a next-bar return.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(len(gains))},
            "decided_by": ("Fewer than 90% of active bars are high-volume down days (1-day change < 0 with "
                           "volume >= 20-bar mean) carrying a short forecast, so the config does not do what "
                           "the Fidelity situation says."),
            "reading": reading,
        }

    gains_a = np.asarray(gains, dtype=float)
    fcs_a = np.asarray(fcs, dtype=float)
    n = len(gains_a)

    mean = float(gains_a.mean()) if n > 0 else None
    if n > 1:
        sd = gains_a.std(ddof=1)
        t = float(mean / (sd / np.sqrt(n))) if sd > 0 else None
    else:
        t = None

    # supporting check
    sup_val, sup_pass = None, None
    if n >= 2:
        order = np.argsort(fcs_a, kind="mergesort")
        h = n // 2
        larger = gains_a[order[:h]]
        smaller = gains_a[order[n - h:]]
        sup_val = float(larger.mean() - smaller.mean())
        sup_pass = bool(sup_val > 0)

    if n < 40:
        status = "not observable"
        decided = f"Only {n} active bars pooled across windows, below the plan's minimum of 40."
    elif t is not None and mean > 0 and t >= 2:
        status = "confirmed"
        decided = "Mean demeaned per-bar gain is above 0 with t >= 2, meeting the confirm rule."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean demeaned per-bar gain is below 0 with t <= -2, meeting the reject rule."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2, so the result neither confirms nor rejects."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean demeaned per-bar gain (forecast/10 x next-bar return minus window mean)",
            "value": mean,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "larger-short half minus smaller-short half mean demeaned gain",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"active bars": int(n)},
        "decided_by": decided,
        "reading": reading,
    }
