import numpy as np
import pandas as pd
from scipy import stats


def _component_series(df, comp_id, field="last_history_value"):
    """Read a strategy component's recorded value, whether flattened or held as dicts."""
    flat = "debug_info.components.%s.%s" % (comp_id, field)
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    if "debug_info.components" in df.columns:
        def get(x):
            try:
                if isinstance(x, str):
                    import json
                    x = json.loads(x)
                v = x.get(comp_id, {}).get(field, None)
                return float(v) if v is not None else np.nan
            except Exception:
                return np.nan
        return df["debug_info.components"].apply(get).astype(float)
    return pd.Series(np.nan, index=df.index)


def measure(bars):
    eps = 1e-9
    band = 2.0
    min_days = 30

    # ---------------- situation check ----------------
    n_active = 0
    n_agree = 0
    n_active_full = 0
    n_agree_full = 0

    # ---------------- cases ----------------
    case_rows = []      # (coin, day, abs_forecast, next_return)
    coin_returns = {}   # coin -> list of 1-bar returns over all windows (drift)

    for coin in sorted(bars.keys()):
        rets_all = []
        for win in sorted(bars[coin].keys()):
            df = bars[coin][win].copy()
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            o = pd.to_numeric(df["open"], errors="coerce")
            h = pd.to_numeric(df["high"], errors="coerce")
            l = pd.to_numeric(df["low"], errors="coerce")
            c = pd.to_numeric(df["close"], errors="coerce")
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            ts = pd.to_datetime(df["timestamp"], utc=True)

            # recompute the regime detector's components from the prices (inside the window)
            trend60 = (c / c.shift(60) - 1.0) * 100.0
            ret1 = (c / c.shift(1) - 1.0) * 100.0
            ret5_px = (c / c.shift(5) - 1.0) * 100.0
            ret5_rec = _component_series(df, "depth5", "last_history_value")
            ret5 = ret5_px.where(ret5_px.notna(), ret5_rec)
            rng = h - l
            mean_rng = rng.rolling(20, min_periods=20).mean()
            wide = rng / mean_rng.replace(0, np.nan)
            loc = (c - l) / rng.replace(0, np.nan)

            conds = {
                "trend60": (trend60 < -10.0 + eps, trend60.notna()),
                "ret1": (ret1 > 0.0 + eps * 0, ret1.notna()),
                "ret5": (ret5 < 0.0, ret5.notna()),
                "wide": (wide >= 1.5 - eps, wide.notna()),
                "loc": (loc >= 0.75 - eps, loc.notna()),
            }
            all_known = np.ones(len(df), dtype=bool)
            all_hold = np.ones(len(df), dtype=bool)
            known_hold = np.ones(len(df), dtype=bool)
            for k, (hold, known) in conds.items():
                hv = hold.fillna(False).values.astype(bool)
                kv = known.values.astype(bool)
                all_known &= kv
                all_hold &= hv
                known_hold &= (hv | ~kv)
            active = (f != 0).values
            short = (f < 0).values

            n_active += int(active.sum())
            n_agree += int((active & known_hold & short).sum())
            n_active_full += int((active & all_known).sum())
            n_agree_full += int((active & all_known & all_hold & short).sum())

            # next-bar returns inside the window
            nxt = (c.shift(-1) / c - 1.0).values
            rets_all.extend([x for x in nxt if np.isfinite(x)])

            # bets on the short side: rise of the short forecast of at least the band
            ref = 0.0
            fv = f.values
            for i in range(len(df)):
                if fv[i] < 0:
                    s = -fv[i]
                    if s - ref >= band - eps:
                        if np.isfinite(nxt[i]):
                            case_rows.append((coin, ts.iloc[i].floor("D"), s, nxt[i]))
                        ref = s
                    else:
                        ref = min(ref, s)
                else:
                    ref = 0.0
        coin_returns[coin] = rets_all

    if n_active_full > 0:
        agreement = n_agree_full / n_active_full
        agree_basis = "full"
    elif n_active > 0:
        agreement = n_agree / n_active
        agree_basis = "partial"
    else:
        agreement = None
        agree_basis = "none"
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("Regime components recomputed from prices inside each window (60-day and 5-day returns in percent, "
               "range over the mean high-low of the last 20 bars including the bar, close location from the low); "
               "the agreement is taken over active bars where all five can be computed (falling back to the computable "
               "conditions only if none can be: basis '%s'); cases are short-side bets per the holding rule (rise of "
               "|forecast| of at least 2 from its lowest level since the last bet, reset on flat/long), drift is the "
               "coin's mean 1-bar return over all its windows, the t uses deviations summed per UTC day "
               "(day-clustered standard error), and fewer than 30 distinct case days is reported as not observable."
               % agree_basis)

    main_name = "mean next-day drift-adjusted short-side return per case (fraction)"
    threshold = "confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active_full if agree_basis == "full" else n_active)},
            "decided_by": ("Fewer than 90%% of the active bars (%.3f) are short bars where the 60-day return is below "
                           "-10%%, the day is up, the range is at least 1.5x the 20-day mean range, the close is in the "
                           "top quarter and the 5-day return is negative." % agreement),
            "reading": reading,
        }

    # ---------------- criterion ----------------
    drift = {k: (float(np.mean(v)) if len(v) else np.nan) for k, v in coin_returns.items()}
    if case_rows:
        cases = pd.DataFrame(case_rows, columns=["coin", "day", "absf", "r"])
        cases["drift"] = cases["coin"].map(drift)
        cases = cases.dropna(subset=["r", "drift"])
        cases["u"] = -(cases["r"] - cases["drift"])
    else:
        cases = pd.DataFrame(columns=["coin", "day", "absf", "r", "drift", "u"])

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_u = float(cases["u"].mean()) if n_cases else None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["u"] - mean_u
        dsum = dev.groupby(cases["day"]).sum().values
        var = (n_days / (n_days - 1.0)) * float(np.sum(dsum ** 2)) / (n_cases ** 2)
        se = np.sqrt(var)
        t_val = float(mean_u / se) if se > 0 else None

    rho = None
    if n_cases >= 3:
        r_, _ = stats.spearmanr(cases["absf"].values, cases["u"].values)
        rho = float(r_) if np.isfinite(r_) else None
    rho_pass = None if rho is None else bool(rho > 0)

    counts = {"cases": n_cases, "distinct case days": n_days}

    if n_days < min_days:
        status = "not observable"
        decided = "Fewer than 30 distinct case days (%d), the plan's minimum, so the data cannot show the idea." % n_days
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean short-side unusual move could not be computed, so neither rule is met."
    elif mean_u > 0 and t_val >= 2:
        if rho_pass:
            status = "confirmed"
            decided = "The mean short-side unusual move is above 0 with a t of 2 or more and the Spearman correlation is above 0."
        else:
            status = "inconclusive"
            decided = "A t of 2 or more with the supporting correlation not above 0 is inconclusive."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean short-side unusual move is below 0 with a t of -2 or less: the coin rises more than its drift the day after."
    else:
        status = "inconclusive"
        decided = "The t is between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_val is None else {"name": "t of the mean, cases of a day summed", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {"name": "Spearman(|forecast|, drift-adjusted short-side next-day return) > 0",
                             "value": rho, "passed": rho_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
