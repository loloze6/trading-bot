import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.rise72.last_history_value"
    SITU_HOURS = {23, 0, 7, 8, 15, 16}   # bars stamped at a settlement hour or the hour before it
    ENTRY_HOURS = {23, 7, 15}            # bars whose close is the settlement time
    H = 2
    MIN_CASES = 300

    n_active = 0
    n_agree = 0
    case_rows = []  # (coin, forecast, raw 2-bar return)
    coin_mean2 = {}

    for coin, wins in bars.items():
        grid_rets = []
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(df[FC], errors="coerce").astype(float)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            hours = ts.dt.hour.values

            # raw 72-bar rise: recorded value where present, else recomputed from prices inside the window
            recomputed = close / close.shift(72) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").astype(float)
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed

            # situation check
            active = fc.notna() & (fc != 0)
            in_clock = pd.Series([h in SITU_HOURS for h in hours], index=df.index)
            situ = in_clock & (raw > 0)
            agree = active & situ & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

            # forward 2-bar returns inside the window
            fwd = close.shift(-H) / close - 1.0

            # coin's mean 2-bar return: non-overlapping grid 0, 2, 4, ... of each window
            g = fwd.iloc[0::H].dropna()
            grid_rets.extend(g.tolist())

            # cases
            regime = df["regime"].astype(str)
            is_entry = pd.Series([h in ENTRY_HOURS for h in hours], index=df.index)
            cmask = is_entry & (regime == "trending") & (fc > 0) & fwd.notna()
            for f, r in zip(fc[cmask].values, fwd[cmask].values):
                case_rows.append((coin, float(f), float(r)))

        coin_mean2[coin] = float(np.mean(grid_rets)) if len(grid_rets) else np.nan

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Situation bars are those stamped 23:00, 00:00, 07:00, 08:00, 15:00, 16:00 UTC with a positive raw "
               "72-bar rise (recorded last_history_value, else recomputed from closes), expected side long; "
               "t+2 is two rows later in the same window; the coin's mean 2-bar return is pooled over all windows "
               "on the non-overlapping grid 0,2,4,...; the slope t is the ordinary OLS slope t of excess return on "
               "forecast, pooled over all coins and windows.")

    threshold = "confirm if slope t >= 2 with forecast-weighted mean excess > 0; reject if slope t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "slope t of excess 2-bar return on forecast at settlement entry bars",
                             "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of non-zero-forecast bars are long bars at the settlement clock hours "
                           "with a positive 72-bar rise, so the config does not trade the plan's situation."),
            "reading": reading,
        }

    f_arr = np.array([c[1] for c in case_rows], dtype=float)
    ex_arr = np.array([c[2] - coin_mean2.get(c[0], np.nan) for c in case_rows], dtype=float)
    ok = np.isfinite(f_arr) & np.isfinite(ex_arr)
    f_arr, ex_arr = f_arr[ok], ex_arr[ok]
    n_cases = int(len(f_arr))

    slope = None
    t_slope = None
    if n_cases >= 3 and np.ptp(f_arr) > 0:
        lr = stats.linregress(f_arr, ex_arr)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    wmean = float(np.sum(ex_arr * f_arr) / np.sum(f_arr)) if n_cases > 0 and np.sum(f_arr) > 0 else None
    sup_passed = None if wmean is None else bool(wmean > 0)

    main = {
        "name": "slope t of excess 2-bar return on forecast at settlement entry bars",
        "value": slope,
        "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
        "threshold": threshold,
    }
    supporting = {"name": "forecast-weighted mean excess 2-bar return", "value": wmean, "passed": sup_passed}
    counts = {"cases pooled across coins and windows": n_cases}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases pooled across coins and windows, below the plan's minimum of 300."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_passed:
        status = "confirmed"
        decided = "The slope t is 2 or more and the forecast-weighted mean excess return is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope t is 2 or more but the forecast-weighted mean excess return is 0 or below."
    else:
        status = "inconclusive"
        decided = "The slope t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
