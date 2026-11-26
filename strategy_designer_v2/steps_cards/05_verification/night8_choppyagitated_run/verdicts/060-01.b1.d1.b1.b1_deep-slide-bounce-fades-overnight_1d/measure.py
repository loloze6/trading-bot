import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.slide_depth.last_history_value"

    def fall5_from_prices(close):
        # 5-bar return ending at t-1, over the 30-bar std of daily returns at t-1 (inside the window)
        r1 = close.pct_change()
        ret5 = close / close.shift(5) - 1.0
        vol = r1.rolling(30, min_periods=30).std()
        return (ret5 / vol).shift(1)

    # ---------- per-coin mean daily return over all windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = df["close"].astype(float).reset_index(drop=True)
            rets.append((c.shift(-1) / c - 1.0).dropna())
        coin_mean[coin] = float(pd.concat(rets).mean()) if rets else np.nan

    # ---------- situation check and case collection ----------
    n_active = 0
    n_agree = 0
    case_rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            fc = pd.to_numeric(d[FC], errors="coerce")
            up1 = close / close.shift(1) - 1.0
            if RAW in d.columns:
                f5 = pd.to_numeric(d[RAW], errors="coerce")
            else:
                f5 = pd.Series(np.nan, index=d.index)
            f5 = f5.where(f5.notna(), fall5_from_prices(close))

            active = fc.notna() & (fc != 0)
            checkable = active & up1.notna() & f5.notna()
            situ = (up1 > 0) & (f5 < 0)
            n_active += int(checkable.sum())
            n_agree += int((checkable & situ & (fc < 0)).sum())

            nxt = close.shift(-1) / close - 1.0
            ts = pd.to_datetime(d["timestamp"], utc=True)
            m = (fc < 0) & nxt.notna()
            for i in np.where(m.values)[0]:
                case_rows.append({
                    "coin": coin,
                    "day": ts.iloc[i].floor("D"),
                    "fc": float(fc.iloc[i]),
                    "excess": float(nxt.iloc[i] - coin_mean[coin]),
                })

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    situation_check = {"agreement": float(agreement), "passed": passed}

    reading = ("Situation checked as a one-day close-to-close rise with the 5-day vol-scaled return at t-1 "
               "below 0 (recorded slide_depth raw value, recomputed from prices if missing) on the short side, "
               "over active bars where it can be computed (a window's first bar is left out), the code-added "
               "profile not being rechecked; cases are bars with forecast<0 and a next close in the same window, "
               "summed per UTC day before the mean and its t; the plan's minimum counts, when unmet, give "
               "'not observable'.")

    main_name = "mean of forecast/10 x next-day excess return, cases summed per day"
    threshold = "positive with t >= 2 confirms (with negative slope); negative with t <= -2 rejects"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": len(case_rows)},
            "decided_by": ("Fewer than 90% of the active bars are one-day rises after a 5-day scaled fall "
                           "with a short forecast, as the plan's Fidelity requires."),
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows, columns=["coin", "day", "fc", "excess"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    main_val, t_val = None, None
    if n_cases > 0:
        cases["gain"] = cases["fc"] / 10.0 * cases["excess"]
        daily = cases.groupby("day")["gain"].sum()
        main_val = float(daily.mean())
        if len(daily) > 1:
            sd = float(daily.std(ddof=1))
            t_val = float(main_val / (sd / np.sqrt(len(daily)))) if sd > 0 else None

    slope = None
    if n_cases > 2 and cases["fc"].abs().nunique() > 1:
        lr = stats.linregress(cases["fc"].abs().values, cases["excess"].values)
        slope = float(lr.slope)
    slope_ok = (slope is not None) and (slope < 0)

    main_measure = {
        "name": main_name,
        "value": main_val,
        "statistic": {"name": "t of the mean of daily sums", "value": t_val} if t_val is not None else None,
        "threshold": threshold,
    }
    supporting = {"name": "slope of next-day excess return on |forecast|", "value": slope,
                  "passed": bool(slope_ok) if slope is not None else None}
    counts = {"cases": n_cases, "distinct days": n_days}

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = f"Minimum not reached: {n_cases} cases on {n_days} distinct days, against at least 100 cases on 60 days."
    elif t_val is not None and main_val > 0 and t_val >= 2 and slope_ok:
        status = "confirmed"
        decided = "The main measure is positive with t >= 2 and the supporting slope is negative."
    elif t_val is not None and main_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "The main measure is negative with t <= -2."
    elif t_val is not None and main_val > 0 and t_val >= 2:
        status = "inconclusive"
        decided = "The main measure confirms but the supporting slope is not negative."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2 (neither confirm nor reject)."

    return {
        "status": status,
        "situation_check": situation_check,
        "main_measure": main_measure,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
