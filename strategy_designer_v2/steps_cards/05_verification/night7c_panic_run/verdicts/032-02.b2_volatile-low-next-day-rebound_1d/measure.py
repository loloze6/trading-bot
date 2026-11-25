import numpy as np
import pandas as pd
from scipy import stats


def _ts(series):
    s = series
    if np.issubdtype(s.dtype, np.number):
        v = float(np.nanmedian(s.values)) if len(s) else 0.0
        unit = "ms" if v > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def _component_raw(df, cid):
    col = "debug_info.components.%s.last_history_value" % cid
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    if "debug_info.components" in df.columns:
        out = []
        for d in df["debug_info.components"].values:
            val = np.nan
            if isinstance(d, dict):
                c = d.get(cid)
                if isinstance(c, dict):
                    v = c.get("last_history_value")
                    try:
                        val = float(v) if v is not None else np.nan
                    except Exception:
                        val = np.nan
            out.append(val)
        return pd.Series(out, index=df.index, dtype=float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def measure(bars):
    situation_rows = []
    case_rows = []
    coin_rets = {}

    for coin in sorted(bars.keys()):
        allr = []
        for w in sorted(bars[coin].keys(), key=lambda x: (len(str(x)), str(x))):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            low = pd.to_numeric(df["low"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            regime = df["regime"].astype(str)
            day = _ts(df["timestamp"]).dt.floor("D")

            r1 = close.shift(-1) / close - 1.0
            allr.append(r1.dropna().values)

            # condition 1: 30-bar close-to-close return < 0 (from prices when the window has the history)
            ret30 = close / close.shift(30) - 1.0
            # condition 3: close below the lowest low of the 30 prior bars (recorded raw value, else from prices)
            prior_low = low.shift(1).rolling(30, min_periods=30).min()
            below_px = close / prior_low - 1.0
            below_rec = _component_raw(df, "depth")
            below = below_rec.where(below_rec.notna(), below_px)
            is_mr = regime == "mean_reversion"
            c1 = np.where(ret30.notna(), ret30 < 0, is_mr)
            # condition 2: the 365/30 range ratio needs 365 bars of history the window does not hold -> detector's regime
            c2 = is_mr.values
            c3 = np.where(below.notna(), below < 0, is_mr)
            sit = np.asarray(c1, bool) & np.asarray(c2, bool) & np.asarray(c3, bool)

            active = fc.values != 0
            for i in np.where(active)[0]:
                situation_rows.append(bool(sit[i] and fc.values[i] > 0))

            for i in range(len(df)):
                if is_mr.iloc[i] and fc.iloc[i] > 0 and np.isfinite(r1.iloc[i]):
                    case_rows.append((coin, day.iloc[i], float(fc.iloc[i]), float(r1.iloc[i])))
        coin_rets[coin] = np.concatenate(allr) if allr else np.array([])

    n_active = len(situation_rows)
    agreement = float(np.mean(situation_rows)) if n_active else None
    passed = bool(n_active > 0 and agreement >= 0.9)
    reading = ("The 365-to-30 range ratio (and the 30-bar return or prior-low distance where the window lacks the history) "
               "cannot be rebuilt inside a window, so the recorded mean_reversion regime stands for those conditions; "
               "the t is a day-clustered t (deviations summed per day, D/(D-1) correction); the plan's fewer-than-30-case-days "
               "rule is applied as the minimum count, giving 'not observable'.")
    threshold = "confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2; at least 30 distinct case days"
    mname = "mean next-day excess return of mean_reversion bars with forecast > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars of the plan's situation "
                          "(30-day fall, wide month's ranges, close below the prior 30-day low).",
            "reading": reading,
        }

    mean_daily = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in coin_rets.items()}
    cases = pd.DataFrame(case_rows, columns=["coin", "day", "fc", "r"])
    if len(cases):
        cases["x"] = cases["r"] - cases["coin"].map(mean_daily)
        cases = cases.dropna(subset=["x"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_x = float(cases["x"].mean()) if n_cases else None
    t = None
    if n_cases and n_days > 1:
        dev = cases["x"] - mean_x
        S = dev.groupby(cases["day"]).sum().values
        se = np.sqrt(n_days / (n_days - 1.0) * np.sum(S ** 2)) / n_cases
        t = float(mean_x / se) if se > 0 else None
    rho = None
    if n_cases >= 3:
        rr = stats.spearmanr(cases["fc"].values, cases["x"].values).correlation
        rho = float(rr) if np.isfinite(rr) else None
    sup_pass = (rho is not None and rho > 0)

    counts = {"distinct case days": n_days, "cases": n_cases}

    if n_days < 30:
        status = "not observable"
        decided = "Fewer than 30 distinct case days across all coins and windows (%d)." % n_days
    elif t is not None and mean_x > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean next-day excess return is positive with t >= 2 and the Spearman correlation is above 0."
    elif t is not None and mean_x < 0 and t <= -2:
        status = "rejected"
        decided = "The mean next-day excess return is negative with t <= -2."
    elif t is not None and mean_x > 0 and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the Spearman correlation is 0 or below (or undefined), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The result lies between the confirm and reject rules, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": mname,
            "value": mean_x,
            "statistic": ({"name": "day-clustered t of the mean", "value": t} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {"name": "Spearman(forecast, next-day excess return) > 0", "value": rho,
                             "passed": (bool(sup_pass) if rho is not None else None)},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
