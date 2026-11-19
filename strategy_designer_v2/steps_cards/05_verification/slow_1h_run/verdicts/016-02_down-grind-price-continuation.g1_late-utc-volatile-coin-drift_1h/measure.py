import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    ONE_H = pd.Timedelta(hours=1)

    # ---------- 1. Situation check ----------
    # Plan situation: the coming bar starts at 21:00 or 22:00 UTC, i.e. bars stamped 20:00 and 21:00.
    # Outcome: a rise, so the expected side is long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            ts = pd.to_datetime(df["timestamp"], utc=True)
            fc = pd.to_numeric(df[FC], errors="coerce")
            coming_hour = (ts + ONE_H).dt.hour
            in_slot = coming_hour.isin([21, 22])
            # The raw vol7d value (a std) is non-negative, so the expected sign is long.
            col = "debug_info.components.vol7d.last_history_value"
            if col in df.columns:
                raw = pd.to_numeric(df[col], errors="coerce")
                raw_ok = ~(raw < 0)
            else:
                raw_ok = pd.Series(True, index=df.index)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & in_slot & (fc > 0) & raw_ok).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of vol-sized excess slot return (excess 2-bar return x forecast/10)"
    main_thr = "mean > 0 with t >= 2 to confirm; t <= -2 rejects"
    sup_name = "OLS slope t of excess slot return on forecast at 20:00 bar"
    reading = ("Cases are every bar stamped 20:00 UTC whose 22:00 bar exists in the same window, "
               "including cases with forecast 0; the coin mean 2-bar return uses non-overlapping "
               "positions 0,2,4,... of each window pooled over all windows; all coins are pooled "
               "into one set of cases for the mean and the regression.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of active bars are long bars whose coming bar starts at 21:00 or "
                           "22:00 UTC, so the config does not trade the plan's slot on the long side."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    excess_all = []
    fc_all = []
    for coin, wins in bars.items():
        # coin mean 2-bar return over all windows (non-overlapping grid)
        r2 = []
        for w, df in wins.items():
            if df is None or len(df) < 3:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            idx = np.arange(0, len(c) - 2, 2)
            r = c[idx + 2] / c[idx] - 1.0
            r2.append(r[np.isfinite(r)])
        if not r2:
            continue
        r2 = np.concatenate(r2)
        if len(r2) == 0:
            continue
        mu = float(np.mean(r2))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            ts = pd.to_datetime(df["timestamp"], utc=True).reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            fc = pd.to_numeric(df[FC], errors="coerce").reset_index(drop=True)
            close_by_ts = pd.Series(c.values, index=ts.values)
            close_by_ts = close_by_ts[~close_by_ts.index.duplicated(keep="first")]
            sel = np.where(ts.dt.hour.values == 20)[0]
            for i in sel:
                t22 = ts.iloc[i] + 2 * ONE_H
                key = t22.to_datetime64()
                if key not in close_by_ts.index:
                    continue
                c0 = c.iloc[i]
                c2 = close_by_ts.loc[key]
                f = fc.iloc[i]
                if not (np.isfinite(c0) and np.isfinite(c2) and np.isfinite(f)) or c0 == 0:
                    continue
                excess_all.append(c2 / c0 - 1.0 - mu)
                fc_all.append(float(f))

    ex = np.asarray(excess_all, dtype=float)
    fcv = np.asarray(fc_all, dtype=float)
    n = int(len(ex))
    counts = {"slot cases": n}

    if n < 500:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Only {n} slot cases, below the plan's minimum of 500.",
            "reading": reading,
        }

    sized = ex * fcv / 10.0
    m = float(np.mean(sized))
    sd = float(np.std(sized, ddof=1))
    t_main = float(m / (sd / np.sqrt(n))) if sd > 0 else 0.0

    slope_t = None
    slope = None
    if np.std(fcv) > 0:
        lr = stats.linregress(fcv, ex)
        slope = float(lr.slope)
        slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else 0.0
    st = slope_t if slope_t is not None else 0.0
    sup_pass = bool(slope_t is not None and slope_t >= 2)

    if (m > 0 and t_main >= 2) and sup_pass:
        status = "confirmed"
        decided = f"Main mean > 0 with t = {t_main:.2f} >= 2 and supporting slope t = {st:.2f} >= 2."
    elif t_main <= -2 or st <= -2:
        status = "rejected"
        decided = f"Main mean t = {t_main:.2f} or supporting slope t = {st:.2f} is <= -2."
    else:
        status = "inconclusive"
        decided = (f"Main mean t = {t_main:.2f} and slope t = {st:.2f} meet neither the confirm rule "
                   "(both >= 2, mean > 0) nor the reject rule (either <= -2).")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": m,
                         "statistic": {"name": "t of the mean", "value": t_main},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": slope_t, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
