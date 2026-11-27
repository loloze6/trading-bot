import numpy as np
import pandas as pd
from scipy import stats


def _to_time(s):
    if np.issubdtype(s.dtype, np.number):
        mx = float(np.nanmax(s.values)) if len(s) else 0.0
        unit = "ms" if mx > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    LHV = "debug_info.components.heavy_vol.last_history_value"
    THRESH_T = 2.0
    MIN_DAYS = 300

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    n_active_unknown = 0
    case_rows = []          # (day, coin, forecast, next_ret)
    coin_rets = {}          # coin -> list of next-day returns over all windows

    for coin in sorted(bars.keys()):
        coin_rets.setdefault(coin, [])
        for win in sorted(bars[coin].keys()):
            df = bars[coin][win]
            if df is None or len(df) == 0:
                continue
            df = df.copy()
            if "timestamp" in df.columns:
                df["_t"] = _to_time(df["timestamp"])
                df = df.sort_values("_t").reset_index(drop=True)
            close = df["close"].astype(float)
            vol = df["volume"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)

            # day's return (PriceEvolutionComponent, period 1), inside the window
            day_ret = close / close.shift(1) - 1.0
            # volume ratio over 20 prior bars (exclude current), inside the window
            prior_mean = vol.shift(1).rolling(20, min_periods=20).mean()
            vr_rec = vol / prior_mean
            vr = vr_rec.copy()
            if LHV in df.columns:
                lhv = pd.to_numeric(df[LHV], errors="coerce")
                has = lhv.notna()
                vr[has] = lhv[has] + 1.0  # centred form: ratio - 1

            active = fc != 0
            known = day_ret.notna() & vr.notna()
            situ = (day_ret < 0) & (vr > 1.0)
            agree = active & known & situ & (fc > 0)
            n_active += int((active & known).sum())
            n_active_unknown += int((active & ~known).sum())
            n_agree += int(agree.sum())

            # next-day returns, inside the window
            nxt = close.shift(-1) / close - 1.0
            coin_rets[coin].extend(nxt.dropna().tolist())

            days = df["_t"].dt.floor("D") if "_t" in df.columns else pd.Series(df.index)
            cmask = (fc > 0) & nxt.notna()
            for i in np.where(cmask.values)[0]:
                case_rows.append((days.iloc[i], coin, float(fc.iloc[i]), float(nxt.iloc[i])))

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90
    reading_base = ("Situation recomputed as close[t]/close[t-1]-1 < 0 and volume / mean of the 20 prior volumes > 1 "
                    "(recorded heavy_vol raw value + 1 where present), active bars without a computable situation "
                    "(first bars of a window) left out; cases with the same UTC day are summed (both excess return and "
                    "forecast) into one observation for an OLS slope t; the plan's 300-day minimum, if not reached, "
                    "gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars without computable situation": int(n_active_unknown)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on a down day with volume "
                           "above its 20-day average, as the plan's Fidelity situation requires."),
            "reading": reading_base,
        }

    coin_mean = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in coin_rets.items()}

    cases = pd.DataFrame(case_rows, columns=["day", "coin", "fc", "ret"])
    if len(cases):
        cases["excess"] = cases["ret"] - cases["coin"].map(coin_mean)
        cases = cases.dropna(subset=["excess", "fc"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    slope = None
    slope_t = None
    mean_ex = None
    if n_cases:
        mean_ex = float(cases["excess"].mean())
        g = cases.groupby("day")[["fc", "excess"]].sum()
        x = g["fc"].values.astype(float)
        y = g["excess"].values.astype(float)
        if len(x) >= 3 and np.std(x) > 0:
            res = stats.linregress(x, y)
            slope = float(res.slope)
            slope_t = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    sup_pass = None if mean_ex is None else bool(mean_ex > 0)
    counts = {"distinct case days": n_days, "case bars": n_cases}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Only {n_days} distinct case days across coins and windows, below the plan's minimum of 300."
    elif slope_t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the day-summed forecast)."
    elif slope_t >= THRESH_T and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean excess next-day return over the cases is above 0."
    elif slope_t <= -THRESH_T:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif slope_t >= THRESH_T:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the mean excess next-day return is 0 or below."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of next-day excess return on forecast, case days summed",
            "value": slope,
            "statistic": None if slope_t is None else {"name": "OLS slope t", "value": slope_t},
            "threshold": "slope t >= 2 (with mean excess > 0) confirms; slope t <= -2 rejects",
        },
        "supporting_check": {
            "name": "mean excess next-day return over case bars > 0",
            "value": mean_ex,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
