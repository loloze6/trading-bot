import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.fade_volw_move.last_history_value"
    H = 4

    # ---------- 1. Situation check ----------
    # The situation is the raw product (last hour's move x volatility ratio).
    # It applies on every bar, and the idea fades it, so the forecast should
    # have the opposite sign of the raw value.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0) & raw.notna()
            n_active += int(active.sum())
            agree = active & (np.sign(f) == -np.sign(raw)) & (raw != 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "pooled OLS slope of excess 4-bar return on forecast"
    threshold = "slope > 0 with t >= 2 confirms (with supporting check); slope < 0 with t <= -2 rejects"
    sup_name = "mean of sign(forecast) x excess 4-bar return over top fifth of |forecast|"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars have a forecast of the opposite sign to the raw "
                           "volatility-weighted last-hour move, so the config does not fade the plan's situation."),
            "reading": ("Active bars are those with a non-zero forecast and a recorded raw value; "
                        "the expected side is opposite to the raw value's sign."),
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, w, c1 / c0 - 1.0, fc[t]))

    s = pd.DataFrame(rows, columns=["coin", "window", "ret", "forecast"])
    if len(s) > 0:
        s["coin_mean"] = s.groupby("coin")["ret"].transform("mean")
        s["excess"] = s["ret"] - s["coin_mean"]
        s = s.dropna(subset=["excess", "forecast"])

    n_sampled = int(len(s))
    n_nonzero = int((s["forecast"] != 0).sum()) if n_sampled else 0

    counts = {
        "non-overlapping sampled bars with a non-zero forecast": n_nonzero,
        "sampled bars": n_sampled,
    }

    reading = ("Active bars for the situation check are those with a non-zero forecast and a recorded raw value; "
               "the regression uses all sampled bars (zero forecasts included) with an intercept and the classic "
               "OLS standard error; the coin's mean 4-bar return is the mean of its sampled returns over all its "
               "windows; the top fifth is the sampled bars with |forecast| at or above the 80th percentile of "
               "|forecast| over all sampled bars.")

    if n_nonzero < 1000:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": passed},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": "Fewer than 1000 non-overlapping sampled bars with a non-zero forecast.",
            "reading": reading,
        }

    x = s["forecast"].to_numpy(dtype=float)
    y = s["excess"].to_numpy(dtype=float)
    n = len(x)
    xm = x.mean()
    ym = y.mean()
    sxx = float(np.sum((x - xm) ** 2))
    if sxx > 0 and n > 2:
        slope = float(np.sum((x - xm) * (y - ym)) / sxx)
        intercept = ym - slope * xm
        resid = y - intercept - slope * x
        sigma2 = float(np.sum(resid ** 2) / (n - 2))
        se = np.sqrt(sigma2 / sxx)
        t_stat = float(slope / se) if se > 0 else 0.0
    else:
        slope, t_stat = 0.0, 0.0

    absf = np.abs(x)
    q80 = float(np.quantile(absf, 0.8))
    top = absf >= q80
    if top.sum() > 0:
        sup_val = float(np.mean(np.sign(x[top]) * y[top]))
    else:
        sup_val = None
    sup_pass = bool(sup_val is not None and sup_val > 0)
    counts["top-fifth sampled bars"] = int(top.sum())

    if slope > 0 and t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the top-fifth mean of sign(forecast) x excess return is above 0."
    elif slope < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    elif slope > 0 and t_stat >= 2:
        status = "inconclusive"
        decided = "The slope has t >= 2 but the top-fifth mean is not above 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "OLS slope t", "value": t_stat},
                         "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
