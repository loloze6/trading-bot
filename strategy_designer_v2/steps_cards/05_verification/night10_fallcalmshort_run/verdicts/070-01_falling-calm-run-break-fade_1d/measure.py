import numpy as np
import pandas as pd
from scipy import stats


def _component_series(df, comp_id, field):
    """Read debug_info.components.<id>.<field>, flattened or nested; NaN where missing."""
    flat = f"debug_info.components.{comp_id}.{field}"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    if "debug_info.components" in df.columns:
        def get(v):
            if isinstance(v, dict):
                c = v.get(comp_id)
                if isinstance(c, dict):
                    x = c.get(field)
                    try:
                        return float(x) if x is not None else np.nan
                    except (TypeError, ValueError):
                        return np.nan
            return np.nan
        return df["debug_info.components"].apply(get).astype(float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def measure(bars):
    rows = []
    coin_rets = {}
    for coin in sorted(bars.keys()):
        rets_all = []
        for window in sorted(bars[coin].keys(), key=lambda w: (len(str(w)), str(w))):
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fwd = close.shift(-1) / close - 1.0  # next-day return, inside the window only
            rets_all.append(fwd.dropna().values)
            prev_up = close > close.shift(1)
            # Down run broken by today's up close, recomputed from prices (only where history exists in the window).
            down = (close < close.shift(1)).astype(int).values
            n = len(df)
            price_run = np.full(n, np.nan)
            for t in range(n):
                if t == 0 or not (close.iloc[t] > close.iloc[t - 1]):
                    continue
                k, j = 0, t - 1
                while j >= 1 and down[j] == 1:
                    k += 1
                    j -= 1
                if j >= 1:  # the run's start is known inside the window
                    price_run[t] = k
            run_len = _component_series(df, "run_len", "last_history_value")
            ts = pd.to_datetime(df["timestamp"], utc=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            out = pd.DataFrame({
                "coin": coin,
                "window": str(window),
                "day": ts.dt.floor("D").astype(str),
                "forecast": fc.values,
                "regime": df["regime"].astype(str).values,
                "run_len": run_len.values,
                "price_run": price_run,
                "up_close": prev_up.values,
                "has_prev": (close.shift(1).notna()).values,
                "fwd": fwd.values,
            })
            rows.append(out)
        coin_rets[coin] = np.concatenate(rets_all) if rets_all else np.array([])

    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": None, "supporting_check": None,
            "counts": {"cases": 0, "distinct days": 0},
            "decided_by": "No bars in the record.", "reading": "none",
        }
    allb = pd.concat(rows, ignore_index=True)

    # ---- Situation check ----
    run_val = allb["run_len"].where(allb["run_len"].notna(), allb["price_run"])
    up_ok = np.where(allb["has_prev"], allb["up_close"], True)
    situation = (allb["regime"] == "mean_reversion") & (run_val >= 2) & up_ok
    active = allb["forecast"] != 0
    n_active = int(active.sum())
    agree = float(((situation & (allb["forecast"] < 0)) & active).sum() / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agree >= 0.9
    reading = ("Falling calm profile read from regime == 'mean_reversion' (the detector's profile vetoes are not "
               "recorded), run length from run_len's last_history_value (prices as fallback), cases are all bars with "
               "forecast < 0 and a next close in the window, the day-clustered t uses per-day sums of deviations "
               "with a D/(D-1) correction, the supporting excess is unsigned (return minus coin mean), and the "
               "plan's minimum counts lead to 'not observable' as the workflow requires.")
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agree, "passed": False},
            "main_measure": None, "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the active bars are up closes ending a down run of 2+ days inside the "
                           "falling calm profile with a short forecast."),
            "reading": reading,
        }

    # ---- Criterion ----
    mu = {c: (float(np.mean(r)) if len(r) else np.nan) for c, r in coin_rets.items()}
    cases = allb[(allb["forecast"] < 0) & allb["fwd"].notna()].copy()
    cases["excess"] = cases["fwd"] - cases["coin"].map(mu)
    cases = cases[cases["excess"].notna()]
    cases["short_excess"] = -cases["excess"]
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique())

    main_mean, main_t = None, None
    if n_cases > 0:
        x = cases["short_excess"].values
        main_mean = float(np.mean(x))
        dev = cases.assign(d=x - main_mean).groupby("day")["d"].sum().values
        D = len(dev)
        if D > 1:
            se = np.sqrt(D / (D - 1) * np.sum(dev ** 2)) / n_cases
            main_t = float(main_mean / se) if se > 0 else None

    long_g = cases.loc[cases["run_len"] >= 3, "excess"].values
    short_g = cases.loc[cases["run_len"] == 2, "excess"].values
    diff, welch = None, None
    if len(long_g) > 0 and len(short_g) > 0:
        diff = float(np.mean(long_g) - np.mean(short_g))
    if len(long_g) >= 2 and len(short_g) >= 2:
        tt = stats.ttest_ind(long_g, short_g, equal_var=False)
        welch = float(tt.statistic) if np.isfinite(tt.statistic) else None
    supp_pass = (diff < 0) if diff is not None else None

    counts = {"cases": n_cases, "distinct days": n_days,
              "cases run >= 3": int(len(long_g)), "cases run == 2": int(len(short_g))}
    main = {
        "name": "mean next-day return beyond the coin's mean daily return, short direction",
        "value": main_mean,
        "statistic": {"name": "t of the mean, cases of one day summed", "value": main_t} if main_t is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2; reject: t <= -2",
    }
    supp = {"name": "mean excess return of runs >= 3 days minus runs of 2 days (Welch t " +
                    (f"{welch:.3f}" if welch is not None else "n/a") + ")",
            "value": diff, "passed": supp_pass}

    if n_cases < 30 or n_days < 25:
        status = "not observable"
        decided = f"The plan's minimum of 30 cases over 25 distinct days is not reached ({n_cases} cases, {n_days} days)."
    elif (main_t is not None and main_t <= -2) or (welch is not None and welch >= 2):
        status = "rejected"
        decided = ("Reject: the main measure's t is <= -2." if (main_t is not None and main_t <= -2)
                   else "Reject: the supporting difference's Welch t is >= +2 (longer runs are followed by weaker falls).")
    elif main_mean is not None and main_mean > 0 and main_t is not None and main_t >= 2 and supp_pass is True:
        status = "confirmed"
        decided = "Confirm: the main mean is above 0 with t >= 2 and the supporting difference is below 0."
    else:
        status = "inconclusive"
        if main_t is not None and main_t >= 2 and main_mean > 0:
            decided = "Inconclusive: main t >= 2 but the supporting difference is at or above 0 (or not measurable)."
        else:
            decided = "Inconclusive: the main t lies between -2 and 2 and no reject rule is met."

    return {
        "status": status,
        "situation_check": {"agreement": agree, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
