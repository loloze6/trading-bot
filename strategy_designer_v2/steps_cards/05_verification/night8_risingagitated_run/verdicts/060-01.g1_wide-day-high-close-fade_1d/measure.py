import numpy as np
import pandas as pd
from scipy import stats


def _component_value(df, comp_id, field="last_history_value"):
    """Read a recorded component value, flattened column or nested dict column."""
    col = f"debug_info.components.{comp_id}.{field}"
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    if "debug_info.components" in df.columns:
        def get(x):
            try:
                if isinstance(x, dict):
                    c = x.get(comp_id)
                    if isinstance(c, dict):
                        v = c.get(field)
                        return float(v) if v is not None else np.nan
            except Exception:
                return np.nan
            return np.nan
        return df["debug_info.components"].apply(get).astype(float)
    return pd.Series(np.nan, index=df.index)


def measure(bars):
    eps = 1e-9
    n_active = 0
    n_agree = 0
    rows = []  # (coin, date, ret, absf)
    drift = {}

    for coin, windows in bars.items():
        coin_rets = []
        coin_rows = []
        for w in sorted(windows.keys(), key=lambda s: int(str(s).lstrip("w")) if str(s).lstrip("w").isdigit() else str(s)):
            df = windows[w].copy().reset_index(drop=True)
            if len(df) == 0:
                continue
            hi = pd.to_numeric(df["high"], errors="coerce")
            lo = pd.to_numeric(df["low"], errors="coerce")
            cl = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            rng = hi - lo
            loc = (cl - lo) / rng.where(rng > 0)
            # range multiple: recorded raw value where present, else recomputed from prices
            rr_rec = _component_value(df, "wide_range")
            rr_calc = rng / rng.rolling(20, min_periods=20).mean()
            rr = rr_rec.where(rr_rec.notna(), rr_calc)

            situ = (loc >= 0.75 - eps) & (rr >= 1.5 - eps)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())

            ret = cl.shift(-1) / cl - 1.0  # inside the window only
            coin_rets.append(ret.dropna().values)
            ts = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D")
            mask = (fc < 0) & ret.notna()
            for i in np.where(mask.values)[0]:
                coin_rows.append((coin, ts.iloc[i], float(ret.iloc[i]), abs(float(fc.iloc[i]))))
        allr = np.concatenate(coin_rets) if coin_rets else np.array([])
        drift[coin] = float(np.mean(allr)) if len(allr) else np.nan
        rows.extend(coin_rows)

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90
    sit = {"agreement": float(agreement), "passed": bool(passed)}
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases and slope >= 0; reject: mean < 0 with t <= -2 over >= 30 cases"
    mm_name = "mean short-direction unusual next-bar move on forecast<0 bars"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": sit,
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars with close location >= 0.75 "
                           "and range multiple >= 1.5, so the config does not do what the Fidelity situation says."
                           if n_active > 0 else "The record has no active bar, so the config never takes the plan's situation."),
            "reading": "Situation recomputed from prices (close location) and the recorded wide_range raw value (range multiple, recomputed from prices where missing); profile vetoes are not part of the situation.",
        }

    cases = pd.DataFrame(rows, columns=["coin", "day", "ret", "absf"])
    if len(cases):
        cases["u"] = -(cases["ret"] - cases["coin"].map(drift))
        cases = cases.dropna(subset=["u", "absf"])
    n = int(len(cases))
    n_days = int(cases["day"].nunique()) if n else 0

    mean_u = float(cases["u"].mean()) if n else None
    t = None
    if n >= 2 and n_days >= 2:
        dev = cases["u"] - mean_u
        g = dev.groupby(cases["day"]).sum()
        G = len(g)
        var = float((g ** 2).sum()) * G / (G - 1)
        se = np.sqrt(var) / n
        t = float(mean_u / se) if se > 0 else None

    slope = None
    slope_pass = None
    if n >= 3 and cases["absf"].nunique() > 1:
        lr = stats.linregress(cases["absf"].values, cases["u"].values)
        slope = float(lr.slope)
        slope_pass = bool(slope >= 0)

    counts = {"cases": n, "days": n_days}
    if n < 30:
        status = "not observable"
        decided = f"Only {n} cases, below the plan's minimum of 30 cases."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the unusual move could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t >= 2 and slope_pass:
        status = "confirmed"
        decided = "Mean short-direction unusual move above 0 with t >= 2 over at least 30 cases, and the slope on abs(forecast) is >= 0."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "Mean short-direction unusual move below 0 with t <= -2 over at least 30 cases: the coin rises after these days."
    elif mean_u > 0 and t >= 2:
        status = "inconclusive"
        decided = "Positive t >= 2 but the slope check failed, which the plan's inconclusive rule covers."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan's inconclusive rule covers."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": {"name": mm_name, "value": mean_u,
                         "statistic": ({"name": "t of the mean, cases clustered by day", "value": t} if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "OLS slope of short-direction unusual move on abs(forecast)", "value": slope,
                             "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Every bar with forecast < 0 and a next bar in the same window is a case (1-bar grid = every bar), the drift is the coin's "
                    "mean 1-bar return over all its windows, the day-clustered t sums the deviations per UTC day, and the slope is an ordinary least-squares fit."),
    }
