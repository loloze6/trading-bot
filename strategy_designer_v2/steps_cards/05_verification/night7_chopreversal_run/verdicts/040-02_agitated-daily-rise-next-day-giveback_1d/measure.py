import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.day_rise.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    # ---------- coin mean daily return over all windows ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp")
            c = d["close"].astype(float).values
            if len(c) > 1:
                rets.append(c[1:] / c[:-1] - 1.0)
        rets = np.concatenate(rets) if rets else np.array([])
        rets = rets[np.isfinite(rets)]
        coin_mu[coin] = float(np.mean(rets)) if len(rets) else np.nan

    # ---------- situation check + collect cases ----------
    n_active = 0
    n_agree = 0
    case_rows = []
    for coin, wins in bars.items():
        mu = coin_mu[coin]
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            regime = d["regime"].astype(str)
            pct = close / close.shift(1) - 1.0  # inside the window only
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                raw = raw.where(raw.notna(), pct)
            else:
                raw = pct
            agitated = regime != "chop"
            situation = agitated & (raw > 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            nxt = close.shift(-1) / close - 1.0
            alloc = pd.to_numeric(d[ALLOC], errors="coerce") if ALLOC in d.columns else pd.Series(np.nan, index=d.index)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            for i in d.index[fc < 0]:
                r = nxt.iloc[i]
                a = alloc.iloc[i]
                if not (np.isfinite(r) and np.isfinite(a) and np.isfinite(mu)):
                    continue
                ex = r - mu
                case_rows.append({
                    "day": ts.iloc[i].floor("D"),
                    "gain": a * ex,
                    "excess": ex,
                    "forecast": float(fc.iloc[i]),
                })

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean excess gain (position x next-day excess return) on short bars, summed per day"
    threshold = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2"
    reading = ("The agitated profile is read as the recorded regime not being 'chop' (the detector's veto), the rise as "
               "the recorded raw day change > 0 (recomputed from closes if missing), the 100 distinct days are days "
               "with a measurable short case, and the slope is pooled over all short cases (not day sums).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "distinct days with a short case": None},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are short bars on an up day inside the "
                           "agitated (non-chop) profile, as the Fidelity's situation and side require."),
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows, columns=["day", "gain", "excess", "forecast"])
    n_cases = int(len(cases))
    daily = cases.groupby("day")["gain"].sum() if n_cases else pd.Series(dtype=float)
    n_days = int(len(daily))

    mean_gain = float(daily.mean()) if n_days else None
    if n_days >= 2 and daily.std(ddof=1) > 0:
        t = float(daily.mean() / (daily.std(ddof=1) / np.sqrt(n_days)))
    else:
        t = None

    slope = None
    if n_cases >= 3 and cases["forecast"].nunique() > 1:
        slope = float(stats.linregress(cases["forecast"].values, cases["excess"].values).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    counts = {"distinct days with a short case": n_days, "short cases": n_cases}

    if n_days < 100 or t is None:
        status = "not observable"
        decided = f"Fewer than 100 distinct days with a short case ({n_days}), the plan's minimum."
    elif t >= 2 and mean_gain > 0:
        if slope_pass:
            status = "confirmed"
            decided = "Mean excess gain above 0 with t >= 2 and a positive supporting slope (confirm rule)."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting slope is zero or negative (inconclusive rule)."
    elif t <= -2 and mean_gain < 0:
        status = "rejected"
        decided = "Mean excess gain below 0 with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_gain,
            "statistic": None if t is None else {"name": "t of the mean over days", "value": t},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "slope of next-day excess return on forecast",
            "value": slope,
            "passed": slope_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
