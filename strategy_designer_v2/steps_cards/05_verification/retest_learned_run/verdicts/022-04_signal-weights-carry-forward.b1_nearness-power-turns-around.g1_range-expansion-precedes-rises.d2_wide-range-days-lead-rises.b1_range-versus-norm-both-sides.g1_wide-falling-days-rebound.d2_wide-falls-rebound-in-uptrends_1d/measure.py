import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    MIN_CASES = 100
    UP_COL = "debug_info.components.fall_range_up.last_history_value"
    DN_COL = "debug_info.components.fall_range_dn.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            high = pd.to_numeric(df["high"], errors="coerce").values
            low = pd.to_numeric(df["low"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            regime = df["regime"].astype(str).values
            up_raw = (pd.to_numeric(df[UP_COL], errors="coerce").values
                      if UP_COL in df.columns else np.full(len(df), np.nan))
            dn_raw = (pd.to_numeric(df[DN_COL], errors="coerce").values
                      if DN_COL in df.columns else np.full(len(df), np.nan))
            rng = high - low
            # Fallback when the component is not recorded: rebuild from prices.
            mean_rng = pd.Series(rng).rolling(30, min_periods=30).mean().values
            prev_close = np.concatenate([[np.nan], close[:-1]])
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                n_active += 1
                if regime[i] == "trending":
                    raw = up_raw[i]
                elif regime[i] == "unknown":
                    raw = dn_raw[i]
                else:
                    raw = np.nan
                if np.isnan(raw):
                    if np.isnan(prev_close[i]) or np.isnan(mean_rng[i]) or mean_rng[i] == 0:
                        continue
                    raw = rng[i] / mean_rng[i] if close[i] < prev_close[i] else 0.0
                down_day = True
                if not np.isnan(prev_close[i]):
                    down_day = close[i] < prev_close[i]
                in_situation = (raw > 0) and down_day
                if in_situation and fc[i] > 0:
                    n_agree += 1

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of 3-day excess return on forecast, forecast > 0 grid bars, pooled"
    threshold = "confirm: slope > 0 with t >= 2 on >= 100 cases; reject: slope < 0 with t <= -2 on >= 100 cases"
    check_name = "mean excess per unit forecast, trending minus unknown"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars on a down day with a "
                           "positive range multiple, as the plan's situation and side require."),
            "reading": "The situation is a down day (close below prior close) with a positive raw range multiple, side long.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            regime = df["regime"].astype(str).values
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    break
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                rows.append((coin, r, fc[i], regime[i]))

    g = pd.DataFrame(rows, columns=["coin", "ret", "fc", "regime"])
    if len(g) > 0:
        drift = g.groupby("coin")["ret"].mean()
        g["excess"] = g["ret"] - g["coin"].map(drift)
        cases = g[(g["fc"] > 0) & g["fc"].notna() & g["excess"].notna()].copy()
    else:
        cases = pd.DataFrame(columns=["coin", "ret", "fc", "regime", "excess"])
    n = int(len(cases))

    slope = None
    tval = None
    if n >= 3 and cases["fc"].nunique() > 1:
        res = stats.linregress(cases["fc"].astype(float).values, cases["excess"].astype(float).values)
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr > 0 else None

    tr = cases[cases["regime"] == "trending"]
    un = cases[cases["regime"] == "unknown"]
    n_tr, n_un = int(len(tr)), int(len(un))
    check_val = None
    check_pass = None
    if n_tr > 0 and n_un > 0 and tr["fc"].sum() > 0 and un["fc"].sum() > 0:
        per_tr = tr["excess"].sum() / tr["fc"].sum()
        per_un = un["excess"].sum() / un["fc"].sum()
        check_val = float(per_tr - per_un)
        check_pass = bool(check_val > 0)

    counts = {"cases": n, "trending cases": n_tr, "unknown cases": n_un}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than 100 cases ({n}), the plan's minimum count."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither confirm nor reject is met."
    elif slope > 0 and tval >= 2:
        if check_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 on at least 100 cases and trending minus unknown is above 0."
        else:
            status = "inconclusive"
            decided = "A confirming slope whose supporting check fails (trending minus unknown not above 0)."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 on at least 100 cases."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {"name": check_name, "value": check_val, "passed": check_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("The normal drift is each coin's mean 3-day return over all grid bars of all its windows, "
                    "the mean excess per unit of forecast is sum(excess)/sum(forecast) per regime, "
                    "a regime is the record's regime on the case bar, and a supporting check that cannot be computed counts as not passed."),
    }
