import numpy as np
import pandas as pd
from scipy import stats


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        unit = "ms" if s.abs().max() > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def _clustered_t(x, days):
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 2:
        return float(np.mean(x)) if n else None, None
    m = float(np.mean(x))
    dev = pd.Series(x - m).groupby(np.asarray(days)).sum().values
    g = len(dev)
    if g < 2:
        return m, None
    var = (dev ** 2).sum() / (n ** 2) * (g / (g - 1.0))
    se = np.sqrt(var)
    if not np.isfinite(se) or se == 0:
        return m, None
    return m, float(m / se)


def measure(bars):
    reading = (
        "The 20-day mean range includes the current bar and is computed inside each window, so a window's first 19 bars "
        "cannot be checked and are left out of the situation check; the close is in the lower half when "
        "(close-low)/(high-low) < 0.5; the coin's mean daily return is over every within-window next-day return of all "
        "its windows; same-day cases are combined by summing their deviations per UTC day (clustered standard error); "
        "the supporting split uses the median forecast of all cases with a next-day return, strictly above versus "
        "strictly below it; the plan's 'fewer than 100 cases / 60 days' rule is reported as 'not observable'."
    )

    active_total = 0
    active_ok = 0
    rows = []

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        coin_rets = []
        coin_rows = []
        for w in sorted(wins.keys()):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.copy()
            ts = _to_utc(df["timestamp"]).reset_index(drop=True)
            df = df.reset_index(drop=True)
            order = np.argsort(ts.values, kind="stable")
            df = df.iloc[order].reset_index(drop=True)
            ts = ts.iloc[order].reset_index(drop=True)

            high = pd.to_numeric(df["high"], errors="coerce")
            low = pd.to_numeric(df["low"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")

            rng = high - low
            mean20 = rng.rolling(20, min_periods=20).mean()
            with np.errstate(divide="ignore", invalid="ignore"):
                ratio = mean20 / rng.replace(0, np.nan)
                loc_pos = (close - low) / rng.replace(0, np.nan)
            evaluable = mean20.notna() & rng.notna()
            wide = (ratio <= 1.0 + 1e-12).fillna(False)
            lower = (loc_pos < 0.5).fillna(False)
            situation = wide & lower

            active = fc.notna() & (fc != 0)
            chk = active & evaluable
            active_total += int(chk.sum())
            active_ok += int((chk & situation & (fc > 0)).sum())

            ret = close.shift(-1) / close - 1.0
            coin_rets.append(ret.dropna().values)
            days = ts.dt.floor("D").dt.strftime("%Y-%m-%d")
            sel = (fc > 0) & ret.notna()
            for i in np.where(sel.values)[0]:
                coin_rows.append((coin, days.iloc[i], float(fc.iloc[i]), float(ret.iloc[i])))
        allr = np.concatenate(coin_rets) if coin_rets else np.array([])
        mu = float(np.mean(allr)) if len(allr) else np.nan
        for c, d, f, r in coin_rows:
            rows.append((c, d, f, r - mu))

    agreement = float(active_ok / active_total) if active_total > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean excess next-day return on forecast > 0 bars (coin's next-day return minus coin's mean daily return)"
    threshold = "confirm: mean > 0 with t >= 2 and supporting difference > 0; reject: mean < 0 with t <= -2"
    sup_name = "excess return, forecast above median minus below median (Welch)"

    if agreement is not None and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"cases": len(rows), "distinct days": len(set(r[1] for r in rows))},
            "decided_by": (
                f"Only {agreement:.3f} of the checkable active bars are long bars on a day with range at or above its "
                "20-day mean and a close in the lower half of its range, below the 90 % needed."
            ),
            "reading": reading,
        }

    df = pd.DataFrame(rows, columns=["coin", "day", "fc", "ex"])
    df = df[np.isfinite(df["ex"])]
    n_cases = int(len(df))
    n_days = int(df["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_ex, t_ex = (None, None)
    if n_cases:
        mean_ex, t_ex = _clustered_t(df["ex"].values, df["day"].values)

    sup_val, sup_t, sup_pass = None, None, None
    if n_cases:
        med = float(np.median(df["fc"].values))
        up = df.loc[df["fc"] > med, "ex"].values
        lo = df.loc[df["fc"] < med, "ex"].values
        if len(up) >= 1 and len(lo) >= 1:
            sup_val = float(np.mean(up) - np.mean(lo))
            if len(up) >= 2 and len(lo) >= 2:
                tt = stats.ttest_ind(up, lo, equal_var=False)
                sup_t = float(tt.statistic) if np.isfinite(tt.statistic) else None
            sup_pass = bool(sup_val > 0)

    sup = {"name": sup_name, "value": sup_val, "passed": sup_pass}
    if sup_t is not None:
        sup["welch_t"] = sup_t

    main = {
        "name": main_name,
        "value": mean_ex,
        "statistic": {"name": "t of the mean, same-day cases combined", "value": t_ex} if t_ex is not None else None,
        "threshold": threshold,
    }

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = f"The plan needs at least 100 cases on at least 60 distinct days; the record has {n_cases} cases on {n_days} days."
    elif t_ex is None:
        status = "inconclusive"
        decided = "The t of the mean excess return could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_ex > 0 and t_ex >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean excess next-day return > 0 with t >= 2, and the upper-minus-lower supporting difference > 0."
    elif mean_ex < 0 and t_ex <= -2:
        status = "rejected"
        decided = "Mean excess next-day return < 0 with t <= -2."
    elif t_ex >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting difference is at or below 0 (or could not be computed): inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess next-day return lies between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
