import numpy as np
import pandas as pd


def _standardise(raw, window, min_periods):
    # value(t) * 10 / mean(|last `window` raw values, bar t left out|), capped at -20..+20.
    # Warm-up bars are not in the record, so the rebuild is exact only where a full
    # `window` of past raw values exists inside the window; elsewhere it is NaN.
    raw = pd.Series(raw, dtype=float)
    denom = raw.abs().shift(1).rolling(window, min_periods=window).mean()
    out = raw * 10.0 / denom
    out = out.where(denom != 0, 0.0)
    out = out.where(denom.notna())
    return out.clip(-20.0, 20.0)


def measure(bars):
    H = 5
    pref = "debug_info.components."
    comps = {
        "mom28": (60, 20, False),
        "rev1": (60, 20, True),
        "high90": (90, 22, False),
        "vol30": (60, 20, True),
    }

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            parts = []
            for cid, (win, mp, neg) in comps.items():
                lcol = pref + cid + ".last_history_value"
                pcol = pref + cid + ".post_pipeline_value"
                raw = (pd.to_numeric(df[lcol], errors="coerce")
                       if lcol in df.columns else pd.Series(np.nan, index=df.index))
                val = _standardise(raw, win, mp)
                if neg:
                    val = -val
                # where the full history is not inside the record, use the engine's
                # recorded value after transforms
                if pcol in df.columns:
                    val = val.fillna(pd.to_numeric(df[pcol], errors="coerce"))
                parts.append(val)
            offset = 10.0  # BuyAndHoldStrategy standardised: constant +10, weight 2
            score = (parts[0] + parts[1] + parts[2] + parts[3] + 2.0 * offset) / 6.0
            active = fc.notna() & (fc != 0)
            for i in np.where(active.values)[0]:
                n_active += 1
                s = score.iloc[i]
                if pd.notna(s) and np.sign(s) == np.sign(fc.iloc[i]) and s != 0:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9
    name = "mean of forecast x (5-day return - coin mean 5-day return), grid cases pooled"
    threshold = "t >= 2 (positive) confirms, t <= -2 (negative) rejects, over at least 500 grid cases"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The forecast's sign does not follow the sign of the equal-weight score "
                           "(momentum + reversal + distance + volatility + 20) / 6 on at least 90 % "
                           "of its active bars."),
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    cases = {}
    for coin in sorted(bars):
        rows = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n - H, H):
                r = close[t + H] / close[t] - 1.0
                rows.append((fc[t], r))
        cases[coin] = rows

    products = []
    for coin, rows in cases.items():
        rets = np.array([r for _, r in rows], dtype=float)
        rets_ok = rets[np.isfinite(rets)]
        if len(rets_ok) == 0:
            continue
        mu = rets_ok.mean()
        for f, r in rows:
            if np.isfinite(f) and np.isfinite(r):
                products.append(f * (r - mu))
    products = np.array(products, dtype=float)
    n_cases = int(len(products))

    mean_p = float(products.mean()) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = products.std(ddof=1)
        t_stat = float(mean_p / (sd / np.sqrt(n_cases))) if sd > 0 else None

    if n_cases < 500:
        status = "not observable"
        decided = f"Only {n_cases} grid cases, fewer than the plan's minimum of 500."
    elif t_stat is not None and mean_p > 0 and t_stat >= 2:
        status = "confirmed"
        decided = "The mean product is positive with t >= 2 over at least 500 cases."
    elif t_stat is not None and mean_p < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean product is negative with t <= -2 over at least 500 cases."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 over at least 500 cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": name,
            "value": mean_p,
            "statistic": ({"name": "t of the mean", "value": t_stat} if t_stat is not None else None),
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": {"grid cases": n_cases},
        "decided_by": decided,
        "reading": ("All grid bars (positions 0, 5, 10, ... of each window with a 5-bar return inside it) "
                    "are cases, flat-forecast ones included, and the coin's mean 5-day return is the mean "
                    "of its grid returns over all its windows."),
    }
