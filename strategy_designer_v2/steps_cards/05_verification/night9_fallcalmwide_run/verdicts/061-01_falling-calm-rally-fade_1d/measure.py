import json
import numpy as np
import pandas as pd


def measure(bars):
    COMP = "scaled_rise"
    BAND = 2.0
    MIN_CASES = 100
    MIN_DAYS = 50

    def to_time(s):
        if np.issubdtype(s.dtype, np.number):
            v = s.astype(float)
            unit = "ms" if v.abs().max() > 1e11 else "s"
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True, errors="coerce")

    def raw_component(df):
        col = "debug_info.components.%s.last_history_value" % COMP
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        if "debug_info.components" in df.columns:
            out = []
            for v in df["debug_info.components"].values:
                val = np.nan
                try:
                    d = v
                    if isinstance(d, str):
                        d = json.loads(d)
                    if isinstance(d, dict) and COMP in d and isinstance(d[COMP], dict):
                        x = d[COMP].get("last_history_value")
                        if x is not None:
                            val = float(x)
                except Exception:
                    val = np.nan
                out.append(val)
            return pd.Series(out, index=df.index, dtype=float)
        return pd.Series(np.nan, index=df.index, dtype=float)

    # ---------- pass 1: situation check, drift, cases ----------
    n_active = 0
    n_agree = 0
    drift_samples = {}
    case_rows = []  # (coin, day, fwd_ret, abs_forecast)

    for coin in sorted(bars.keys()):
        for win in sorted(bars[coin].keys()):
            df = bars[coin][win]
            if df is None or len(df) == 0:
                continue
            df = df.copy()
            df["_t"] = to_time(df["timestamp"])
            df = df.sort_values("_t").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values.astype(float)
            raw = raw_component(df).values.astype(float)
            regime = df["regime"].astype(str).str.strip().str.lower().values

            # 1-bar forward returns inside the window (grid of every bar, horizon 1)
            fwd = np.full(len(df), np.nan)
            if len(df) > 1:
                fwd[:-1] = close[1:] / close[:-1] - 1.0
            drift_samples.setdefault(coin, []).extend(list(fwd[np.isfinite(fwd)]))

            # situation check
            active = fc != 0
            in_profile = regime == "unknown"
            up_day = np.isfinite(raw) & (raw > 0)
            short = fc < 0
            n_active += int(active.sum())
            n_agree += int((active & in_profile & up_day & short).sum())

            # cases: forecast falls by >= BAND onto the short side (bet rule)
            ref = 0.0
            days = df["_t"].dt.floor("D").astype(str).values
            for i in range(len(df)):
                f = fc[i]
                if not (f < 0):
                    ref = 0.0
                    continue
                m = -f
                if m - ref >= BAND - 1e-12:
                    if np.isfinite(fwd[i]):
                        case_rows.append((coin, days[i], fwd[i], m))
                    ref = m
                else:
                    ref = min(ref, m)

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean next-day unusual move of short cases (drift removed, short direction)"
    threshold = "confirm: mean > 0 with day-pooled t >= 2 (and size split > 0); reject: mean < 0 with t <= -2"
    sup_name = "mean unusual move of larger-|forecast| half minus smaller half"
    reading = ("Profile read from the recorded regime ('unknown' = falling calm, not vetoed to chop) and the up day "
               "from the raw scaled_rise > 0; cases are short-side bets per the holding rule (a rise of |forecast| "
               ">= 2 from its lowest short level since the last bet, reset at flat/long) on every bar (1-bar grid); "
               "drift is the coin's mean 1-bar return pooled over all its windows; t uses day-clustered standard error "
               "(deviations summed per UTC day); the larger half is |forecast| strictly above the median, the smaller "
               "half at or below it.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of active bars are short forecasts on up days inside the falling calm "
                           "profile, so the config does not do what the plan's Fidelity says."),
            "reading": reading,
        }

    drift = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in drift_samples.items()}

    if case_rows:
        cases = pd.DataFrame(case_rows, columns=["coin", "day", "ret", "absf"])
        cases["drift"] = cases["coin"].map(drift)
        cases = cases[np.isfinite(cases["drift"]) & np.isfinite(cases["ret"])]
        cases["u"] = -(cases["ret"] - cases["drift"])
    else:
        cases = pd.DataFrame(columns=["coin", "day", "ret", "absf", "drift", "u"])

    N = int(len(cases))
    D = int(cases["day"].nunique()) if N else 0

    mean_u = float(cases["u"].mean()) if N else None
    t_val = None
    if N >= 2 and D >= 2:
        dev = cases["u"] - mean_u
        S = dev.groupby(cases["day"]).sum().values
        var = (D / (D - 1.0)) * float(np.sum(S ** 2)) / (N ** 2)
        se = np.sqrt(var) if var > 0 else np.nan
        t_val = float(mean_u / se) if np.isfinite(se) and se > 0 else None

    diff = None
    if N:
        med = float(cases["absf"].median())
        big = cases.loc[cases["absf"] > med, "u"]
        small = cases.loc[cases["absf"] <= med, "u"]
        if len(big) and len(small):
            diff = float(big.mean() - small.mean())
    sup_pass = None if diff is None else bool(diff > 0)

    counts = {"cases": N, "distinct days": D}
    out = {
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": None if t_val is None else {"name": "t of the mean, cases of one day pooled",
                                                                  "value": t_val},
                         "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "reading": reading,
    }

    if N < MIN_CASES:
        out["status"] = "not observable"
        out["decided_by"] = "Fewer than 100 cases (%d), the plan's minimum count." % N
        return out
    if D < MIN_DAYS:
        out["status"] = "not observable"
        out["decided_by"] = "Cases fall on fewer than 50 distinct days (%d), the plan's minimum count." % D
        return out

    if t_val is None:
        out["status"] = "inconclusive"
        out["decided_by"] = "The t of the mean unusual move could not be computed, so neither rule is met."
        return out

    if mean_u > 0 and t_val >= 2:
        if sup_pass:
            out["status"] = "confirmed"
            out["decided_by"] = ("Confirm rule: mean unusual move above 0 with t >= 2 and the larger-half minus "
                                 "smaller-half difference above 0.")
        else:
            out["status"] = "inconclusive"
            out["decided_by"] = "Inconclusive rule: t >= 2 with a size difference at or below 0."
        return out
    if mean_u < 0 and t_val <= -2:
        out["status"] = "rejected"
        out["decided_by"] = "Reject rule: mean unusual move below 0 with t <= -2 (the rises continue the next day)."
        return out
    out["status"] = "inconclusive"
    out["decided_by"] = "Inconclusive rule: the t of the mean unusual move is between -2 and 2."
    return out
